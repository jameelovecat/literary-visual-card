---
name: literary-visual-card
description: Create 4:5 visual cards for literary and reflective text—including poems, reading quotes, book excerpts, article passages, aphorisms, and original short prose—by selecting a shareable verbatim excerpt, applying one of four established visual styles, and typesetting it with a consistent editorial system. Do not use for instructional, business, or data-heavy information cards.
---

# Literary Visual Card Skill

Create finished text cards from literary or reflective writing while preserving the source wording and keeping artwork, typography, and attribution independently editable.

## Select the excerpt

When the user supplies a poem, article, transcript, book passage, or group of texts without choosing an excerpt, select the strongest excerpt directly. Do not pause for excerpt approval by default.

Rank candidates by standalone clarity, emotional tension, memorability, reader identification, and concise shareability. Prefer one contiguous passage of roughly 2–7 source lines. For prose, choose one compact paragraph or 2–4 adjacent sentences. For batches, normally choose one excerpt per source item. A short complete work may be used in full when its internal contrast would be lost by excerpting and it fits comfortably.

Preserve selected wording, characters, punctuation, stanza breaks, and sentence order exactly. Never rewrite, polish, correct, translate, or join non-adjacent fragments. Preserve authorial line breaks for poetry. For prose, permit visual line wrapping at punctuation or natural reading boundaries without altering the text. State the selected excerpt when delivering the result.

Use a supplied title exactly. When no title is supplied, default to a titleless card and move the body upward to preserve balance. Create a title only when the user explicitly asks for one; never make a generated editorial title look like source metadata.

## Handle attribution

Treat attribution as optional metadata, not required copy.

- Show an author, creator name, book title, article title, or source only when the user explicitly supplies it or explicitly asks for it to be included.
- Never assume the text belongs to Jamee or to the current user. Never infer or invent an author or source from memory.
- Use only the metadata provided. Do not add placeholders such as `出处待补`, `出处待考`, `未知作者`, or `佚名`.
- When no attribution metadata is supplied, omit both the attribution and its divider so the card is publication-ready without a removal step.
- When only partial metadata is supplied, display only that information cleanly; do not call attention to missing fields.
- Search for attribution only when the user asks. Include found metadata only when a reliable source verifies it; otherwise omit it.

## Interpret the source

Before choosing or applying a style, identify both the source text's semantic core and its visual world. Read the entire supplied source even when only a short excerpt will appear on the card. Build the image through two linked decisions: the whole source establishes the world; the selected excerpt establishes the visual hook.

- From the whole source, extract the central emotional action, tension, atmosphere, and visual world. These determine the image's overall setting, emotional direction, and internal conflict; the literal picture is not automatically invariant across styles.
- From the selected excerpt, identify one arresting visual hook: a concrete moment, object, gesture, spatial contradiction, optical event, or uncanny relation that can make a viewer pause before reading. Give this hook a clear first-read position in the composition. It should sharpen the excerpt rather than merely decorate the larger mood.
- Require both layers to survive in the finished artwork. Reject a background that accurately matches the poem's atmosphere but lacks a memorable focal tension, and reject a striking subject that is detached from the whole poem's emotional world.
- Priority order is: explicit user direction, semantic core, selected style's own visual logic, decisive source imagery, then optional invention.
- Lock the concrete scene only when the user explicitly requests scene fidelity or when the setting, time, object, and physical action are themselves the point of the writing. In that case preserve decisive evidence such as `凌晨`, `黄昏`, `操场`, `垃圾桶`, `水管`, or `山脚` so it can be inferred without reading the copy.
- Otherwise allow each preset to interpret the same meaning through its strongest language: photography may stage a believable moment; crayon may reconstruct a private memory; screenprint may reduce the idea to one object and graphic relation; oil painting may transfer the emotion into landscape, light, and movement. Four styles do not need to depict an identical composition.
- A freer interpretation must still retain the text's emotional direction and must not contradict it, beautify away its conflict, or substitute a generic unrelated symbol.
- Add invented objects only when they sharpen the semantic core or strengthen the selected excerpt's visual hook without redirecting the source. Never illustrate every sentence or pile up symbols.

## Confirm the visual intention

Before discussing style, show one compact proposal containing the exact selected excerpt followed by a short visual-intention paragraph that combines the whole source's world with the excerpt's arresting hook. Ask the user to confirm or revise it. Do not split the world and hook into a long questionnaire or expose the full internal checklist. For batches, present all proposals together so the user can approve them in one response.

A style choice does not replace intention confirmation. Skip this confirmation only when the user explicitly says “直接做”, “不用确认”, or otherwise clearly delegates the excerpt and visual intention.

## Choose a visual style

After the visual intention is confirmed, ask the user to choose from the four established presets below. If the user already named a style, use it without asking again. If the user says “直接做”, “你来选”, or clearly delegates the style choice, recommend and use the best-fitting preset immediately, state the choice and reason in one short sentence, and do not pause. Do not invent another style or blend presets unless explicitly requested.

1. **时光蜡笔** — an adult world redrawn with a child’s awkward crayon grammar, combining dense scribbled charcoal, blunt color, naïve proportions, and real projected window light; raw, private, and quietly reborn.
2. **电影诗影** — realistic cinematic photography with deep-blue and warm-gold light, analog softness, and emotionally charged negative space.
3. **旧梦丝网** — modern flat graphic composition with one cleanly simplified subject, two or three spot colors, restrained geometric fields, coarse halftone, and tactile silkscreen wear.
4. **梵高油画** — expressive post-impressionist oil painting with rhythmic impasto, emotionally intensified natural color, and bright-melancholy tension.

When selecting automatically:

- Prefer **时光蜡笔** for renewal, childhood, vulnerability, growth, self-recognition, and emotionally mixed personal experience.
- Prefer **电影诗影** for atmosphere, memory, relationships, distance, longing, urban encounters, and visually concrete scenes.
- Prefer **旧梦丝网** for ordinary objects, labor, daily rituals, dry humor, gentle absurdity, cultural memory, and concise observational writing.
- Prefer **梵高油画** for nature, solitude, restless vitality, inner conflict, wandering, fatigue, renewal, and writing where the landscape carries the emotion.

Before generating, read [references/visual-styles.md](references/visual-styles.md) and use only the selected preset’s specification. Translate the confirmed intention through that preset's own visual language; the later style choice may change the literal scene construction but must preserve the approved world and visual hook.

Generate the artwork without lettering. Require no text, letters, numbers, handwriting, pseudo-writing, logos, labels, borders, frames, or watermarks. Inspect the background, then typeset all copy deterministically.

## Typeset with the bundled renderer

Read [references/typesetting.md](references/typesetting.md), prepare its small JSON specification, and use `scripts/render_card.py` instead of recreating layout code for each card. The renderer bundles the required fonts, preserves poetry lines, wraps prose without changing its wording, supports mixed Chinese and Latin text, omits empty title and attribution blocks, checks fit, and verifies output dimensions.

If the renderer reports that text cannot fit at the permitted sizes, select a shorter contiguous excerpt before asking the user to edit the source. Never compress, paraphrase, or silently remove text to make it fit.

## Locked canvas and typography

Final canvas is exactly `1600 × 2000 px`, vertical `4:5`. Keep every text element at least `140 px` from each edge.

| Element | Typeface | Size | Tracking | Position |
| --- | --- | ---: | ---: | --- |
| Chinese title | Source Han Serif SC Regular | `54–68 px` | proportional | `x=150`, `y=620`, when supplied |
| Chinese excerpt | Source Han Serif SC Regular | `34–40 px` | proportional | starts `x=150`, `y=805` with title; `y=620` without |
| Attribution | Source Han Serif SC Regular | `28 px` | `3 px` | after divider, only when supplied |
| Optional credit | Source Serif 4 Regular | `20 px` | default | bottom-right, only when requested |

- Excerpt line step: `66 px`.
- Extra stanza gap: `38 px`.
- When attribution is supplied, add `54 px` after the excerpt, then a thin `60 px` divider, then `54 px` before the attribution.
- When attribution is absent, end after the excerpt; do not draw the divider or reserve an empty attribution block.
- Information order: optional `《Title》`, excerpt, optional divider and attribution.
- Do not add a visual credit, AI label, watermark, or creator signature by default. Add a credit only when the user explicitly supplies or requests one; reproduce the requested wording exactly.
- Use warm off-white text rather than pure white. Adapt text color only when a light artwork area requires a darker ink for readable contrast.
- Add a subtle readability field only when required; preserve the artwork’s texture.

Use the bundled Source Han Serif SC for Chinese and Source Serif 4 for Latin text; switch fonts within a line for mixed-language copy. The font files are distributed under the included SIL Open Font License files. Do not silently substitute fonts. Keep the JSON specification, text-free background, and renderer output so later wording or placement changes do not require regenerating the artwork.

## Verify and deliver

Inspect every final card at full size after typesetting. Verify exact dimensions, source-faithful text, poetry lineation or prose wrapping, fixed typography, safe margins, supplied attribution only, user-requested credit only, and absence of accidental generated text. Treat readability as a release gate: title, every body line, attribution, and credit must remain comfortably legible across their actual background regions. If any line disappears into the artwork, first choose an appropriate light or dark ink, then add the smallest useful readability field; if contrast still varies across the block, regenerate or recompose the background's text zone rather than accepting the card. Never deliver a card merely because the renderer completed successfully.

Deliver final PNG files, identify the selected excerpt and visual preset, and include the editable source. For batches, provide a ZIP archive when useful.
