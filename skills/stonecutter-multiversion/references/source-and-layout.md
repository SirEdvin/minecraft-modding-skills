# Source syntax and resources

Syntax the pinned plugin does not implement fails preprocessing for every node, so check the version column before copying an example. Layout choices live in the project-topology reference.

## Express the smallest source delta

```java
//? if >=1.21 {
newApi();
//?} else
/*oldApi();*/

//? if fabric && minecraft: >=1.21
fabricOnly();
```

- Closed scope: `//? if condition {` through `//?}`.
- Line scope: the condition affects the next non-empty line or logical block.
- Lookup scope: `//? if condition >> 'token'`; add `+` after `>>` to capture the token.
- Branch with `else`, `elif`, or `else if`; on 0.9.x every branch before the last must be closed.
- Predicates: `=`, `!=`, `<`, `>`, `<=`, `>=`, `~` (same major/minor), `^` (same major), plus `!`, `&&`, `||`, and parentheses.
- Define loader/build booleans with `constants`, compared library versions with `targets` (0.10) or `dependencies` (0.9.x; still accepted but deprecated on 0.10 `[source]`), repeated code alternatives with registered `swaps`, and broad reversible renames with `replacements.string`.
- Prefer a condition for an isolated alternate block, a swap for a repeated fragment, and a string replacement for a reversible rename. Regex replacements are slower and need explicit forward and reverse patterns.
- Local swaps (`//$ if ...`) and scoped local replacements (`//~ if ... 'old' -> 'new' {` … `//~}`) exist on both lines.

## Syntax only 0.10 understands `[changelog]`

| Feature | Form |
| --- | --- |
| Chain without closing brace | `//? if 1.21` / line / `//? else` / commented line |
| Any-prerelease predicate | `>=1.0-*` matches `1.0-alpha.1` |
| Named local replacement | `//~ if >=1.21 'A' -> 'B' as id`, later `//~ !id` |
| Anonymous rest-of-file replacement | `... as _` (cannot be disabled) |
| Several local replacements | `//~ if >=1.21 'a' -> 'b', 'c' -> 'd'` |
| Comma-separated toggles | `//~ one, !two` |
| PCRE replacements | `replacements.perl(direction) { replace("A", "B", "B", "A") }` |
| Per-file replacement filter | `include()` / `exclude()` on a replacement |
| Conditionally disabled files | `files.disable(direction, "com/example/compat/")` |
| Range checks in build scripts | `current.parsed in "1.20"..<"1.22"`, `current.parsed(">1.20", "<1.22")` |

Do not add these to a 0.9.x project: the older parser rejects or misreads them, and the build-script functions do not exist.

## Behaviour that differs on 0.10 `[changelog]`

- Disabled scopes are uncommented, checked, and reassembled on every run, so an invalid parameter inside commented-out code is now reported. Code that only ever compiled on a dropped version can start failing preprocessing.
- Line and lookup scopes capture a whole comment instead of splitting it, and a line condition can capture another condition chain.
- Closed scopes are no longer disabled with single-line comments, and nested block-comment placeholders (`/^ ^/`) count depth instead of using superscript numbers. Expect one-time formatting changes on the first switch; review and commit them separately from logic.
- A lookup scope or lookup swap without a match is a warning and a no-op, not an error. A missing token no longer stops the build, so read warnings after a refactor.
- Stonecutter statements inside swap scopes are not processed and emit a warning.
- Replacement validity is checked at runtime: one pattern with several valid replacements is an error, and a cyclic replacement is left unreplaced instead of failing. Local and global string replacements can chain.
- Processed files must be valid UTF-8. Line endings are preserved unless the `line_separator` flag sets one.

## Default file formats

| Style | 0.9.8 `[source]` | Added in 0.10 `[source]` |
| --- | --- | --- |
| `//` and `/* */` | `java`, `scala`, `sc`, `groovy`, `gradle`, `json5` | — |
| Kotlin nested comments | `kt`, `kts` | — |
| Shaders | `fsh`, `vsh` | `glsl` |
| `#` comments | `cfg`, `aw`, `accesswidener`, `ct`, `classtweaker`, `yml`, `yaml` | `toml`, `properties` |
| XML comments | — | `xml`, `html`, `htm`, `xhtml`, `svg`, `xsd`, `xsl` |
| No comments (replacements only) | — | `json`, `mcmeta`, `txt`, `md`, `csv` |

- On 0.9.x `.properties` is not handled even though the FAQ lists it: `#?` conditions in it are copied verbatim `[probe]`. Register it with `stonecutter handlers { inherit("aw", "properties") }`.
- On 0.10 global replacements also apply to the newly registered formats, including the comment-less ones (`.json`, `.toml`, `.txt` confirmed `[probe]`); unregistered extensions are left alone. Before upgrading, search resources for every global replacement key, then scope the replacement with an identifier or an `exclude()` filter where a data file must keep the old text.
- Reuse a handler with `inherit("aw", "your_extension")` before writing an ANTLR-backed custom handler. Custom scanner, commenter, and format APIs changed on 0.10 `[changelog]`; an addon or hand-written handler needs a port.

## Excluding and disabling files

- File filters (`filters` / `files`) are exclusion-only on both lines: an `include` there is reported at build time and can have undefined side effects `[wiki]`. Replacement filters are a separate API and do support `include()`.
- 0.9.x: `stonecutter.filters.exclude("java/com/example/Bad.java")`, relative to each `src/<source-set>/` `[wiki]`.
- 0.10: `stonecutter.files.exclude("com/example/Bad.java")`, relative to every source directory of every source set, so the `java/` or `resources/` segment must be dropped `[changelog]`. A pattern carried over unchanged silently matches nothing.
- 0.10 `files.disable(direction, patterns)` comments the file out with a `stonecutter-disabled` marker and removes it from the build `[wiki]`. Prefer it to a whole-file condition for version-only classes; it is not a substitute for excluding an overridden shared file.
- 0.10 also processes source directories outside `src/<set>/` as long as they sit in the node project directory and not its build directory `[changelog]`. Re-check custom `srcDir` wiring after an upgrade.

## Files a loader reads early

- Use `sc.process(input, output)` only for files a loader consumes before ordinary source/resource processing; it is expensive and not cached like normal generation.
- With Fabric Loom interface injection, point `loom.fabricModJsonPath` at the shared valid JSON file. Unprocessed placeholders must still leave valid JSON.
- Treat access wideners and transformers as build inputs: loader artifact tasks must run after `stonecutterGenerate` and read the node's effective file.
