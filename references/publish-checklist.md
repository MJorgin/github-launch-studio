# Publishing checklist

## Local verification

- [ ] Repository name matches the package/project name where practical.
- [ ] Description and topics use words a target user would search for.
- [ ] Root README answers who, what, why, how to try, and current limits.
- [ ] Quickstart works from a clean environment.
- [ ] Example input and expected output are real.
- [ ] Installed package name and command match the published instructions.
- [ ] Version tags, release notes, and breaking changes are consistent.
- [ ] License exists and dependencies permit the intended distribution.
- [ ] Supported runtimes, platforms, API services, regions, and costs are documented.
- [ ] CI/build/test/lint checks relevant to the project pass or their absence is acknowledged.
- [ ] Internal links, anchors, documentation links, and image paths resolve.
- [ ] Screenshots and logs exclude tokens, private data, customer names, credentials, and local secrets.
- [ ] `.gitignore` covers build artifacts, environment files, caches, and OS files.
- [ ] Issue templates, discussions, security policy, contributing guide, and roadmap match the project's actual maintenance capacity.
- [ ] Roadmap avoids committing to dates the maintainer cannot promise.

## Clean-install check

When feasible, perform the exact user path:

1. Create a temporary directory.
2. Clone or install the release candidate.
3. Configure only documented prerequisites.
4. Run the quickstart commands.
5. Confirm the expected output or visible result.
6. Test one common option beyond the default.
7. Record platform, runtime, and version details in the release notes or QA notes.

Do not use the maintainer's already-configured global environment as the only proof.

## Repository settings

Recommended for a public solo project:

- protect the default branch against deletion and force pushes;
- require status checks only when they exist and reliably pass;
- enable Issues and Discussions only if someone will respond;
- add a short issue template for bugs and reproducible steps;
- add repository topics, homepage/demo link, and social preview;
- ensure the default branch name in instructions matches GitHub settings;
- review third-party app permissions and secrets before release.

## Security and privacy

Never print or commit:

- API tokens, private keys, `.env` files, cookie strings, or cloud credentials;
- private customer data, employee data, or confidential screenshots;
- hostnames or internal URLs that reveal sensitive infrastructure;
- personal contact information without consent.

If a project collects data or calls external APIs, document:

- what data leaves the machine;
- which provider receives it;
- whether prompts or files are retained or used for training;
- how to disable telemetry or providers;
- enterprise/self-host alternatives, if relevant.

## External action gate

The following require separate explicit user authorization:

- creating or changing a GitHub repository, release, topic, branch rule, or settings;
- pushing tags or opening/merging pull requests;
- posting to social networks or communities;
- commenting as the maintainer;
- sending DMs or emails;
- contacting external users or companies.

Prepare all drafts locally or as a reviewable artifact first. Include the intended account, destination, title/body, media, timing, and whether comments/DMs are enabled.

## Launch-day response plan

Assign a short triage workflow:

- **Crash/blocker:** reproduce, label, acknowledge, patch or provide workaround.
- **Compatibility issue:** collect OS/runtime/version and exact command.
- **Usage question:** answer and turn repeated answers into README/docs.
- **Feature request:** capture goal and context; do not promise roadmap entry immediately.
- **Security report:** move to private channel and avoid exposing exploit details.
- **Negative feedback:** acknowledge the concrete trade-off; avoid defensive marketing.

## Post-launch review

After one week and one month, review signals that fit the project:

- stars and watch/fork conversion;
- README-to-quickstart behavior if analytics are ethical and disclosed;
- issue/question categories;
- successful installs or downloads;
- demo views and external referrals;
- recurring confusion;
- actual bugs and unsupported platforms.

Use the findings to improve activation and docs. Do not optimize for stars through deceptive prompts, fake urgency, or coercive “please star” placement.
