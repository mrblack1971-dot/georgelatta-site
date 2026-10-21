# Adding a trip to the Travel Journal

1. **Photos:** convert to WebP in two sizes into `images/` (name them e.g. `trip-myplace-1`):
   ```
   python3 -c "from PIL import Image,ImageOps;im=ImageOps.exif_transpose(Image.open('IN.jpg')).convert('RGB')
   for w,s in[(1000,''),(500,'-sm')]:
     c=im.copy();c.thumbnail((w,w*2));c.save(f'images/trip-myplace-1{s}.webp',quality=78)"
   ```
2. **Add an entry** to `travels/trips.json` (copy an existing one):
   - `slug` – URL folder (lowercase-with-dashes), `title`, `date` (display text), `sort` (YYYY-MM-DD, newest shows first)
   - `image` – cover photo base name without `-sm.webp` (empty = "Photo coming soon"), `alt` – description
   - `teaser` – one or two sentences for the card
   - `body` – list of paragraphs (HTML allowed; items starting with `<!--` are hidden comments)
   - `photos` – optional list of `[image-base-name, caption]` for a gallery on the trip page
   - `draft` – `true` shows a "Draft" tag; set `false` once George approves the story
   - Only real facts. No confirmation numbers, home address or room details.
3. **Build:** `python3 build_travels.py` — regenerates `travels/index.html`, each `travels/<slug>/index.html`,
   and the 3 newest cards on the homepage (between `<!--TRIPS-->` markers; don't edit those by hand).
4. **Preview** `index.html` locally, then publish: push changed HTML/CSS to `main` of
   `mrblack1971-dot/georgelatta-site`; new images go up as a base64 tarball in `_b64/part_*`,
   which `.github/workflows/publish.yml` decodes and force-pushes to `gh-pages`.

# Adding a lodge visit to "Traveling Man"

Same steps, different data file: add an entry to `traveling-man/visits.json`, then run `python3 build_travels.py`
(it builds both the Travel Journal and Traveling Man, including the homepage cards between `<!--VISITS-->` markers).
Fields: `slug`, `title` (lodge or Grand Lodge name), `place` (City, State), `date` (display), `sort` (YYYY-MM-DD),
`image`/`alt` (empty = photo slot), `teaser`, `body` (paragraphs), optional `photos`, `draft`.
Pages appear at `traveling-man/<slug>/`. Only verified visits (e.g. from the Masonic Life Facebook page or George).
