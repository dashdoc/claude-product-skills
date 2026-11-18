# FigJam / Figma board mechanics — shared reference

Operational know-how for writing to the **Betting-Fabien** FigJam board (file key `ZsyYHB1iSYvWDZerEZfHR4`) via `mcp__1ba6bdfa-e088-4566-98a8-89902a5b5b12__use_figma` and `upload_assets`. Hard-won; read before populating a block or importing images.

---

## 1. Coordinates: section children are SECTION-RELATIVE

The #1 source of "everything landed off-canvas." Empirically confirmed:

- A node **directly inside a SECTION** uses coordinates **relative to the section's top-left**. After `section.appendChild(node); node.x = X`, the result is `node.absoluteBoundingBox.x === section.absoluteBoundingBox.x + X`.
- So to place a child at a **target absolute point**: `node.x = targetAbsX − section.absoluteBoundingBox.x` (same for y). Valid relative range is `0 … section.width` × `0 … section.height`.
- Assigning a **page-absolute** coordinate (e.g. a negative board coord like `-5040`) directly to a section child throws it thousands of px away.
- Nodes appended directly to the **PAGE** (`page.appendChild` or default) use **page-absolute** coords — the opposite convention.
- `absoluteBoundingBox` is for **reading/verifying only**, never for assignment to a section child.

**Always verify after writing:** read each child's `absoluteBoundingBox` and confirm it's within the section box; if not, reposition with relative coords and report it.

```js
// place children inside a section using a relative layout, then verify
const sec = await figma.getNodeByIdAsync(SECTION_ID);
const W = sec.width, H = sec.height;               // relative canvas
// ...create nodes, sec.appendChild(n), n.x/n.y in [0..W]x[0..H]...
const sb = sec.absoluteBoundingBox; let overflow = 0;
for (const c of sec.children){ const b=c.absoluteBoundingBox; if(!b) continue;
  if (b.x<sb.x-2||b.y<sb.y-2||b.x+b.width>sb.x+sb.width+2||b.y+b.height>sb.y+sb.height+2) overflow++; }
// overflow must be 0
```

## 2. Importing images (competitor screenshots, references)

Use the `upload_assets` MCP tool — it supports **PNG, JPG, GIF, WebP** (max 10MB).

Recipe that works:
1. In `use_figma`, create a **rectangle** sized to the image's aspect ratio, append it to the target section/page, give it a placeholder fill + stroke + cornerRadius. Capture its node id.
2. Call `upload_assets` with `count:1`, `nodeId:<rectId>`, `scaleMode:"FIT"` → returns a single-use `submitUrl`.
3. **POST the bytes immediately** — the submit URL expires fast (you'll see `{"success":false,"error":"Upload has expired"}` if you dawdle). Re-request a fresh URL and POST again if it expires.
   ```bash
   curl -s -X POST "<submitUrl>" -F "file=@/tmp/img.png;type=image/png"
   # success → {"success":true,"imageHash":"…","placedOnNodeId":"…"}
   ```
4. Size the rect to the image aspect ratio so `scaleMode:"FIT"` fills cleanly (no letterboxing).

Notes:
- `nodeId` sets the image as a **fill on that existing node** — the controllable path (you choose position + caption). Without `nodeId`, it auto-creates frames on the current page (uncontrolled placement).
- WebP uploads fine via `upload_assets`, but `figma.createImageAsync(url)` in plugin code does **not** reliably handle WebP — prefer `upload_assets`, or convert first.

## 3. Getting competitor screenshots

- **Help centers are usually gated** (HTTP 403 to WebFetch, login walls): Samsara KB, many support portals.
- **Marketing / product pages expose usable CDN image URLs** (png/webp) — this is the reliable source. WebFetch the product page and ask for "direct image URLs (png/jpg/webp) of product screenshots." Worked for Shippeo, FourKites, Samsara (ctfassets), Webfleet (media.webfleet.com).
- **Resize via CDN params** when present (Cloudinary/Contentful): bump `w_…,h_…` or `?w=…&h=…&fm=png` for a higher-res, PNG-formatted copy.
- Convert WebP→PNG locally with `sips -s format png in.webp --out out.png` (macOS); check dims with `sips -g pixelWidth -g pixelHeight`.
- If nothing good is found, hand the user **Google Images / YouTube search URLs** (`https://www.google.com/search?tbm=isch&q=…`, `https://www.youtube.com/results?search_query=…`) plus the specific help-center article URLs (they render screenshots in a logged-in browser even when gated to the fetcher).

## 4. Text & stickies

- `figma.createText()` → `await figma.loadFontAsync(node.fontName)` **before** setting `.characters`; set `.fontSize` after.
- `figma.createSticky()` → set `.text.characters` (load `.text.fontName` first to be safe), `.authorVisible = false`, and `.fills = [{type:"SOLID",color:{r,g,b}}]` (0–1 floats). Don't leave the default yellow — color-code by theme, or copy a peer sticky's fills.
- Stickies have a fixed-ish width and grow **vertically** with text — keep entries short or they get tall.

## 5. Misc gotchas

- **Don't** set `figma.currentPage = page`; use `await figma.setCurrentPageAsync(page)`.
- To find a node on another page, `await figma.getNodeByIdAsync("123:456")` resolves document-wide (convert a URL `node-id=7600-7083` → `"7600:7083"`).
- Guard recursion: not every node has `.children` (e.g. `LINK_UNFURL`) — check `"children" in node` before descending.
- `get_metadata` is **design-files only** — not FigJam; inspect FigJam via `use_figma` instead.
