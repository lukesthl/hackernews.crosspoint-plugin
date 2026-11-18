# Hackaday for CrossPoint

A [CrossPoint](https://github.com/crosspoint-reader/crosspoint-reader) SD-card plugin: browse and search [Hackaday](https://hackaday.com) on the reader and save articles as plain text.

The installable plugin is the `hackaday.crosspoint-plugin/` folder. Everything else in this repo is for development.

## How it works

The plugin is a single `device.json` and has no code:

- Lists and search come from Hackaday's public WordPress REST API (`/wp-json/wp/v2/posts`). Category lists filter by category ID; `_embed=author` supplies the author name, and `_fields` keeps each page small.
- Selecting a post downloads `https://r.jina.ai/<article-url>` (Jina Reader) to `/Hackaday/<title>.txt`. The `X-Target-Selector: #post-{id}` header keeps only the post's own `<article>` element, which drops the site menus, sidebar and comment thread; `X-Remove-Selector` drops the share widget and the category/tag footer.

## Try it on a reader

Needs CrossPoint 2.0 (release candidate or nightly) with Plugins enabled under Settings > Connectivity.

Copy the contents of `hackaday.crosspoint-plugin/` to `/.crosspoint/plugins/hackaday/` on the SD card, then open Home > Plugins > Hackaday.

## Check before a release

```bash
python3 tools/check.py
```

It validates the manifest and `device.json`, and calls each live API URL once. `--offline` skips the network checks.

## Publish to Plugin Hub

1. Push this repo to GitHub as a public repo and add the topic `crosspoint-plugin`.
2. Bump `version` in both `manifest.json` and `device.json`.
3. Publish a GitHub Release (not a draft or pre-release) tagged `v<version>`.

Plugin Hub picks it up on its next catalog refresh (every three hours).

## Not done yet

- HTML entities in titles. WordPress only exposes `title.rendered`, which is entity-encoded (`Won&#8217;t`), and the firmware's JSON catalog does not decode entities. Hackaday's RSS feed would decode cleanly through the `xml` browse format, but that format has no paging, search or lists.
- An optional Jina API key: anonymous Jina use is rate-limited per IP and can return an error body instead of the article.
- Comment threads.

## Credits

Based on the Hacker News CrossPoint plugin by lukestahl.

## License

[MIT](LICENSE)
