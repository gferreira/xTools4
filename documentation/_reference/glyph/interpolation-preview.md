---
title     : interpolation preview
menutitle : interpolation
layout    : page
permalink : /reference/tools/glyph/interpolation-preview
---

Preview interpolation steps with another font, layer and / or glyph.
{: .lead }

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyph/interpolation.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
font
: font source for the other interpolation master

layer
: source layer in the selected master font

glyph name
: source glyph in the selected master font

steps
: the number of interpolation steps between the masters

preview color
: choose a color for the interpolation preview

show lines
: display trails connecting point positions of all instances

show steps
: display intermediate interpolation steps

show preview
: turn the visualisation on/off

starting point
: move start of selected contours to the previous / next point

contour index
: move index of selected contours up / down
</div>

</div>


Preview
-------

![]({{"images/glyph/interpolation_preview.png" | relative_url }}){: .img-fluid}


Errors
------

If the two master glyphs are incompatible, an error report is displayed in the background.

![]({{"images/glyph/interpolation_error.png" | relative_url }}){: .img-fluid}


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header">see also</div>
<div class="card-body" markdown='1'>
[glyphs > interpolate](../../dialogs/glyphs/interpolation/interpolate/)
{: .card-text }
</div>
</div>
