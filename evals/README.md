<!--
Path: evals/README.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Parsing Quality Evaluations

Software tests answer **“does the pipeline behave according to its contract?”** Parsing evaluations answer **“how good is the extracted content?”** Those concerns should remain separate.

A production evaluation set should use redistributable or internally approved documents with gold expectations such as:

- required text coverage/recall;
- table cell accuracy;
- page attribution accuracy;
- OCR character/word error rate;
- heading/list preservation;
- parser latency and peak memory;
- RAG chunk coverage and provenance completeness.

Heavy parser/model evaluations should run on a scheduled or release workflow rather than every pull request. Do not commit confidential source documents as evaluation fixtures.
