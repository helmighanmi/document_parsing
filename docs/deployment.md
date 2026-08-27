<!--
Path: docs/deployment.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Deployment

The Docker image runs as an unprivileged user and includes only the OCR system dependencies needed by the default Tesseract path.

```bash
docker compose up --build
```

For public deployments:

- keep `ALLOW_LOCAL_PATH_INPUT_IN_UI=false`;
- keep `ALLOW_PRIVATE_NETWORK_URLS=false`;
- terminate TLS at a trusted reverse proxy;
- set an upload/body limit at the proxy in addition to application limits;
- restrict CPU/memory because document and OCR workloads are attacker-controlled;
- centralize logs and add request-level metrics/traces at the platform boundary.
