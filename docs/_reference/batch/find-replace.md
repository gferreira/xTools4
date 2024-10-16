---
title     : batch find & replace
layout    : page
permalink : /reference/tools/batch/find-replace/
---

Find and replace font data in the selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


find & replace
--------------

find
: A string of text to find.

replace
: A string of text to replace the found string.


fonts
-----

Select on which fonts to find & replace data.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchFindReplace_0.png" | relative_url }}){: .img-fluid}
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


font info
-----

Find and replace text in the selected font info attributes.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchFindReplace_1.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
font info attributes
: select which font info attributes to use in the search

select all
: select all attributes in the list

find & replace
: find and replace strings in all selected fonts

preflight
: simulate the action before applying it
</div>

</div>

{% comment %}
consider adding support for find & replace in other places:

- glyph names
- OpenType features
- groups
- components
{% endcomment %}

