# Data Pebbles — Frontend

Nuxt-based web UI for the Data Pebbles platform. Manage projects and resources across the bronze, silver, and gold layers, preview schemas and data, and view documentation for the Python SDK and MCP server.

## Tech Stack

- [Nuxt 4](https://nuxt.com/) — Vue framework
- [Nuxt UI](https://ui.nuxt.com/) — component library
- [Tailwind CSS 4](https://tailwindcss.com/) — styling
- [Shiki](https://shiki.style/) — syntax highlighting (SDK & MCP docs)
- [DOMPurify](https://github.com/cure53/DOMPurify) — HTML sanitisation

## Pages

| Route | Description |
| --- | --- |
| `/` | Home / redirect |
| `/projects` | Projects list — create, rename, delete projects |
| `/projects/:projectId` | Project detail — resource list with bronze/silver/gold tabs, rename project |
| `/projects/:projectId/:layer/:resourceId` | Resource detail — versions, upload, rename, schema & data preview |
| `/sdk` | Python SDK documentation |
| `/mcp` | MCP server setup & tool reference |

## Setup

```bash
pnpm install
```

## Development

```bash
pnpm dev
```

Runs at `http://localhost:3000`. Expects the backend at `http://localhost:8000`.

## Build

```bash
pnpm build
```

## Other Commands

| Command | Description |
| --- | --- |
| `pnpm lint` | Lint with ESLint |
| `pnpm format` | Auto-fix lint issues |
| `pnpm typecheck` | Run `nuxt typecheck` |
| `pnpm test` | Run Vitest |
| `pnpm openapi` | Regenerate the TypeScript API client from `openapi.json` |
