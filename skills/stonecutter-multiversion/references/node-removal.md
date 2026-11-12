# Removing a version node

Removal touches more files than the settings line, and two orderings break the build outright. Work through the steps in order and keep each phase a separate commit so a reviewer can tell source-state churn from real deletions.

## 0. Inventory before deleting anything

Search the whole repository for the node's project name and for its logical version (they differ in flat `{version}-{loader}` layouts). Record every hit in:

- settings: `versions(...)`, `version(...)`, branch version lists, data-driven tree files, per-node `buildFileName` redirects, `vcsVersion`;
- every controller's `stonecutter active` literal or active file — one per tree;
- version overrides: `versions/<project>/` in the root branch and in every branch (`src/` overrides, `gradle.properties`, `stonecutter.properties.*`, access wideners/transformers, fixtures);
- build logic: build scripts used only by that node, `if (version == ...)` branches, version catalogs, toolchain/Java level maps, loader plugin versions needed only by that node;
- structured properties: tables or tagged keys for the version;
- Stonecutter parameters: constants, targets/dependencies, swaps, and replacements whose direction compares against the removed boundary;
- source conditionals mentioning the version or a constant that only that node set;
- CI: build/test matrices, "for each active node" loops, JDK setup steps, cache keys, required-check names;
- publication: publish task selectors, release asset collection, expected artifact counts, mod-platform game-version lists, metadata compatibility ranges;
- documentation: supported-version tables, README commands, changelog.

Run `./gradlew projects` and save the node list; it is the baseline for the final comparison.

## 1. Move the active and VCS state off the node first

Both statements must name a registered node or configuration fails for every task, including the switch tasks that would fix it (0.9.8 and 0.10 `[probe]`):

- a removed node still named by `vcsVersion` → `VCS version '<x>' doesn't match any registered subproject` on 0.9.8, `VCS project '<x>' doesn't match any registered subproject for project '<path>'` on 0.10;
- a removed node still named by the active literal → `Version '<x>' is not registered`.

So, while the node is still registered:

1. Switch every tree to a retained node with its discovered `Set active project to ...` task. In a multi-tree build an unqualified task switches all trees; confirm each controller's literal afterwards.
2. If the node was the VCS node, set `vcsVersion` to a retained node and run `Reset active project`. This rewrites every conditional in shared sources to the new canonical state. Commit that churn alone, before any deletion, and build all nodes on it.
3. If the node was not the VCS node, reset now and confirm a clean `git status`.

If the declaration was already deleted, edit the active literal (or active file) by hand to a retained node, then run `Refresh active project` so the sources match it.

## 2. Remove the registration

- Delete the node from settings or the tree data file, plus any `buildFileName` redirect or special-case loop that names it. A redirect left behind fails with an unknown project path.
- With branches, remove the version from the tree and from every branch that listed it explicitly.
- Run `./gradlew projects` and `./gradlew tasks --all`: the node, its tasks, and its switch task must be gone, and nothing else.

## 3. Delete version overrides and node-only build logic

- Delete `versions/<project>/` in every branch. Stonecutter ignores an unregistered directory, so leftovers produce no error and silently rot `[probe]`.
- Before deleting, check whether any override there is still the only correct implementation for a retained node's neighbour range; move it rather than lose it.
- Delete build scripts, catalogs, property tables, and plugin versions used only by the removed node. Remove the JDK or toolchain only if no retained node and no tool (including the Stonecutter launcher requirement) still needs it.
- When a tree is left with one node, any full-file override of that node now collides with the shared file on every build `[probe]`; fold the override into shared sources.

## 4. Remove dead conditionals and parameters

A condition that is constant across all retained nodes is dead weight, and on 0.10 its disabled branch is still parsed on every run, so a stale identifier there becomes a preprocessing error `[changelog]`.

1. List candidates: search Stonecutter comments (`//?`, `/*?`, `#?`, `//$`, `//~`) for the removed version, for boundaries at or beyond it, and for constants only that node enabled.
2. Evaluate each condition against the retained set. Always true: keep the body, delete the markers and the `else` branch. Always false: delete the branch and its commented-out body. Mixed: keep.
3. Remove constants, targets, and swaps nothing references any more. A remaining reference fails preprocessing with `Unresolved constant '<name>'` and the file position `[probe]`, which is the signal that one was missed.
4. For a replacement whose direction is now constant: if it is always false, delete the registration; if it is always true, confirm the sources already hold the replaced text in the VCS state, then delete it. A switch round trip must leave no diff afterwards.
5. Do not hand-edit commented-out code to "fix" it for a version that no longer exists; delete it.

Keep version boundaries that still separate retained nodes even if they were introduced for the removed one.

## 5. CI, publication, and documentation

- Remove the node from every matrix and loop, then check that required-check names did not change or that branch rules were updated; a required check that no longer runs blocks merges forever.
- Recompute the expected artifact inventory (artifact × version × loader, plus sources) and update any asserted count. Compare the release task's resolved asset list with it in a dry run.
- Tighten metadata compatibility ranges and platform game-version lists so retained artifacts do not claim the dropped version.
- Leave already published artifacts and tags for the removed version untouched. State the end of support in the changelog instead.
- Update supported-version tables and example commands.

## 6. Verify

1. `./gradlew projects` matches the baseline minus exactly the removed nodes.
2. A repository-wide search for the project name and logical version returns only history (changelog, archived reports).
3. Build all nodes, then switch to each other retained node and build again, as separate invocations.
4. Run `Reset active project`; `git status` is clean and the active literal equals `vcsVersion` in every tree.
5. Run the retained nodes' real tests; a removal often deletes a fixture or bootstrap dependency another node shared.
6. The dry-run release inventory equals the recomputed expectation.
