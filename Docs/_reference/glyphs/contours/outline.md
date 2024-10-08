---
title     : outline
layout    : page
permalink : /reference/dialogs/glyphs/contours/outline
---

Expand glyph contours outwards and/or inwards by a given offset distance.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/outline.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
source layer
: layer containing the source glyph contours

target layer
: layer where the resulting outlined contours will be drawn

stroke
: total width of the applied stroke

join style
: style of the stroke joins: square, round, or bevel

cap style
: style of the stroke caps: square, round, or butt

edges
: choose whether to expand contours inwards and/or outwards

apply
: expand outlines in the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


preview
-------

![]({{"images/glyphs/outline_preview.png" | relative_url }}){: .img-fluid}

[Outliner]: http://github.com/typemytype/outlinerRoboFontExtension


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
This dialog is a simple wrapper around the stroke expansion functions from the [Outliner] extension.
{: .card-text }
</div>
</div>
