You are working in a Minecraft Java mod repository.

Task: <describe the concrete change>

Constraints:
- First read `gradle.properties`, `settings.gradle(.kts)`, root/module build files, and loader metadata before editing.
- Identify active Minecraft version, loader(s), Java target, and module layout from files; do not guess.
- Use official Fabric/Forge/NeoForge/CC:Tweaked/docs matching the active version for API details.
- Keep common code and loader-specific adapters separate according to the existing layout.
- Preserve metadata placeholders, dependency scopes, resource namespaces, mixin/access-widener conventions, and generated-resource workflow.
- Do not run destructive git commands or discard user changes.

Verification:
- Run the narrowest relevant Gradle task first, then `./gradlew build --no-daemon` or the repository's documented equivalent when practical.
- Report exact files changed, commands run, and any blockers.
