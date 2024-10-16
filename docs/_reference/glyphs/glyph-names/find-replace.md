---
title     : find & replace in glyph names
layout    : page
permalink : /reference/tools/glyphs/glyph-names/find-replace/
---

Find and replace strings in the names of selected glyphs.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/namesFindReplace.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
find string
: string to be found and replaced

replace string
: new string to be used in place of the found one

apply
: find and replace the given string in the names of selected glyphs

overwrite
: overwrite existing glyphs with the new name

duplicate
: rename glyphs as duplicates and keep original glyphs
</div>

</div>


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
This tool will be rewritten using `font.renameGlyph`, which adds options to also rename the glyph in *components*, *groups*, *kerning*, and *layers*.
{: .card-text }
</div>
</div>
