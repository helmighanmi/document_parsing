<!--
Path: docs/development.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Development

Use Python 3.11 for the reference environment.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pre-commit install
make ci
```

Keep parser-specific imports inside adapter methods when the dependency is optional. New formats must include a compatibility mapping, normalized result contract, unit tests, and at least one local integration test when practical.
