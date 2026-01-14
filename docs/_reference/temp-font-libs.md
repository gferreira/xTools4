---
title     : Custom libs in temporary fonts
layout    : default
permalink : /reference/temp-font-libs/
---

<style>
    td:nth-child(1) { width: 140px; }
</style>

Custom data to make temporary fonts interoperable with other tools.
{: .lead}

* Table of Contents
{:toc}

### Temp edit mode

| lib key    | `com.xTools4.tempEdit.mode` |
| lib value  | Import mode of the temporary font: `fonts`, `glyphs` or `layers`. |
| lib level  | font |
| created by | [TempEdit], [GlyphMeme], [GlyphTuning] |
| used by    | [TempEdit], [GlyphMeme], [GlyphTuning], [GlyphValidator], [VarGlyphViewer], [ImportLayer] |
{: .table }

### Glyphset path

| lib key    | `com.xTools4.tempEdit.glyphSetPath` |
| lib value  | Path of the UFO glyph set from which a glyph came from and must return to. |
| lib level  | glyph |
| created by | [TempEdit], [GlyphMeme], [GlyphTuning] |
| used by    | [TempEdit], [GlyphMeme], [GlyphTuning] |
{: .table }

### Font measurements

| lib key      | `com.xTools4.measurements.font` |
| lib value    | A dictionary with the font-level measurements for a glyph’s font. |
| lib level    | glyph |
| created by   | [GlyphMeme] |
| used by      | [Measurements] |
{: .table }

### Default measurements

| lib key      | `com.xTools4.measurements.default` |
| lib value    | A dictionary with the glyph-level measurements of the default glyph. |
| lib level    | glyph |
| created by   | [GlyphMeme] |
| used by      | [Measurements] |
{: .table }

[temporary fonts]: ../../explanations/temp-fonts/

[TempEdit]: ../tools/variable/temp-edit/
[GlyphMeme]: ../tools/variable/glyph-meme/
[GlyphTuning]: ../tools/variable/glyph-tuning/
[GlyphValidator]: ../tools/variable/glyph-validator/
[VarGlyphViewer]: ../tools/variable/varglyph-viewer/
[ImportLayer]: ../tools/glyphs/layers/import/
[Measurements]: ../tools/variable/measurements/