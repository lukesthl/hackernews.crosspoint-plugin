# Hacker News for CrossPoint

A [CrossPoint](https://github.com/crosspoint-reader/crosspoint-reader) SD-card plugin: browse and search Hacker News on the reader and save linked articles as plain text.

The installable plugin is the `hackernews.crosspoint-plugin/` folder. Everything else in this repo is for development.

## How it works

The plugin is a single `device.json` and has no code:

- Story lists and search come from the [Algolia HN API](https://hn.algolia.com/api).
- Selecting a story downloads `https://r.jina.ai/<article-url>` (Jina Reader), which returns the article as plain text, to `/Hacker News/<title>.txt`.

## Try it on a reader

Needs CrossPoint 2.0 (release candidate or nightly) with Plugins enabled under Settings > Connectivity.

Copy the contents of `hackernews.crosspoint-plugin/` to `/.crosspoint/plugins/hackernews/` on the SD card, then open Home > Plugins > Hacker News.

## Check before a release

```bash
python3 tools/check.py
```

It validates the manifest and `device.json`, and calls each live API URL once.

## Publish to Plugin Hub

1. Push this repo to GitHub as a public repo and add the topic `crosspoint-plugin`.
2. Bump `version` in both `manifest.json` and `device.json`.
3. Publish a GitHub Release (not a draft or pre-release) tagged `v<version>`.

Plugin Hub picks it up on its next catalog refresh (every three hours).

## Not done yet

- Comment threads (needs a browser `plugin.js` or a small server to turn Algolia's JSON into text).
- Ask HN posts, which have no link to download.
- A check that skips pages that do not convert to readable text.

## License

[MIT](LICENSE)
