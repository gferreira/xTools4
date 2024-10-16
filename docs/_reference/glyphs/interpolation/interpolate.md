---
title     : interpolate glyphs
layout    : page
permalink : /reference/tools/glyphs/interpolation/interpolate/
---

Interpolate two fonts into the selected glyphs of the current font.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/interpolationMasters.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
master 1 / master 2
: two compatible master font layers

x factor / y factor
: horizontal / vertical interpolation factors

proportional
: keep x / y factors equal

interpolate
: interpolate master glyphs into selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


Preview
-------

![]({{"images/glyphs/interpolationMasters_preview.png" | relative_url }}){: .img-fluid}


<div class="card bg-light my-3 rounded-0">
<div class="card-header">see also</div>
<div class="card-body" markdown='1'>
[glyph > interpolation preview](../../../glyph/interpolation-preview/)
{: .card-text }
</div>
</div>
