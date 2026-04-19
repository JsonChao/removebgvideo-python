# Contributing

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Guidelines

- Keep API surface aligned with backend `/v1` endpoints.
- Add tests for new methods.
- Update `README.md` and `CHANGELOG.md` in the same PR.
