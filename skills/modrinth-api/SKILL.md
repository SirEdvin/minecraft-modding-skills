---
name: modrinth-api
description: Use when querying Modrinth API v2 project/search/version/file endpoints, source lookup, loader and Minecraft-version filtering, hashes, downloads, checksum verification, or required User-Agent handling for read-only Modrinth workflows.
license: MIT
compatibility: Independently authored for read-only Modrinth API v2 workflows; verify current official endpoint documentation before relying on parameters or response fields.
metadata:
  author: SirEdvin
  version: "1.0.0"
  hermes-tags: "modrinth, api, minecraft, downloads, hashes"
---

# Modrinth API

Use this specialist for read-only Modrinth API v2 lookup, filtering, and download verification. Always send a uniquely identifying `User-Agent`. Do not perform write/authenticated actions unless the user explicitly asks and provides credentials through an approved secret path.

References:

- `references/read-only-v2.md`

## Workflow

1. Start with official docs for the exact endpoint. Modrinth API behavior is documented per operation.
2. Use `https://api.modrinth.com/v2` for production read-only calls.
3. Send `User-Agent: <owner>/<tool>/<semver> (<contact or repo>)` or another uniquely identifying value.
4. For discovery, use `/search` with documented `query`, `facets`, `index`, `offset`, and `limit` parameters.
5. For a known project, use `/project/{id|slug}` and `/project/{id|slug}/version` with documented filters.
6. For files, select the file with `primary: true`. If none is primary, use the first file in the documented response order as the fallback. Then verify downloaded bytes against `sha512` or `sha1` from that file's metadata.

## Important Limits

- The current official docs for `GET /project/{id|slug}/version` document `loaders`, `game_versions`, `featured`, and `include_changelog`. Do not claim that this endpoint supports `limit` or `offset` unless the official docs add those parameters.
- Search facets encode loader filtering through `categories` and Minecraft version filtering through `versions`; URL-encode the JSON facet string.
- Prefer `sha512` verification when available; `sha1` is still documented for lookup and metadata.

## Validation

- Check HTTP status and rate-limit headers.
- Verify the selected version has the expected loader, game version, project id, and either a primary file or the documented first-file fallback.
- Hash downloaded bytes before trusting a file path or cache hit.
