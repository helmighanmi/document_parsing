<!--
Path: SECURITY.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Security Policy

## Supported code

Security fixes target the latest `main` branch.

## Reporting

Please report security issues privately through GitHub's private vulnerability reporting feature when enabled. Do not open a public issue containing exploit details or credentials.

## Security assumptions

Documents are untrusted input. Parsers can consume significant CPU and memory, and optional third-party backends may have their own attack surface.

The default public UI therefore:

- disables arbitrary local file-path input;
- blocks private/reserved URL destinations;
- validates redirects;
- limits file size and network timeouts;
- runs in a non-root container configuration;
- does not require application secrets.

For internet-facing production use, add reverse-proxy limits, authentication where appropriate, resource quotas, centralized logs/metrics, and sandbox/isolation for heavyweight parsers.
