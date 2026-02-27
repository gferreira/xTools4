---
title     : build constructions
layout    : page
permalink : /reference/tools/glyphs/components/build-constructions/
---

Build selected glyphs from components using [Glyph Construction] language.
{: .lead }

[Glyph Construction]: http://github.com/typemytype/GlyphConstruction


<div class='row'>
<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/glyphs/buildConstructions.png){: .img-fluid}
</div>
<div class='col-sm-8' markdown='1'>
import…
: import constructions from `.glyphConstruction` file

reload
: Reload the previously selected designspace file.

preview color
: Choose a color for the glyph construction preview in the Glyph Editor.

validation
: Check if the glyph is equal or different to the glyph construction.

preview
: show a preview of the glyph construction

build
: build selected glyphs if a construction is available

composites
: Show only glyphs which include the selected glyph as a component.
</div>
</div>


Validation
----------

If validation is enabled, a letter `C` appears in the right side of the glyph cell of all composite glyphs for which there is a construction, indicating the glyph’s validation status.

<table class='table'>
<tr>
<td><span class='green'>green</span></td>
<td>the composite glyph is equal to its glyph construction output</td>
</tr>
<tr>
<td><span class='red'>red</span></td>
<td>the composite glyph is different from its glyph construction output</td>
</tr>
</table>

![]({{ site.url }}/images/glyphs/buildConstructions_validation.png){: .img-fluid}


Preview
-------

![]({{ site.url }}/images/glyphs/buildConstructions_preview.png){: .img-fluid}
