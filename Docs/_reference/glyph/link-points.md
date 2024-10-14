---
title     : linked points
layout    : page
permalink : /reference/dialogs/glyph/link-points
---

Create permanent links between pairs of points and show the distance or angle between them.
{: .lead }

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyph/links.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
length
: show the distance between linked points

angle
: show the angle between linked points

link
: create a new link from two selected points

unlink
: unlink selected points

display color
: choose the color of link captions and lines

caption size
: size of the caption font

projections
: display distance measurements as x / y projections

clear all
: clear all links in the current glyph

show preview
: turn the visualisation on / off
</div>

</div>


Preview
-------

![]({{"images/glyph/links_preview.png" | relative_url }})


{% comment %}

Implementation details
----------------------

Links are stored in each glyph's lib under the key `com.hipertipo.xTools4.dialogs.glyph.linkPoints`

Links are defined using the ID attribute of each point, so they remain in place even after the point structure changes.

{% endcomment %}


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header">see also</div>
<div class="card-body" markdown='1'>
[variable > measurements](../../dialogs/variable/measurements/)
{: .card-text }
</div>
</div>
