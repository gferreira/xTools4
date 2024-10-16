---
title     : set margins
layout    : page
permalink : /reference/tools/glyphs/metrics/set-margins
---

Set left / right margins in the selected glyphs.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/marginsSet.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
left / right
: values for left and right margins

operators
: how the value is used to calculate the margin

use beam
: optionally measure margins using the beam

y beam
: vertical position of the beam

apply
: set margins in the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Supports setting margins in multiple layers using the [layers] selector.
{: .card-text }
</div>
</div>

[layers]: ../../modifiers/layers/


Preview
-------

![]({{"images/glyphs/marginsSet_preview.png" | relative_url }}){: .img-fluid}
