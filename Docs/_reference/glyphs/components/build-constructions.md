---
title     : build constructions
layout    : page
permalink : /reference/dialogs/glyphs/components/build-constructions
---

Build selected glyphs from components using [Glyph Construction] language.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  


[Glyph Construction]: http://github.com/typemytype/GlyphConstruction


<div class='row'>

<div class='col-sm' markdown='1'>
![]({{"images/glyphs/buildConstructions.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
import…
: import constructions from `.glyphConstruction` file

glyph constructions
: edit the list of glyph constructions as needed

export
: save construction changes back to the `.glyphConstruction` file

build
: build selected glyphs if a construction is available

preview
: show a preview of the glyph construction
</div>

</div>


preview
-------

![]({{"images/glyphs/buildConstructions_preview.png" | relative_url }}){: .img-fluid}


{% comment %}
- improve user interface to allow standard small palette
{% endcomment %}
