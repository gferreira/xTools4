---
title     : interpolation preview
menutitle : interpolation
layout    : page
permalink : /reference/dialogs/glyph/interpolation-preview
---

Preview interpolation steps with another font.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyph/interpolation.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
master
: font and layer to be used as second master

steps
: the number of interpolated steps between the masters

preview color
: choose a color for the interpolation preview

show lines
: display trails connecting point location across masters

show steps
: display intermediate interpolation steps

preview
: turn the visualisation on/off

starting point
: move start of selected contours to the previous / next point

contour index
: move index of selected contours up / down
</div>

</div>


preview
-------

![]({{"images/glyph/interpolation_preview.png" | relative_url }}){: .img-fluid}


incompatible glyphs
-------------------

If the two master glyphs are incompatible, an error report is displayed in the background.

![]({{"images/glyph/interpolation_error.png" | relative_url }}){: .img-fluid}


- - -

see also [glyphs > interpolate masters](../../../glyphs/interpolation/interpolate/)
