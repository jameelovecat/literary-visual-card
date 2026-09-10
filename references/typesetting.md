# Typesetting and Renderer

Use `scripts/render_card.py` after the text-free artwork is approved. It produces a deterministic `1600 × 2000 px` PNG and uses the bundled Source Han Serif SC and Source Serif 4 fonts.

## Input specification

Create a UTF-8 JSON file:

```json
{
  "background": "/absolute/path/background.png",
  "output": "/absolute/path/final-card.png",
  "content_type": "poetry",
  "title": "标题",
  "text": "第一行\n第二行",
  "attribution": "作者｜《书名》",
  "credit": ""
}
```

Required fields:

- `background`: absolute path to the text-free artwork.
- `output`: absolute output path ending in `.png`.
- `text`: exact selected excerpt.

Optional fields:

- `content_type`: `poetry` or `prose`; defaults to `prose`.
- `title`: omit or use an empty string for a titleless card.
- `decorate_title`: defaults to `true`; adds `《》` only when a title exists and is not already enclosed.
- `attribution`: a string or list of lines. Omit it when the user supplied no attribution. The renderer then omits the divider automatically.
- `credit`: defaults to an empty string. Omit it unless the user explicitly requests a credit; when requested, reproduce the supplied wording exactly.
- `text_width`: defaults to `930`; supported range is `500–1300`.
- `readability_field`: left-side darkening from `0` to `1`; defaults to `0.22`.
- `text_color` and `secondary_text_color`: hexadecimal colors such as `#F4F1E7`.

## Contrast workflow

Choose text colors only after inspecting the finished background; do not reuse one preset's colors mechanically on another image.

1. Identify the complete title and body footprint on the actual background, including every line and stanza gap—not merely the upper-left corner.
2. Use warm off-white ink over a consistently dark field and dark charcoal or chromatic ink over a consistently light field. Avoid placing one text block across alternating light and dark bands.
3. Render once, inspect at full size and at a reduced phone-like preview, and check every line independently. A successful script exit does not mean the card is readable.
4. If contrast is weak, first change `text_color` and `secondary_text_color`; next apply the smallest useful `readability_field`. Do not use a heavy overlay to conceal a poorly composed background.
5. If the same text block crosses incompatible values and no single ink remains clear, revise or regenerate the background so the typography zone becomes calmer and more consistent. This is mandatory before delivery.

Reject clipped, low-contrast, shimmering, or texture-obscured text. Typography must be comfortably readable without zooming and must remain distinct from halftone, foliage, brushwork, projected shadows, or bright paper scars behind it.

## Content rules

- Poetry preserves every supplied line and blank stanza break. If it cannot fit at `34–40 px`, select a shorter excerpt or revise the artwork’s text area; do not change its lineation.
- Prose may wrap visually at punctuation or character boundaries. Visual wrapping must not change wording, punctuation, or sentence order.
- A missing title moves the body upward to the title position.
- A missing attribution removes both the attribution and divider.
- For mixed Chinese and Latin text, the renderer switches between Source Han Serif SC and Source Serif 4 character by character.

## Attribution formatting

Format only metadata explicitly supplied by the user:

- Author only: `作者`
- Author and book: `作者｜《书名》`
- Author and article: `作者｜〈文章名〉`
- Multiple useful fields: pass a list to create two restrained lines.

Do not add missing-field labels or placeholders.

## Run

```bash
python3 /path/to/literary-visual-card/scripts/render_card.py /path/to/card.json
```

Inspect the PNG at full size after rendering. The script checks dimensions and fit but cannot judge whether the artwork competes visually with the text.
