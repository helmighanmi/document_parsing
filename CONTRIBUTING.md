<!--
Path: CONTRIBUTING.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Contributing

Contributions should preserve the repository's main contract: parser backends may differ internally, but consumers receive a normalized result structure.

## Local workflow

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
make ci
```

For new parser backends or formats:

1. document the dependency and license;
2. add a format/backend compatibility rule;
3. normalize output to the existing parse result contract;
4. add deterministic tests;
5. keep heavyweight/network work out of normal unit tests;
6. update architecture/ADR documentation when the design boundary changes.

Do not commit private documents, credentials, `.env` files, model caches, generated RAG exports, or large binary fixtures.
