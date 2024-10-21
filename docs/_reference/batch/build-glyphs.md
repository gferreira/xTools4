---
title     : batch build glyphs
layout    : page
permalink : /reference/tools/batch/build-glyphs/
---

Create new glyphs in the selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


fonts
-----

Select on which fonts to build the glyphs.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_0.png){: .img-fluid}
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


new
---

Create new empty glyphs in the selected fonts.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_1.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyph names
: as a space-separated list

batch make glyphs
: build new glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
The default width for new glyphs is defined in RoboFont’s [Font Overview preferences].
{: .card-text }
</div>
</div>

[Font Overview preferences]: http://robofont.com/documentation/reference/workspace/preferences-window/font-overview/


constructions
-------------

Create new glyphs from glyph construction rules.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_2.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import constructions
: import constructions from a `.glyphConstruction` file

construction rules
: glyph definitions in [glyph construction] language

export constructions
: export constructions to a `.glyphConstruction` file

select glyphs
: select the new glyphs after they are created

mark glyphs
: ^
  apply a mark color to the new glyphs  
  click on the button to choose a color

batch build glyphs
: build the glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

[glyph construction]: http://github.com/typemytype/GlyphConstruction



duplicates
----------

Duplicate glyphs in the same font under new names.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_3.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
source and target names
: a list defining source and target names for duplicates

add current font selection
: populate the list based on the current font selection

import glyph names from file…
: import source and target glyph names from `.txt` file

add new entry
: add a new entry to the list

select all
: select all glyph names in the list

export glyph names to file…
: export current list to `.txt` file

overwrite existing glyphs
: if target glyph already exists, overwrite it

mark duplicates
: ^
  apply a mark color to the duplicate glyphs  
  click on the button to choose a color

preflight
: simulate the action before applying it
</div>

</div>


{% comment %}
- - -

> - add default width to *new* section
{: .todo }

{% endcomment %}
