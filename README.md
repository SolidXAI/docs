# SolidX documentation

This Next.js site uses Fumadocs to serve two documentation sections:

- **SolidX:** `/docs/solidx`
- **Test Hub:** `/docs/test-hub`

Their root folders in `content/docs` define the sidebar switcher. Each folder has a `meta.json` with `"root": true` and an `index.mdx` landing page. Add new pages inside the appropriate folder and list them in its `meta.json`.

Previous SolidX URLs under `/docs/quick-start`, `/docs/developer-docs`, `/docs/recipes`, `/docs/tutorial`, and `/docs/admin-docs`, plus the old Test Hub URLs under `/docs/product-modules/test-hub`, redirect to the corresponding section. Keep these redirects in `next.config.mjs` when reorganizing pages.

## Run locally

```bash
npm ci
npm run dev
```

The development server uses port 3003. Run `npm run build` before publishing.
