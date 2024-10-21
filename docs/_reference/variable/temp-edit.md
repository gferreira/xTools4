---
title     : TempEdit
layout    : default
permalink : /reference/tools/variable/temp-edit/
---

A tool to edit glyphs from multiple designspace sources using temporary font(s).
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  


Options
-------

<div class='row'>
<div class='col' markdown='1'>
  <img class='img-fluid' src='{{ site.url }}/images/variable/TempEdit.png' />
</div>
<div class='col' markdown='1'>
designspaces
: a list of designspace files  
  
  - drag one or more `.designspace` files from Finder to add them to the list
  - select and press backspace to remove files from the list

sources
: a list os sources in the selected designspace
  
  - select one or more sources to import glyphs from

glyphs
: a list of glyph names to import from the selected sources

import glyphs
: import glyphs with the given glyph names from the selected designspace sources for editing  

export selected glyphs
: export selected glyphs in the current temp font back into their parent fonts
</div>
</div>


Import modes
------------

TempEdit offers 3 different import modes:

### fonts → fonts
{: .h5 }

Import glyph(s) from each source into a separate font.

<img class='img-fluid' src='{{ site.url }}/images/variable/TempEdit_fonts.png' />

### fonts → glyphs
{: .h5 }

Import each glyph source into a separate glyph of a single font

<img class='img-fluid' src='{{ site.url }}/images/variable/TempEdit_glyphs.png' />

### fonts → layers
{: .h5 }

Import glyph sources as layers of a single font.

<img class='img-fluid' src='{{ site.url }}/images/variable/TempEdit_layers.png' />

