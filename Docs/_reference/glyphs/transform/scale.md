---
title  : Scale
layout : page
---

Scale the selected glyphs.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/scale.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
origin
: origin point of the transformation

factor
: the scaling factor

dimensions
: choose between proportional, horizontal or vertical scaling

sidebearings
: scale left and right margins too

vertical metrics
: scale the font’s vertical metrics

apply
: scale the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


<div class="card bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Supports scaling multiple layers using the [layers] selector.
{: .card-text }
</div>
</div>

[layers]: ../../modifiers/layers/


Preview
-------

![]({{"images/glyphs/scale_preview.png" | relative_url }}){: .img-fluid}


{% comment %}
- add a second input field for the y-factor (like the [interpolate masters](../../interpolation/interpolate/) dialog)
{% endcomment %}
