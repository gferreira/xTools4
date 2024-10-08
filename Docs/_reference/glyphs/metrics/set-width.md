---
title     : set width
layout    : page
permalink : /reference/dialogs/glyphs/metrics/set-width
---

Set the advance width in selected glyphs.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/widthSet.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
width
: value for width adjustment

mode
: how the value will be applied to the width

position
: choose the positioning mode for the glyph’s contours

apply
: set width value in the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Supports setting widths in multiple layers using the [layers] selector.
{: .card-text }
</div>
</div>

[layers]: ../../modifiers/layers/


positioning modes
-----------------

<table class='table table-hover'>
<tr>
  <th>do not move</th>
  <td>keeps the glyph’s left margin unchanged, whitespace is added/removed in the right margin</td>
</tr>
<tr>
  <th>center glyph</th>
  <td>divides the glyph’s total whitespace equally between left and right margins</td>
</tr>
<tr>
  <th>split margins</th>
  <td>splits the added/removed whitespace equally between left and right margins</td>
</tr>
<tr>
  <th>relative split</th>
  <td>splits the added/removed whitespace proportionally between left and right margins</td>
</tr>
</table>


preview
-------

![]({{"images/glyphs/widthSet_preview.png" | relative_url }}){: .img-fluid}
