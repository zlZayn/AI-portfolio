# Data Table Snapshots

These versioned fixtures power the portfolio's generated comparison tables.

- `decision-maker/`: small dirty/clean examples and categorical-analysis output from `AI-decision-maker`.
- `schema-mapper/`: showcase input, cleaned output, and quality report from `AI-schema-mapper`.
- `tier-guardian/`: batch evaluation output from `AI-tier-guardian`.

The build reads only these snapshots so it produces the same page in a normal checkout, a Git worktree, or a standalone clone. To refresh them, replace the matching files from the source projects, review the data diff, run the test suite, and rebuild `index.html` in the same commit.

- Rules → [AGENTS.md](AGENTS.md)
