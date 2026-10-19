# Social preview

The social preview is the image shown when someone shares the repository link in chat, on social media, or in a document. Without one, GitHub generates a card from the owner's avatar, the name, and the description.

## Specs

From [github-facts.md](shared/github-facts.md#repository-metadata):
- **Size:** 1280×640 px recommended, 640×320 px minimum.
- **Format:** PNG, JPG, or GIF, under 1 MB.
- **Transparency:** PNG transparency is supported, but transparent areas look different on light and dark backgrounds. Prefer a solid background.
- **Upload:** **Settings → General → Social preview → Edit → Upload an image**. GitHub documents only this UI path, with no API, so the user uploads it themselves.

## Brief

Give the user, or their designer, this brief filled in:

| Element | Content | Rule |
|---|---|---|
| Name | The repository or product name | The largest text, at least 72 px tall at 1280×640 |
| Tagline | The repository description, shortened to 4 to 10 words if needed | At least 36 px. One line, two at most. |
| Visual | A logo, icon, or one simple illustration of what it does | Not a full screenshot. It is unreadable at thumbnail size. |
| Owner mark (optional) | `github.com/OWNER/REPO` or the owner's logo | Small, in a corner |
| Background | A solid color or a subtle gradient | Contrast ratio of 4.5:1 or more against the text |

Layout rules:
- Keep important content inside a centered safe area, with about 80 px of margin on every side. Some platforms crop the edges.
- Use no more than about 12 words in total. People see it for a second, at small size.
- Use the project's existing brand colors when they exist. Otherwise pick one strong color and one neutral.
- Check that it reads at 320×160, about the size of a chat preview.

## SVG starter

[../templates/social-preview.svg](../templates/social-preview.svg) is a 1280×640 layout with a name, a tagline, a URL line, and a simple mark. Fill its `{{PLACEHOLDERS}}` and colors, then write the result to `.github/social-preview.svg` in the user's repository. The image does not need to be committed; keeping it in `.github/` just makes later edits easy.

Export to PNG with whichever tool is installed. Check with `command -v` first; do not install anything without approval.

```bash
# Inkscape
inkscape .github/social-preview.svg --export-type=png --export-filename=social-preview.png -w 1280 -h 640

# librsvg
rsvg-convert -w 1280 -h 640 .github/social-preview.svg -o social-preview.png

# Chrome or Chromium (headless)
google-chrome --headless --disable-gpu --hide-scrollbars --window-size=1280,640 \
  --screenshot=social-preview.png "file://$PWD/.github/social-preview.svg"
```

**Alternative without design tools:** [Socialify](https://github.com/wei/socialify) is an open-source service that generates a preview image from the repository's name, description, language, and stats. The user picks a theme on its site and downloads the PNG. It suits users who want a consistent card and no custom artwork.

The starter uses a system font stack, so the result depends on the fonts installed where it is exported. Open the PNG and check it before uploading. The file must be under 1 MB. A flat-color design exported as PNG usually is.
