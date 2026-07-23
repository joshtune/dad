# Dad's Slideshow

A simple, dependency-free photo + video slideshow you can host for free on GitHub
Pages. Edit one file (`media.json`) to control what plays.

## Files

- **`admin.html`** — visual editor: add photos/videos/captions/music, preview live, and publish.
- **`index.html`** — the slideshow player. You rarely need to touch this.
- **`media.json`** — your list of photos/videos, captions, title/end screens, and music.
- **`manifest.json`**, **`sw.js`**, **`icon-*.png` / `apple-touch-icon.png` / `favicon-32.png`** —
  the PWA bits (see below). Commit them, but you never edit them by hand.
- **`README.md`** — this file.

## Install it on your phone (PWA)

The site is a Progressive Web App, so you can add it to your home screen and it opens
full-screen like a real app (and the player works offline once cached). The **editor** is
the installed app; "Play slideshow" is available as a long-press shortcut on the icon.

- **iPhone (Safari):** open the editor → Share → **Add to Home Screen**.
- **Android (Chrome):** open the editor → menu **⋮** → **Install app** / **Add to Home screen**.

Install and offline need a **secure origin** — use the live `https://…github.io/…` site (or an
HTTPS tunnel). Plain `http://<ip>` won't register the service worker.

## Easiest workflow: the editor (`admin.html`)

1. Run a local server (see below) and open **http://localhost:8000/admin.html**.
2. Fill in the title, add slides (photos, videos, chapter cards), set captions/dates and a music URL.
   Everything autosaves in your browser and shows in the **live preview** on the right.
3. Press **Publish** once your GitHub details + token are filled in (bottom of the editor) — it
   commits `media.json` straight to your repo and GitHub Pages rebuilds in about a minute.

You don't have to use the editor — you can still hand-edit `media.json` directly (format below).

### Publishing from the editor — GitHub token setup (one time)

The Publish button talks to GitHub directly from your browser, so it needs a token:

1. Go to <https://github.com/settings/personal-access-tokens/new> (fine-grained token).
2. **Resource owner**: you. **Repository access**: only the slideshow repo.
3. **Permissions → Contents: Read and write**. Generate, copy the token.
4. Paste it into the editor's **token** field (plus owner/repo). It's stored only in your
   browser's localStorage and sent only to GitHub — never committed or shared.

The **first** time, tick "Push index.html too" in the editor's advanced section so the live
player matches. After that, leave it off — publishing just updates `media.json`.

## How to add your photos & videos

Open `media.json` and edit the `"slides"` list. Each slide is one entry:

```json
{ "type": "photo", "url": "https://.../photo.jpg", "caption": "Summer 1985" }
{ "type": "video", "url": "https://.../clip.mp4",  "caption": "Dad's speech" }
```

- **`type`** — `"photo"` or `"video"`. You can omit it; the player guesses from the
  file extension (`.mp4`, `.webm`, `.mov` → video, otherwise photo).
- **`url`** — a direct link to the image or video file (must end in the file itself,
  e.g. `.jpg`/`.png`/`.mp4`, not a webpage that *shows* the photo).
- **`caption`** — optional text shown at the bottom. Leave out for no caption.
- **`duration`** — optional, seconds this photo stays on screen (overrides the global
  `photoDuration`). Ignored for videos — they always play in full.

### Title & end screens

Edit `"title"` (shown on the start screen) and `"end"` (the closing slide):

```json
"title": { "heading": "For Dad", "subtitle": "A life in pictures" },
"end":   { "heading": "We love you, Dad", "subtitle": "With love, always ❤️" }
```

### Background music

Put a direct link to an `.mp3`/`.m4a` file in `"music"`. It plays across photo slides
and automatically pauses during videos (so you hear the video's own sound), then resumes.

```json
"music": "https://.../song.mp3"
```

Leave it as `""` for no music. (Browsers require one click to start audio — that's what
the **Start** button on the title screen is for.)

## Controls

- **Auto-play**: starts automatically after you press Start. Photos advance on the timer;
  videos play fully, then advance.
- **Manual**: click the left/right edges of the screen, use the on-screen ‹ ❚❚ › buttons,
  or press **← / →**. Any manual move pauses auto-play; press **space** or ❚❚ to resume.
- **Fullscreen**: the ⤢ button or press **f**.
- **Mute music**: the ♪ button.

## Where to put the photos/videos (the URLs)

The slideshow streams media from URLs — it doesn't store the files. Good sources:

- **This repo**: drop files in an `images/` folder and use a relative URL like
  `"images/dad.jpg"`. Simplest and most reliable. (GitHub has a 100 MB/file limit and
  repos work best under ~1 GB total — fine for photos, watch out for long videos.)
- **Cloud storage with direct links** (Cloudflare R2, S3, Backblaze, Dropbox*, etc.).
- **YouTube/Vimeo/Google Photos/Drive share pages do _not_ work** as `url` values —
  those are web pages, not direct file links. (Tell me if your media lives in Google
  Photos/Drive and I'll set up the right approach.)

\* Dropbox: change `?dl=0` to `?raw=1` at the end of the share link.

## Test it locally

Because the page loads `media.json` with `fetch`, opening `index.html` directly with a
`file://` path won't work in most browsers. Run a tiny local server instead:

```bash
cd dad
python3 -m http.server 8000
# then open http://localhost:8000
```

## Publish on GitHub Pages (free, your-name.github.io)

1. Create a GitHub repo and push these files (see commands below).
2. In the repo: **Settings → Pages → Build and deployment**.
3. Source: **Deploy from a branch**. Branch: **main**, folder: **/ (root)**. Save.
4. Wait ~1 minute. Your slideshow is live at
   `https://<your-username>.github.io/<repo-name>/`.

To get the special `https://<your-username>.github.io/` (no repo path), name the repo
exactly `<your-username>.github.io`.

```bash
cd dad
git init
git add .
git commit -m "Dad's slideshow"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

After it's live, you can edit `media.json` directly on github.com (pencil icon),
commit, and the live site updates in about a minute.
