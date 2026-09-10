#!/usr/bin/env python3
"""Render a deterministic 1600×2000 text card from a JSON specification."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


W, H = 1600, 2000
SAFE = 150
DEFAULT_TEXT_WIDTH = 930
SKILL_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = SKILL_ROOT / "assets" / "fonts"
CJK_PATH = FONT_DIR / "SourceHanSerifSC-Regular.otf"
LATIN_PATH = FONT_DIR / "SourceSerif4-Regular.otf"
BREAK_AFTER = set("，。！？；：、,.!?;:）)]}》〉」』—… ")


def parse_color(value, default):
    if not value:
        return default
    value = value.lstrip("#")
    if len(value) not in (6, 8):
        raise ValueError(f"Invalid color: {value}")
    parts = tuple(int(value[i : i + 2], 16) for i in range(0, len(value), 2))
    return parts if len(parts) == 4 else (*parts, 255)


def cover(image):
    image = image.convert("RGB")
    scale = max(W / image.width, H / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (image.width - W) // 2
    top = (image.height - H) // 2
    return image.crop((left, top, left + W, top + H))


def add_readability_field(image, opacity):
    if opacity <= 0:
        return image.convert("RGBA")
    opacity = max(0.0, min(1.0, opacity))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = overlay.load()
    peak = round(255 * opacity)
    for x in range(W):
        alpha = peak if x <= 900 else max(0, round(peak * (1280 - x) / 380))
        for y in range(H):
            pixels[x, y] = (8, 10, 12, alpha)
    return Image.alpha_composite(
        image.convert("RGBA"), overlay.filter(ImageFilter.GaussianBlur(18))
    )


def is_latin(char):
    return ord(char) < 128 and (char.isalpha() or char.isdigit())


def fonts(size):
    return (
        ImageFont.truetype(str(CJK_PATH), size),
        ImageFont.truetype(str(LATIN_PATH), size),
    )


def font_for(char, cjk_font, latin_font):
    return latin_font if is_latin(char) else cjk_font


def tracking_width(draw, text, cjk_font, latin_font, tracking):
    if not text:
        return 0
    widths = [
        draw.textlength(char, font=font_for(char, cjk_font, latin_font))
        for char in text
    ]
    return sum(widths) + tracking * (len(text) - 1)


def draw_tracking(draw, x, y, text, cjk_font, latin_font, fill, tracking):
    for char in text:
        font = font_for(char, cjk_font, latin_font)
        draw.text((x, y), char, font=font, fill=fill)
        x += draw.textlength(char, font=font) + tracking


def wrap_one(draw, text, cjk_font, latin_font, tracking, max_width):
    if not text:
        return [""]
    lines = []
    remaining = text
    while remaining:
        fit = 0
        last_break = 0
        for index, char in enumerate(remaining, start=1):
            if tracking_width(draw, remaining[:index], cjk_font, latin_font, tracking) > max_width:
                break
            fit = index
            if char in BREAK_AFTER:
                last_break = index
        if fit == len(remaining):
            lines.append(remaining)
            break
        if fit == 0:
            raise ValueError("A character cannot fit inside the configured text width.")
        cut = last_break if last_break >= max(1, fit // 2) else fit
        lines.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    return lines


def layout_lines(draw, text, content_type, cjk_font, latin_font, tracking, max_width):
    source_lines = text.splitlines()
    if not source_lines:
        return []
    if content_type == "poetry":
        too_wide = [
            line
            for line in source_lines
            if tracking_width(draw, line, cjk_font, latin_font, tracking) > max_width
        ]
        if too_wide:
            raise ValueError(f"Poetry line exceeds text width: {too_wide[0]}")
        return source_lines

    result = []
    for source_line in source_lines:
        if not source_line.strip():
            if result and result[-1] != "":
                result.append("")
            continue
        result.extend(
            wrap_one(draw, source_line.strip(), cjk_font, latin_font, tracking, max_width)
        )
    return result


def block_height(lines, line_step, paragraph_gap):
    return sum(paragraph_gap if line == "" else line_step for line in lines)


def fit_body(draw, text, content_type, max_width, start_y, attribution_lines):
    reserved = 128 + 46 * attribution_lines if attribution_lines else 20
    bottom = H - SAFE - reserved
    for size in range(40, 33, -1):
        cjk_font, latin_font = fonts(size)
        tracking = max(4, round(7 * size / 40))
        line_step = round(66 * size / 40)
        paragraph_gap = round(38 * size / 40)
        try:
            lines = layout_lines(
                draw, text, content_type, cjk_font, latin_font, tracking, max_width
            )
        except ValueError:
            continue
        if start_y + block_height(lines, line_step, paragraph_gap) <= bottom:
            return lines, cjk_font, latin_font, tracking, line_step, paragraph_gap
    raise ValueError("Text does not fit. Select a shorter excerpt or increase text_width.")


def title_fonts(draw, title, max_width):
    for size in range(68, 53, -1):
        cjk_font, latin_font = fonts(size)
        tracking = max(5, round(7 * size / 68))
        if tracking_width(draw, title, cjk_font, latin_font, tracking) <= max_width:
            return cjk_font, latin_font, tracking
    raise ValueError("Title does not fit. Shorten the title.")


def normalized_title(title, decorate):
    title = title.strip()
    if not title or not decorate:
        return title
    if title.startswith("《") and title.endswith("》"):
        return title
    return f"《{title}》"


def render(spec):
    background = Path(spec["background"]).expanduser().resolve()
    output = Path(spec["output"]).expanduser().resolve()
    content_type = spec.get("content_type", "prose")
    if content_type not in {"poetry", "prose"}:
        raise ValueError("content_type must be 'poetry' or 'prose'.")
    text = spec["text"].strip("\n")
    if not text:
        raise ValueError("text cannot be empty.")

    title = normalized_title(spec.get("title", ""), spec.get("decorate_title", True))
    attribution = spec.get("attribution", "")
    if isinstance(attribution, list):
        attribution = "\n".join(str(item) for item in attribution if str(item).strip())
    attribution = str(attribution).strip()
    credit = str(spec.get("credit", "") or "").strip()
    text_width = int(spec.get("text_width", DEFAULT_TEXT_WIDTH))
    if not 500 <= text_width <= W - SAFE * 2:
        raise ValueError("text_width must be between 500 and 1300.")

    image = add_readability_field(
        cover(Image.open(background)), float(spec.get("readability_field", 0.22))
    )
    draw = ImageDraw.Draw(image)
    ink = parse_color(spec.get("text_color"), (244, 241, 231, 244))
    muted = parse_color(spec.get("secondary_text_color"), (235, 232, 222, 220))
    x = SAFE

    if title:
        title_cjk, title_latin, title_tracking = title_fonts(draw, title, text_width)
        draw_tracking(
            draw, x, 620, title, title_cjk, title_latin, ink, title_tracking
        )
        text_y = 805
    else:
        text_y = 620

    attribution_lines = len(attribution.splitlines()) if attribution else 0
    lines, body_cjk, body_latin, tracking, line_step, paragraph_gap = fit_body(
        draw, text, content_type, text_width, text_y, attribution_lines
    )
    y = text_y
    for line in lines:
        if line == "":
            y += paragraph_gap
            continue
        draw_tracking(draw, x, y, line, body_cjk, body_latin, ink, tracking)
        y += line_step

    if attribution:
        y += 54
        draw.line((x, y, x + 60, y), fill=muted, width=2)
        y += 54
        attr_cjk, attr_latin = fonts(28)
        for line in attribution.splitlines():
            if tracking_width(draw, line, attr_cjk, attr_latin, 3) > text_width:
                raise ValueError("Attribution does not fit. Shorten or split it.")
            draw_tracking(draw, x, y, line, attr_cjk, attr_latin, muted, 3)
            y += 46

    if credit:
        _, credit_font = fonts(20)
        width = draw.textlength(credit, font=credit_font)
        draw.text(
            (W - SAFE - width, H - SAFE - 20),
            credit,
            font=credit_font,
            fill=muted,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, format="PNG", optimize=True)
    if Image.open(output).size != (W, H):
        raise AssertionError("Output dimensions are not 1600×2000.")
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", help="Path to a UTF-8 JSON specification")
    args = parser.parse_args()
    spec_path = Path(args.spec).expanduser().resolve()
    with spec_path.open(encoding="utf-8") as handle:
        spec = json.load(handle)
    print(render(spec))


if __name__ == "__main__":
    main()
