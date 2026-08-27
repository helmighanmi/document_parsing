<!--
Path: docs/decisions/003-safe-remote-ingestion.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# ADR-003: Safe Remote Document Ingestion

## Status

Accepted.

## Context

Accepting arbitrary URLs in a public document parser creates SSRF, unbounded-download, redirect, and resource-exhaustion risk.

## Decision

Validate HTTP(S) URLs before every request/redirect, block non-public IP ranges by default, reject embedded credentials, enforce connect/read timeouts, and stop downloads at a configured byte limit. Local file-path input is hidden in the public UI unless explicitly enabled.

## Consequences

The public default is safer, while controlled internal deployments can opt into private-network URLs through explicit configuration.
