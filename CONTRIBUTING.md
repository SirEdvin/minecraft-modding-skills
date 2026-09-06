# Contributing skill improvements

## Destination and scope

Update packages in this repository under `skills/<name>/`, not only an agent's installed runtime copy. Use a feature branch and pull request; an open PR is not a merged release. When building on another open PR, name the dependency and use its branch as the review base until it merges.

Do not modify example projects merely to make skill guidance appear correct. Inspect pinned revisions, use disposable checkouts for builds, and keep unrelated local edits and runtime configuration out of the contribution.

## Authoring contract

- Keep package names stable and lowercase-hyphenated; update discovery, README, and provenance together for intentional additions/renames/removals.
- Keep the description a single capability sentence, at most 60 characters and ending in a period. This is this repository's routing policy, stricter than the 1024-character Agent Skills maximum.
- Use portable frontmatter fields. `metadata` maps string keys to string values; put author, version, and comma-separated tags there rather than nesting agent-specific structures.
- Preserve existing attribution. Do not derive authors from the machine's login, Git identity, or environment.
- Aim for a concise always-loaded workflow. Move substantial API tables, examples, and source maps to directly linked package-local `references/`; reusable code belongs in `scripts/` and needs tests.
- Individual package installs must work without repository-level documents or adjacent skill directories. Other package names may be optional recommendations, not implicit local-file dependencies.
- Match examples to an explicit game/loader/mapping/tool version. Prefer exact project configuration, official versioned docs, release source/tests, then pinned examples. Label contradictions and unresolved claims.
- Use imperative decision rules that explain the failure they avoid. Keep project-specific observations labeled as examples, not universal Minecraft rules.
- Preserve useful domain detail while removing repetition, stale paths, fabricated tasks, and unqualified latest-version advice.
- Do not copy unlicensed skill prose. Record independently researched sources in `PROVENANCE.md` or an explicitly linked source map.

## Validation and review

1. Run the commands in README's Validate section: regression tests, repository validator, official package validator, discovery, and diff whitespace checks.
2. Review every new support file; unstaged/new files are not shown by a normal tracked-only diff.
3. For command/API changes, exercise a safe disposable fixture or real version-pinned project when feasible. Record precisely what ran, including discovered/executed test counts and skipped tasks.
4. For a library-wide audit, reconcile the directory inventory with a per-package evidence table. A skill that is not applicable to the sample projects still needs source/API review; do not invent project usage.
5. Keep audit observations separate from normative package instructions. A build blocked by the environment or an existing project defect is not a skill-validation success.
6. Request an independent review of meaningful changes, resolve actionable findings, and include sources, checks, and limitations in the PR.
7. Verify the remote head and changed-file list after pushing; inspect finished CI before reporting green. Do not merge or publish mod artifacts without authorization.

The repository validator intentionally supplements the official validator, including compact descriptions, scalar metadata, canonical discovery coverage, and package-link boundaries. Changes to these checks require synthetic regression tests, not edits that merely make the current corpus pass.
