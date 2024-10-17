---
title     : rotate
layout    : page
permalink : /reference/tools/glyphs/transform/rotate/
---

Rotate selected glyphs.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/glyphs/rotate.png){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
origin
: origin point of the transformation

angle
: the angle of rotation in degrees

apply
: rotate the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Supports rotating multiple layers using the [layers] selector.
{: .card-text }
</div>
</div>

[layers]: ../../modifiers/layers/


Preview
-------

![]({{"images/glyphs/rotate_preview.png" | relative_url }}){: .img-fluid}
