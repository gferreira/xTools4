---
title     : interpolation preview
menutitle : interpolation
layout    : page
permalink : /reference/tools/glyph/interpolation-preview/
---

Preview interpolation steps with another font, layer and / or glyph.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/glyph/interpolation.png){: .img-fluid}
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

![]({{ site.url }}/images/glyph/interpolation_preview.png){: .img-fluid}


Errors
------

If the two master glyphs are incompatible, an error report is displayed in the background.

![]({{ site.url }}/images/glyph/interpolation_error.png){: .img-fluid}


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header">see also</div>
<div class="card-body" markdown='1'>
[glyphs > interpolate](../../dialogs/glyphs/interpolation/interpolate/)
{: .card-text }
</div>
</div>
