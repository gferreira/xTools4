---
title     : Custom designspace libs
layout    : default
permalink : /reference/custom-designspace-libs/
---

<style>
    td:nth-child(1) { width: 140px; }
</style>

Additional data formats linked to designspace files and used by different tools for variable fonts.
{: .lead}

### Measurements 

| lib key       | `com.xTools4.xProject.measurementsPath` |
| lib value     | name of the measurements file (in the same folder as the designspace) |
| linked format | [Measurements format] | 
| used by       | [Measurements], [GlyphMeme], [VarFontAssistant], [VarGlyphAssistant] |
{: .table }

### Glyph Constructions

| lib key       | `com.xTools4.xProject.glyphConstructionsPath` |
| lib value     | name of the glyph construction file (in the same folder as the designspace) | 
| linked format | [GlyphConstruction] | 
| used by       | [GlyphMeme] | 
{: .table }

### Glyph Groups (Smart Sets)

| lib key       | `com.xTools4.xProject.smartSetsPath` |
| lib value     | name of the smart sets file (in the same folder as the designspace) | 
| linked format | [Smart Sets] | 
| used by       | [GlyphMeme] | 
{: .table }

[Measurements format]: ../measurements-format/
[GlyphConstruction]: http://github.com/typemytype/GlyphConstruction
[Smart Sets]: http://robofont.com/documentation/topics/smartsets/
[Measurements]: ../tools/variable/measurements/
[GlyphMeme]: ../tools/variable/glyph-meme/
[VarFontAssistant]: ../tools/variable/varfont-assistant/
[VarGlyphAssistant]: ../tools/variable/varglyph-assistant/
