---
title     : batch copy data
layout    : page
permalink : /reference/dialogs/batch/copy-data
---

Copy data from one source font to all selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


fonts
-----

Select source and target fonts.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_0.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
source font
: select the source font from which to copy data

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


font info
---------

Copy the selected font info attributes from source font to all target fonts.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_1.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
select all
: select all attributes in all groups

attributes
: select/deselect font info attributes to copy

copy font info
: copy the selected font info attributes

preflight
: simulate the action before applying it
</div>

</div>


glyphs
------

Copy data from the source font to all target fonts.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_2.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyph selection
: define how the target glyphs are chosen

glyph data
: select which types of glyph data to copy

remove source glyphs
: delete the source glyphs after copying

clear target glyphs
: delete the target glyph’s contours before copying

select glyphs
: select glyphs after copying data

mark glyphs
: ^
  apply a mark color to the new glyphs  
  click on the button to choose a color

preflight
: simulate the action before applying it
</div>

</div>


kerning
-------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_3.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
copy kerning
: copy kerning data from the source font to the target fonts

clear target kerning
: delete the target font’s kerning before copying

preflight
: simulate the action before applying it
</div>

</div>


groups
------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_4.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
copy groups
: copy groups from the source font to all target fonts

clear target groups
: delete the target font’s groups before copying

group type
: select which types of group to copy

preflight
: simulate the action before applying it
</div>

</div>


features
--------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchCopy_5.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
copy features
: copy OpenType features from source to target fonts
</div>

</div>
