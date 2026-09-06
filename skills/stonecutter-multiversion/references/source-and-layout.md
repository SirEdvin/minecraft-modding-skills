# Source deltas, layouts, and resources

Preserved 0.9.x guidance; consult the core skill and its version-boundary references before using newer wiki syntax.

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
   - Line scope: condition affects the next non-empty line/logical block.
   - Lookup scope: `//? if condition >> 'token'`; add `+` after `>>` to capture the token.
   - Branch with `else`, `elif`, or `else if`; every branch before the last must be closed.
   - Predicates: `=`, `!=`, `<`, `>`, `<=`, `>=`, `~` (same major/minor), `^` (same major), plus `!`, `&&`, `||`, and parentheses.
   - Define loader/build booleans with `constants`, library versions with `dependencies`, repeated code alternatives with registered `swaps`, and broad reversible renames with `replacements.string`.
   - Prefer string replacements. Regex replacements are slower and require explicit forward and reverse patterns. Avoid ambiguous or cyclic replacement graphs.
   - Local swaps (`//$ if ...`) and scoped local replacements (`//~ if ... 'old' -> 'new'`) are released in 0.9.x. Prefer registered swaps for repeated logic and review every transformed node.
   - Do not copy 0.10 `targets`, named local replacements (`as name` / `as _`), or `getAs` property examples into 0.9.x. Keep `dependencies` and the matching property API until a deliberate migration.

## Choose a maintainable multi-loader layout
   - Flat nodes combine version and loader in one tree and use split build scripts/constants. They suit small or Mixin-heavy mods.
   - Branched `common`/`fabric`/`neoforge` sources isolate loader APIs and cache well, but require more Gradle wiring.
   - Official guidance prefers split native loader build scripts for long-term flat multi-loader maintenance. Do not force one build plugin to emulate every loader when native plugins are clearer.
   - Keep logical Minecraft version separate from project names such as `1.21.1-fabric`; otherwise the loader suffix is parsed as a SemVer prerelease.

## Handle resources and uncommon formats intentionally
   - 0.9.7 source defaults cover Java/Scala/Groovy/Gradle/JSON5, Kotlin, shaders, YAML, CFG, access wideners/transformers, and class tweakers—but not `.properties`, despite the FAQ claim.
   - For `.properties`, explicitly register `stonecutter handlers { inherit("aw", "properties") }` or another handler whose comment syntax matches the file.
   - Reuse a handler with `stonecutter handlers { inherit("aw", "your_extension") }` before writing an ANTLR-backed custom handler.
   - `stonecutter.filters` is exclusion-only; paths are relative to each `src/<source-set>` directory. Do not call `include`.
   - Use `sc.process(input, output)` only for files a loader consumes before ordinary source/resource processing; it is expensive and not normally cached/parallelized.
   - With Fabric Loom interface injection, set `loom.fabricModJsonPath` to the shared valid JSON file. Unprocessed placeholders must still leave valid JSON.

