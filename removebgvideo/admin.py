from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests

from .exceptions import ApiError


class RemoveBGVideoAdminClient:
    def __init__(
        self,
        admin_token: str,
        base_url: str = "https://api.removebgvideo.com",
        timeout: int = 30,
    ) -> None:
        if not admin_token:
            raise ValueError("admin_token is required")
        self.admin_token = admin_token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "X-Admin-Token": self.admin_token,
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

    def get_config(self) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/v1/admin/config",
            headers=self._headers(),
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def list_keys(self) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/v1/admin/keys",
            headers=self._headers(),
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def create_key(self, client_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"client_id": client_id}
        if note:
            payload["note"] = note
        resp = requests.post(
            f"{self.base_url}/v1/admin/keys",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def disable_key(self, key_fingerprint: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/v1/admin/keys/disable",
            headers=self._headers(),
            json={"key_fingerprint": key_fingerprint},
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def enable_key(self, key_fingerprint: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/v1/admin/keys/enable",
            headers=self._headers(),
            json={"key_fingerprint": key_fingerprint},
            timeout=self.timeout,
        )
        return self._handle_response(resp)
