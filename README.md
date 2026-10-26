# The Cut v4 — personal film & TV discovery

857 curated titles with unique synopses and personal justifications; 152 initial viewing records; ratings, comments, progress, full backups and ChatGPT-ready exports.

## What's new

- **One-tap Seen and Save** on every discovery card, with Undo. Tap Details for ratings, comments and season progress. Viewed titles leave Discover immediately (unless Hide seen & skipped is off).
- **Bulk mode**: Select multiple titles, then mark them seen in one action.
- **Cleaner mobile Discover**: search and curated routes first; extra filters are tucked behind Filters. No decorative star/green emoji.
- **Streaming information**: the card and details show subscription inclusion when UK offers have actually been checked. Never counts Prime/Amazon rentals or Apple rentals as included. All titles link to JustWatch UK for manual checking. A "Included on my subscriptions" filter unlocks once verified data is loaded.
- **Posters**: real TMDB posters show where an approved metadata snapshot provides them, with a well-designed typographic fallback otherwise.
- **Backward compatibility**: uses the original `the-cut-state-v1` browser storage key; no watch history, comments or status migrations are discarded.

## Install on GitHub Pages

1. Unzip and upload all project files, including hidden `.github/workflows/` and `scripts/`, to the root of your GitHub repository.
2. In GitHub, open **Settings → Pages** and select **Deploy from a branch**, `main`, `/ (root)`.
3. Open the HTTPS Pages URL, then add it to your iPhone Home Screen if desired.
4. **Export Full Backup (.json)** before upgrading an existing deployment. The app preserves local records on the same domain and browser. Import a backup when changing domains or devices.

Or open `THE-CUT-v4-standalone.html` in a normal desktop browser. Note that local `file://` browser storage support varies; hosting on GitHub Pages is more reliable and essential for automatic streaming updates.

## Set up verified UK streaming availability

To avoid presenting invented availability for 857 titles, The Cut ships with an **empty, honest** availability snapshot. All titles still have working *Check on JustWatch* links.

To populate cards with subscription providers, accurate TMDB posters and dated streaming data:

1. Apply for a free personal / non-commercial TMDB API read access token: https://www.themoviedb.org/settings/api . TMDB requires attribution and its terms apply.
2. In your GitHub repository, go to **Settings → Secrets and variables → Actions → New repository secret**, named **`TMDB_READ_TOKEN`**, and paste the *API Read Access Token*.
3. Go to **Actions → Refresh UK streaming listings → Run workflow**. The job checks the entire catalogue and commits `metadata.js`. It runs again each Sunday by default, provided GitHub continues running scheduled workflows for your repository.
4. Reload your GitHub Pages site once the workflow and Pages redeployment complete. Posters and confirmed provider badges appear; the *Included on my subscriptions* filter becomes available.

The token **never goes into the web page** or downloaded snapshots; only GitHub Actions uses it. Alternatively run `TMDB_READ_TOKEN=... python scripts/sync_tmdb.py` locally. Do not commit or share your API token.

**Precise interpretation:** `flatrate` means subscription availability. `rent` and `buy` offers do not qualify. Standalone Amazon/Apple rentals are excluded. Apple TV TMDB provider 350 is the subscription, NOT Apple TV Store ID 2. NOW movies/entertainment depend on membership; unless the entitlement is known, the app displays **"Listed on NOW · membership depends"**, not confirmed free viewing. TV series can have differing seasonal availability; check before watching. Providers may vary by ad-supported tier. Snapshots over 30 days old cease to count as confirmed inclusion.

TMDB provides the film and TV metadata and watch-provider feed (powered by JustWatch). **The Cut is not endorsed or certified by TMDB or JustWatch**. Attribution in the app and the provider data source applies.

## Your data and privacy

- The Cut stores viewing status, ratings, notes, progress, bookmarks and preferences in this browser's `localStorage`. It has no accounts and does not share your viewing history.
- **My library → Export data → ChatGPT update (.md)** makes a readable export with all tracked records and comments. Paste it into ChatGPT to update your profile.
- **Full data backup (.json)** preserves your personal records, custom titles and catalogue, for import on another browser/device.
- Your personal data is separate from streaming metadata and recommendation listings.
- The initial recommendations are editorial/rule-based, not live AI. Each title contains a bespoke synopsis and personal justification.

## Technical notes

Static HTML/CSS/vanilla JS, designed for offline catalogue use. `data.js` holds titles, `app.js` handles interaction, `metadata.js` is optional verified UK provider/poster snapshot. A GitHub Actions workflow securely refreshes metadata; Pages hosts the output. No mandatory npm toolchain or backend.
