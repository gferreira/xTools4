---
title     : batch set data
layout    : page
permalink : /reference/tools/batch/set-data/
---

Set data in all selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


fonts
-----

Select on which fonts to set data.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSet_0.png" | relative_url }}){: .img-fluid}
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
---------

Set data in the selected font info attributes.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSet_1.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import info from UFO
: import font info values from a UFO font

import info from JSON
: import font info values from a `.json` file

font info attributes
: edit and select font info values in the list

select all
: select all attributes in the list

export to JSON
: save selected font info values to a `.json` file

apply selected info
: apply selected font info values to selected fonts

preflight
: simulate the action before applying it
</div>

</div>


glyph set
---------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSet_2.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import glyph set
: import glyph set from `.enc` file

glyph set
: edit glyph set as a space-separated list

export glyph set
: export glyph set to `.enc` file

create missing glyphs
: create glyphs if they don’t exist in the font

delete remaining glyphs
: delete all glyphs which are not in the glyph set

apply glyph set
: apply the glyph set to the selected fonts

preflight
: simulate the action before applying it
</div>

</div>


unicodes
--------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSet_3.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import unicodes
: import additional unicode mapping from `.uni` file

unicode mappings
: edit and select glyph name to unicode mappings

select all
: select all unicodes in the list

clear existing unicodes
: remove all unicode values in the font first

set unicodes
: set selected unicodes in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

data formats (examples)
-----------------------

### glyphset.enc

```plaintext
space
a
b
c
d
A
B
C
D
zero
one
two
three
```

see also [font > set glyph order](../../font/set-glyph-order/)

### fontinfo.json

```json
{
  "familyName": "Publica",
  "unitsPerEm": 1000,
  "xHeight": 500,
  "ascender": 680,
  "descender": -150,
  "capHeight": 680,
  "openTypeNameDesigner": "Gustavo Ferreira",
  "openTypeOS2WidthClass": 5
}
```

### unicodes.uni

```plaintext
2190 arrowleft
2191 arrowup
2192 arrowright
2193 arrowdown
2194 arrowleftright
2195 arrowupdown
2196 arrowupleft
2197 arrowupright
2198 arrowdownright
2199 arrowdownleft
```
