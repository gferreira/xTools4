---
title     : batch glyph actions
layout    : page
permalink : /reference/tools/batch/glyph-actions
---

Apply glyph-level actions to selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


fonts
-----

Select on which fonts the actions should be applied.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchActions_0.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
target fonts
: a list of open and/or closed fonts for selection

add all open fonts
: add all open fonts to the list

select all
: select all fonts in the list

add fonts folder
: add a folder with UFOs to the list

clear font lists
: empties the list of fonts
</div>

</div>


glyphs
------

Select on which glyphs the actions should be applied.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchActions_1.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyph selection
: define how the target glyphs are chosen

mark glyphs
: ^
  apply a mark color to the transformed glyphs  
  click on the button to choose a color
</div>

</div>


actions
-------

Select and apply actions.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchActions_2.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
actions list
: select which actions to apply

drag actions to reorder
: drag the list items to change their order

PostScript / TrueType
: affects only *correct contour direction*

apply
: apply the selected actions to the selected glyphs

preflight
: simulate the actions before applying
</div>

</div>


{% comment %}
- add a new section with *transform* actions (move, scale, skew, rotate, etc.)
{% endcomment %}
