# removebgvideo-python

Official Python SDK for RemoveBGVideo Public API (`/v1`), aligned with our website API design.

## Installation

```bash
pip install removebgvideo
```

## Quick Start

```python
import os
from removebgvideo import RemoveBGVideoClient

client = RemoveBGVideoClient(api_key=os.environ["REMOVEBGVIDEO_API_KEY"])

job = client.create_job(
    video_url="https://cdn.example.com/input.mp4",
    model="pro",
    text_prompt="person wearing red jacket",
    bg_type="transparent",
    output_format="webm",
)

result = client.wait_for_completion(job["id"])
print(result.get("output_url"))
```

## More Examples

- `examples/basic.py` - create and wait for a job
- `examples/upload_then_process.py` - upload local file then process
- `examples/admin_key_ops.py` - admin key management

## Public API Methods (`RemoveBGVideoClient`)

- `upload(file_path)`
- `create_job(...)`
- `start_job(job_id)`
- `get_job(job_id)`
- `list_jobs(limit=20, offset=0, status=None)`
- `usage_summary(days=7)`
- `usage_events(limit=20)`
- `wait_for_completion(job_id, interval_seconds=2, timeout_seconds=600)`

## Admin API Methods (`RemoveBGVideoAdminClient`)

```python
from removebgvideo import RemoveBGVideoAdminClient

admin = RemoveBGVideoAdminClient(admin_token="YOUR_ADMIN_TOKEN")
print(admin.get_config())
print(admin.list_keys())
```

- `get_config()`
- `list_keys()`
- `create_key(client_id, note=None)`
- `disable_key(key_fingerprint)`
- `enable_key(key_fingerprint)`

## Environment

- `REMOVEBGVIDEO_API_KEY`
- `REMOVEBGVIDEO_ADMIN_TOKEN` (if using admin client)

## License

MIT

## Release

See [RELEASING.md](./RELEASING.md) for PyPI release steps.
