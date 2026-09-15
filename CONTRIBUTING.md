# Contributing

Thanks for your interest in GitHub Launch Studio.

## Good first contributions

- Improve launch checklist wording or add a missing edge case.
- Add a benchmark category with current public evidence.
- Improve repository-language heuristics in the audit script.
- Report unclear Skill instructions or false-positive audit findings.
- Fix documentation links, typos, and Chinese/English phrasing.

## Pull requests

1. Open an issue first for non-trivial behavior changes.
2. Keep changes focused; launch guidance should stay practical rather than becoming a generic marketing manual.
3. Preserve the safety boundary: no fake growth, scraped outreach, fabricated metrics, undisclosed paid promotion, or automatic external posting.
4. Run:

   ```bash
   python -m py_compile scripts/repo_audit.py scripts/benchmark_github.py scripts/render_social_card.py
   python scripts/repo_audit.py . --pretty
   ```

5. If benchmark numbers are updated, include the observation date.

## Commit messages

Use concise conventional messages such as:

- `feat: add Rust project audit signals`
- `fix: ignore .env.example in secret candidate scan`
- `docs: refresh benchmark observations`
