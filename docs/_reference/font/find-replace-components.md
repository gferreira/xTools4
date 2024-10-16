---
title     : find (and replace) components
layout    : page
permalink : /reference/tools/font/find-replace-components/
---

Find all components of a given glyph, and optionally replace it by another glyph.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/font/findComponents.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
find
: the name of the base glyph

references
: a list of glyphs which reference the base glyph

mark color
: choose a color to mark selected glyphs

mark
: apply mark color to selected glyphs in the list

new base glyph
: the name of a replacement base glyph

replace
: replace base glyph by new glyph in the selected glyphs
</div>

</div>
