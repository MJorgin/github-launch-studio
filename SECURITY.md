# Security Policy

## Reporting a vulnerability

Please report suspected security issues privately through GitHub Security Advisories when available. Do not include working exploit code, private credentials, or personal data in a public issue.

Include:

- affected file or workflow;
- steps to reproduce, with sensitive values redacted;
- expected and actual behavior;
- suggested remediation, if available.

## Local data and credentials

- `scripts/repo_audit.py` works offline and only reads repository files.
- `scripts/benchmark_github.py` sends repository slugs to the public GitHub API and may use `GITHUB_TOKEN`; it never prints the token.
- Do not commit `.env` files, API keys, private screenshots, customer data, or cloud credentials.
