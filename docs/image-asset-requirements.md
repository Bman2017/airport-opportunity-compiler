# Airport Image Asset Requirements

The production viewer must not depend on a low-resolution embedded placeholder.

## Required renditions

- `assets/airport-reference-3840.webp` — primary desktop source, approximately 3840×2160.
- `assets/airport-reference-1920.webp` — standard desktop source.
- `assets/airport-reference-1280.webp` — tablet and constrained-network source.
- `assets/airport-reference-960.webp` — mobile fallback.
- Optional AVIF equivalents when supported.

## Rules

- Preserve one canonical aspect ratio across renditions.
- Use the exact same composition for every rendition so normalized annotations remain valid.
- Do not embed raster data inside SVG for production.
- Do not blur, stretch, crop, or independently regenerate a rendition.
- Record source generation, approval, dimensions, checksum, version, and rights status.
- Annotation geometry must reference the visual asset version.

## Viewer behavior

Use a responsive `picture` element and choose the smallest rendition that preserves the required display quality. The hotspot overlay must share the same containing block and aspect ratio as the selected image.
