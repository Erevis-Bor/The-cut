# THE CUT — Your personal cinema

A mobile-first, private film and TV discovery app, built for your particular taste.

## Start in 30 seconds

### Option A: open the single HTML file

Open **THE-CUT-standalone.html** in a full browser. It contains the design, scripts and complete catalogue in one file. This is the quickest way to try the app.

**Important:** some mobile file-preview apps block JavaScript or don't retain local storage between openings. For regular use, hosting it on GitHub Pages (below) is much more dependable.

### Option B: GitHub Pages (recommended for everyday use)

1. Create a new GitHub repository, for example `the-cut`.
2. Upload `index.html`, `app.js`, `data.js`, `styles.css`, `manifest.webmanifest`, `sw.js` and the `assets/` folder to the **root** of the repository. (Do not upload only the ZIP.)
3. In repository **Settings → Pages**, select **Deploy from a branch**, branch **main**, folder **/(root)**, and save.
4. Open the `https://YOUR-USERNAME.github.io/the-cut/` address GitHub shows. On your iPhone, use Safari's Share menu → **Add to Home Screen**.

The installable web app caches its code and catalogue for use offline after its first successful load.

## What's inside

- **260 curated titles:** 157 films and 103 TV programmes, each with its own short synopsis and a hand-written, personalised justification. A small number are negative preference references, clearly flagged.
- Separate Film and TV exploration, genre / mood / collection filters, full-text search, favourites and essential / wildcard categories.
- A three-choice **Tonight** picker using your mood, preferred effort, format and company.
- A genuine personal **Library**, separate from the larger discovery catalogue.
- Statuses for *Want to watch, Watching, Watched / finished, Seen (completion unknown), Sampled / tried, Paused, Dropped, Not continuing, Not interested*.
- Ratings: *Loved / Liked / Alright / Disliked / Unrated*.
- Optional progress and a reason for stopping a show, plus a **free-text private comment on every title**. Add unlimited context about why something worked or didn't.
- Ability to add any missing film or show, and edit its synopsis / reason.
- Simple taste-aware ranking that adjusts to your ratings. This happens in your browser, not via an external AI service.
- Subscription preferences for Netflix, Prime Video, Disney+, NOW, BBC iPlayer and Apple TV.

## Your preloaded viewing history

We've brought in your explicit reactions, including the ten most recent ratings, your favourite movies and series, the 15 remaining recommendations from the earlier sample, BoJack Horseman and Slow Horses as **Paused**, and Fargo as **Not continuing (season one complete)**.

We **do not assume** that enjoying a TV programme means you finished every season; those are saved as **Seen (completion unknown)** unless you confirmed otherwise. That distinction is preserved in exports.

## Export your data to ChatGPT

Open **My library → Export data**, or **My taste → Export your profile**, or use **Export & back up** on desktop.

- **ChatGPT update (.md)**: a human-readable report of *every title you've rated, watched, sampled, paused, dropped or wishlisted*, plus ratings, season progress, reasons for stopping and your complete comments. Upload the file to ChatGPT or copy its contents using **Copy ChatGPT update**. This is the best format for improving your recommendations.
- **Full data backup (.json)**: your records **and** every curated title with synopsis and justification, plus custom titles, profile notes, streaming preferences and timestamps. This is the definitive backup and can be imported later.
- **Import previous backup**: imports a prior `the-cut-full-backup-*.json` and merges those records into the current app. Your other local records aren't wiped just because they aren't present in the imported file.

If you use two devices, export on one, import on the other. There is no automatic cross-device synchronisation in this version.

**Make backups** periodically. All records are stored in the browser's `localStorage`; clearing site data or using an unstable private/file preview can erase local changes.

## Where to watch

Each title includes **Where to watch in the UK**, which opens a JustWatch search. JustWatch can show current provider offers. The app does **not** call a live streaming API, so it does **not** claim that a title is currently included in any of your subscriptions or give unverified rental prices. This would require a reliable licensed or authenticated availability feed.

## Poster imagery and privacy

The design uses distinctive, procedurally styled typographic covers rather than externally hotlinked copyrighted posters. No tracking pixels, login, analytics, account, server database or paid API keys.

For an ongoing personal app, use the GitHub Pages build and keep a copy of the JSON export. Everything can be rebuilt or migrated from that file.
