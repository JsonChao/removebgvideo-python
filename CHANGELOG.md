# Changelog

All notable changes to this project will be documented in this file.

## 0.1.0 - 2026-04-19

### Added
- Initial Python SDK for RemoveBGVideo Public API (`/v1`).
- Public client methods:
  - `upload`
  - `create_job`
  - `start_job`
  - `get_job`
  - `list_jobs`
  - `usage_summary`
  - `usage_events`
  - `wait_for_completion`
- Admin client methods:
  - `get_config`
  - `list_keys`
  - `create_key`
  - `disable_key`
  - `enable_key`
- Basic examples and unit tests.
- CI workflow for Python 3.9 and 3.11.
