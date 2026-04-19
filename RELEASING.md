# Releasing (Python)

## 1) Prerequisites

- PyPI project created (`removebgvideo`)
- GitHub secret configured:
  - `PYPI_API_TOKEN`

## 2) Bump version

Update version in `pyproject.toml` and add changelog entry.

## 3) Tag and push

```bash
git tag v0.1.0
git push origin v0.1.0
```

GitHub Actions will build and publish to PyPI.
