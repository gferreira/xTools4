---
title     : curvature visualizer
menutitle : curvature
layout    : page
permalink : /reference/tools/glyph/show-curvature/
---

Visualize the curvature along curve segments.
{: .lead }

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/glyph/curvature.png){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
display color
: choose a color for the curvature preview

scale
: the scale of the curvature measurements at each step

steps
: number of measurement steps along each curve segment

show preview
: turn the visualisation on / off

selection only
: show visualisation only for selected segments
</div>

</div>


Preview
-------

![]({{ site.url }}/images/glyph/curvature_preview.png){: .img-fluid}


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Does not work correctly with quadratic contours yet.
{: .card-text }
</div>
</div>
