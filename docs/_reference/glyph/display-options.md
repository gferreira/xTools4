---
title     : display options
layout    : page
permalink : /reference/tools/glyph/display-options
---

A floating palette to quickly toggle the [display options] in the Glyph Editor.
{: .lead }

<span class="badge text-bg-danger rounded-0">RF3</span> RoboFont 3 code which does no longer work in RoboFont 4.  

[Display options]: http://www.robofont.com/documentation/reference/workspace/glyph-editor/display-options/#options


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyph/display-options.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
glyph
: ^
  - contour fill
  - contour stroke
  - glyph margins, vertical metrics 
  - anchor points
  - image

points
: ^
  - on-curve points
  - off-curve  points
  - point coordinates
  - point labels

indexes
: ^
  - point indexes
  - segment indexes
  - contour indexes
  - component indexes
  - anchor indexes

alignment
: ^
  - rulers
  - guidelines
  - grid
  - blues
  - family blues

info 
: ^
  - metrics info
  - measurement info
  - component info
  - image info

helpers
: ^
  - outline errors
  - curve lengths
  - bitmap preview
</div>

</div>


Preview
-------

<div id='__display-options' class="carousel slide carousel-dark carousel-fade my-4" data-bs-ride="carousel">

<div class="carousel-inner">
  <div class="carousel-item active">
    <img src='{{"images/glyph/display-options_preview_1.png" | relative_url }}' class="d-block w-100">
  </div>
  <div class="carousel-item">
    <img src='{{"images/glyph/display-options_preview_3.png" | relative_url }}' class="d-block w-100">
  </div>
  <div class="carousel-item">
    <img src='{{"images/glyph/display-options_preview_4.png" | relative_url }}' class="d-block w-100">
  </div>
  <div class="carousel-item">
    <img src='{{"images/glyph/display-options_preview_5.png" | relative_url }}' class="d-block w-100">
  </div>
  <div class="carousel-item">
    <img src='{{"images/glyph/display-options_preview_2.png" | relative_url }}' class="d-block w-100">
  </div>
</div>

<button class="carousel-control-prev" type="button" data-bs-target="#__display-options" data-bs-slide="prev">
<span class="carousel-control-prev-icon" aria-hidden="true"></span>
<span class="visually-hidden">Previous</span>
</button>
<button class="carousel-control-next" type="button" data-bs-target="#__display-options" data-bs-slide="next">
<span class="carousel-control-next-icon" aria-hidden="true"></span>
<span class="visually-hidden">Next</span>
</button>

</div>


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header"> note</div>
<div class="card-body" markdown='1'>
This tool will be rewritten and improved for RF4. The user will be able to store different combinations of display settings, and to quickly switch between them.
{: .card-text }
</div>
</div>
