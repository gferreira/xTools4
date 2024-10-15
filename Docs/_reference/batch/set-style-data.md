---
title     : batch set style data
layout    : page
permalink : /reference/tools/batch/set-style-data
---

Set data for individual styles in selected fonts.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


fonts
-----

Select on which fonts to set data.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSetData_0.png" | relative_url }}){: .img-fluid}
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


style data
----------

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/batch/BatchSetData_1.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import style data
: import style data from JSON file

style data
: edit imported style data manually if needed

set data
: set style data in selected fonts

preflight
: simulate the action before applying it
</div>

</div>


data format (example)
---------------------

### style-data.json

```json
{

  "featuresDir"   : "feaFolder",
  "features"      : ["features.fea"],

  "15.ufo": {
    "features"         : ["15.fea"],
    "weight"           : 100,
    "width"            : 5,
    "blue zones"       : [-200, -190, -10, 0, 465, 475, 605, 615, 675, 685],
    "stems vertical"   : [70],
    "stems horizontal" : [60]
  }

}
```


<div class="card bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
- document cascading behavior of *features* and *blue zones*.
{: .card-text }
</div>
</div>
