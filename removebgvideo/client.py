from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests

from .exceptions import ApiError


class RemoveBGVideoClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.removebgvideo.com",
        timeout: int = 30,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            raise ApiError(
                f"Non-JSON response: {response.text[:300]}",
                status_code=response.status_code,
            ) from exc

        if response.status_code >= 400:
            error = data.get("error", {}) if isinstance(data, dict) else {}
            raise ApiError(
                message=error.get("message") or data.get("message") or "Request failed",
                status_code=response.status_code,
                code=error.get("code"),
                request_id=error.get("request_id"),
            )

        return data

    def upload(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("rb") as f:
            resp = requests.post(
                f"{self.base_url}/v1/uploads",
                headers={"X-Api-Key": self.api_key},
                files={"file": (path.name, f)},
                timeout=self.timeout,
            )
        return self._handle_response(resp)

    def create_job(
        self,
        video_url: str,
        model: str = "original",
        bg_type: str = "green",
        output_format: str = "webm",
        text_prompt: Optional[str] = None,
        bg_color: Optional[list[float]] = None,
        auto_start: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "video_url": video_url,
            "model": model,
            "bg_type": bg_type,
            "output_format": output_format,
            "auto_start": auto_start,
        }
        if text_prompt:
            payload["text_prompt"] = text_prompt
        if bg_color is not None:
            payload["bg_color"] = bg_color
        if metadata is not None:
            payload["metadata"] = metadata

        resp = requests.post(
            f"{self.base_url}/v1/jobs",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def start_job(self, job_id: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/v1/jobs/{job_id}/start",
            headers={"X-Api-Key": self.api_key},
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/v1/jobs/{job_id}",
            headers={"X-Api-Key": self.api_key},
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def list_jobs(
        self,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        resp = requests.get(
            f"{self.base_url}/v1/jobs",
            headers={"X-Api-Key": self.api_key},
            params=params,
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def usage_summary(self, days: int = 7) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/v1/usage/summary",
            headers={"X-Api-Key": self.api_key},
            params={"days": days},
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def usage_events(self, limit: int = 20) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/v1/usage/events",
            headers={"X-Api-Key": self.api_key},
            params={"limit": limit},
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def wait_for_completion(
        self,
        job_id: str,
        interval_seconds: float = 2.0,
        timeout_seconds: int = 600,
    ) -> Dict[str, Any]:
        start = time.time()
        while True:
            job = self.get_job(job_id)
            status = job.get("status")
            if status == "completed":
                return job
            if status == "failed":
                raise ApiError(job.get("error", "Job failed"))

            if time.time() - start > timeout_seconds:
                raise TimeoutError(f"Job {job_id} did not complete in {timeout_seconds}s")

            time.sleep(interval_seconds)
