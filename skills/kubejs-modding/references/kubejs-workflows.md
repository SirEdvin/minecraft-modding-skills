# KubeJS Workflows

Official sources used for this reference:

- KubeJS wiki: https://kubejs.com/wiki/
- KubeJS folder structure: https://kubejs.com/wiki/folder-structure
- KubeJS events: https://kubejs.com/wiki/events
- KubeJS addons: https://kubejs.com/wiki/addons
- KubeJS tooling: https://kubejs.com/wiki/tooling
- Rhino project: https://github.com/KubeJS-Mods/Rhino
- ProbeJS project: https://github.com/Prunoideae/ProbeJS

## Version Checks

- Minecraft version and loader.
- KubeJS major/version and addon versions.
- Rhino version bundled by the installed KubeJS line.
- ProbeJS version and generated typings freshness.

## Script Scopes

- `startup_scripts`: startup-only registration and type/schema setup. Restart after changes.
- `server_scripts`: recipes, tags, datapack/server behavior, reloadable server events when supported.
- `client_scripts`: client-only UI/rendering behavior. Never put server-required behavior here.

## Recipes, Tags, Schemas

- Check existing script style before adding helpers.
- Prefer data-driven JSON where KubeJS already forwards custom recipe schemas.
- For custom schemas, verify the addon or Java mod exposes the recipe type/serializer expected by scripts.
- Keep generated/server reload behavior clear: not every script change is reloadable.

## Java Addon Boundary

- Java addon code owns registries, custom events, exposed wrappers, and integration classes.
- KubeJS scripts own pack-specific data and behavior.
- When a script needs a missing Java surface, add the smallest addon API and document the event/type name in generated typings if the project uses ProbeJS.

## Debug Loop

- Read `kubejs/logs/` first for script errors.
- Check the main client/server log for Java exceptions and addon loading errors.
- Restart after startup script or compiled mod changes.
- Use `/reload` for server script/datapack changes only when the installed KubeJS version supports the target reload path.
