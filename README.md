<p align="center">
  <img src="https://removebgvideo.com/images/remove-bg-video-logo.png" alt="RemoveBGVideo" width="72" />
</p>

<h1 align="center">RemoveBGVideo Python SDK</h1>

<p align="center">
  Official Python SDK for RemoveBGVideo Public API (<code>/v1</code>)
</p>

<p align="center">
  <a href="https://github.com/JsonChao/removebgvideo-python/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/JsonChao/removebgvideo-python/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <a href="https://github.com/JsonChao/removebgvideo-python/actions/workflows/release.yml"><img src="https://img.shields.io/github/actions/workflow/status/JsonChao/removebgvideo-python/release.yml?branch=main&label=Release" alt="Release" /></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/API-v1-7c3aed" alt="API v1" />
  <img src="https://img.shields.io/badge/license-MIT-16a34a" alt="MIT License" />
</p>

<p align="center">
  <a href="https://removebgvideo.com/docs"><strong>📘 Full Documentation</strong></a>
  ·
  <a href="https://removebgvideo.com/api"><strong>🧪 API Playground</strong></a>
  ·
  <a href="https://removebgvideo.com/api-management"><strong>🔐 API Management</strong></a>
  ·
  <a href="https://github.com/JsonChao/removebgvideo-python"><strong>🐙 GitHub</strong></a>
</p>

## Why This SDK

`removebgvideo-python` wraps `/v1` endpoints with a Pythonic interface for:

- Authenticated job creation and status tracking
- Local upload support
- Usage analytics (`usage_summary`, `usage_events`)
- Admin key management via `X-Admin-Token`
- Structured API exceptions (`ApiError`)

## Installation

```bash
pip install removebgvideo
```

## Requirements

- Python 3.9+
- `requests>=2.31.0` (installed automatically)
- RemoveBGVideo API key for public API
- Optional admin token for admin API

## Quick Start

```python
import os
from removebgvideo import RemoveBGVideoClient

client = RemoveBGVideoClient(api_key=os.environ["REMOVEBGVIDEO_API_KEY"])

job = client.create_job(
    video_url="https://cdn.example.com/input.mp4",
    model="original",
    bg_type="transparent",
    output_format="webm",
    auto_start=True,
)

result = client.wait_for_completion(job["id"], interval_seconds=2, timeout_seconds=600)
print(result.get("output_url"))
```

## Authentication

### Public API Client

```python
from removebgvideo import RemoveBGVideoClient

client = RemoveBGVideoClient(
    api_key="YOUR_API_KEY",
    base_url="https://api.removebgvideo.com",
    timeout=30,
)
```

### Admin API Client

```python
from removebgvideo import RemoveBGVideoAdminClient

admin = RemoveBGVideoAdminClient(
    admin_token="YOUR_ADMIN_TOKEN",
    base_url="https://api.removebgvideo.com",
    timeout=30,
)
```

## End-to-End Workflows

### 1) Process Existing Video URL

```python
job = client.create_job(
    video_url="https://cdn.example.com/input.mp4",
    model="human",
    bg_type="transparent",
    output_format="webm",
    auto_start=True,
)

done = client.wait_for_completion(job["id"])
print(done["status"], done.get("output_url"))
```

### 2) Upload Local File Then Process

```python
uploaded = client.upload("./input.mp4")

job = client.create_job(
    video_url=uploaded["video_url"],
    model="light",
    output_format="webm",
    auto_start=True,
)

done = client.wait_for_completion(job["id"])
print(done.get("output_url"))
```

### 3) Create Pending Job, Start Later

```python
job = client.create_job(
    video_url="https://cdn.example.com/input.mp4",
    model="pro",
    text_prompt="person wearing red jacket",
    auto_start=False,
)

client.start_job(job["id"])
done = client.wait_for_completion(job["id"])
```

## Model Selection Guide

| Model | Speed | Quality | Best For | text_prompt |
|---|---|---|---|---|
| `original` | Standard | Highest | General quality-first segmentation | No |
| `light` | Fastest cost/perf | High | Simple scenes, throughput-first workloads | No |
| `pro` | Slowest | Highest | Complex objects with prompt-based targeting | Yes |
| `human` | Fast | High | Portraits / human subjects | No |

## `create_job` Options

`create_job(...)` parameters:

- `video_url` (str, required)
- `model` (`original` | `light` | `pro` | `human`, default `original`)
- `bg_type` (str, default `green`)
- `output_format` (str, default `webm`)
- `text_prompt` (str, optional, meaningful for `pro`)
- `bg_color` (list[float], optional)
- `auto_start` (bool, default `True`)
- `metadata` (dict, optional)

## Public Client API

### Constructor

```python
RemoveBGVideoClient(api_key: str, base_url: str = "https://api.removebgvideo.com", timeout: int = 30)
```

### Methods

- `upload(file_path)` -> `POST /v1/uploads`
- `create_job(...)` -> `POST /v1/jobs`
- `start_job(job_id)` -> `POST /v1/jobs/{id}/start`
- `get_job(job_id)` -> `GET /v1/jobs/{id}`
- `list_jobs(limit=20, offset=0, status=None)` -> `GET /v1/jobs`
- `usage_summary(days=7)` -> `GET /v1/usage/summary`
- `usage_events(limit=20)` -> `GET /v1/usage/events`
- `wait_for_completion(job_id, interval_seconds=2.0, timeout_seconds=600)` -> polling helper

### Polling Behavior (`wait_for_completion`)

- Returns job payload when `status == "completed"`
- Raises `ApiError` when `status == "failed"`
- Raises `TimeoutError` when elapsed time exceeds `timeout_seconds`

## Admin Client API

### Constructor

```python
RemoveBGVideoAdminClient(admin_token: str, base_url: str = "https://api.removebgvideo.com", timeout: int = 30)
```

### Methods

- `get_config()` -> `GET /v1/admin/config`
- `list_keys()` -> `GET /v1/admin/keys`
- `create_key(client_id, note=None)` -> `POST /v1/admin/keys`
- `disable_key(key_fingerprint)` -> `POST /v1/admin/keys/disable`
- `enable_key(key_fingerprint)` -> `POST /v1/admin/keys/enable`

## Error Handling

```python
from removebgvideo import ApiError

try:
    job = client.get_job("invalid-id")
except ApiError as err:
    print("status:", err.status_code)
    print("code:", err.code)
    print("request_id:", err.request_id)
    print("message:", str(err))
```

## Retry Strategy (Recommended)

Retry only transient failures:

- Retry: `429`, `500`, `502`, `503`, `504`
- No blind retry: `400`, `401`, `403`, `404`

```python
import time
from removebgvideo import ApiError


def with_retry(fn, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except ApiError as err:
            retryable = err.status_code in {429, 500, 502, 503, 504}
            if not retryable or attempt == max_attempts:
                raise
            time.sleep(attempt * 0.5)
```

## Usage & Billing Integration

```python
summary = client.usage_summary(days=7)
events = client.usage_events(limit=50)

print(summary)
print(events)
```

Typical pattern:

1. Use `usage_summary` for high-level dashboard metrics.
2. Use `usage_events` for detailed event-level auditing.

## Examples Included

- [`examples/basic.py`](./examples/basic.py): basic create + wait
- [`examples/upload_then_process.py`](./examples/upload_then_process.py): upload local file then process
- [`examples/admin_key_ops.py`](./examples/admin_key_ops.py): admin key operations

## Environment Variables

- `REMOVEBGVIDEO_API_KEY`
- `REMOVEBGVIDEO_ADMIN_TOKEN` (admin only)

## Changelog and Releases

- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Release process: [RELEASING.md](./RELEASING.md)

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT
