---
title     : GlyphMeme
layout    : default
permalink : /reference/tools/variable/glyph-meme/
---

A tool to open all parametric sources of a single glyph in a temporary font for editing.
{: .lead}


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/GlyphMeme.png){: .img-fluid }
</div>
<div class='col-8' markdown='1'>
designspace…
: Open a dialog to select a designspace file.

reload
: Reload the previously selected designspace file.

glyph group
: Select a glyph group from the list (imported from smart sets).

glyph name
: Select a glyph from which to load parameters (meme).

glyph parameters (meme)
: A list of all parameters involved in the variations of the selected glyph.

open
: Import the selected glyph from the selected parametric sources into a temporary font for editing.

save
: Export the selected glyphs back into the UFO sources from where they came from.
</div>
</div>

<!-- move steps to a tutorial:

Step-by-step
------------

1. Open the GlyphMeme tool from the menu *xTools4 > variable > glyph meme*.
2. Use the buttons at the bottom to load the necessary data files (designspace, measurements, smart sets).
3. Use the first drop-down menu to select a group of glyphs, and the second one to choose one glyph for editing.
4. Select which parameters of this glyph you would like to edit.
5. Click the “open” button to import glyphs from the corresponding sources into a temporary font.
6. Multiple glyphs can be opened this way, with one temporary font for each.
7. Edit glyphs as needed, and then use the “save” button to export the selected glyphs back to their UFOs.

-->


Example
-------

<img class='img-fluid' src='{{ site.url }}/images/variable/GlyphMeme_font.png' />


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Temporary fonts created with GlyphMeme are compatible with [GlyphValidator], [Measurements] and [Import Layer] tools.
{: .card-text }
</div>
</div>

[GlyphValidator]: ../glyph-validator
[Measurements]: ../measurements
[Import Layer]: ../../glyphs/layers/import/
