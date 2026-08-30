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
cases
: Select a case from the list (lowercase, uppercase, figures, etc).

glyph group
: Select a glyph group from the list.

glyph name
: Select a glyph from which to load parametric glyph sources.

glyph parameters (meme)
: A list of all parameters involved in the variations of the selected glyph.

open
: Import the selected glyph from the selected parametric sources into a temporary font for editing.

save
: Export the selected glyphs back into the UFO sources from where they came from.

designspace…
: Open a dialog to select a designspace file.

reload
: Reload the previously selected designspace file.
</div>
</div>


Example
-------

<img class='img-fluid' src='{{ site.url }}/images/variable/GlyphMeme_font.png' />

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Temporary fonts created with GlyphMeme are compatible with [GlyphValidator], [Measurements] and [Import Layer] tools.

Interoperability is achieved by adding [custom data] to the glyphs imported into a temporary font.
{: .card-text }
</div>
</div>

[GlyphValidator]: ../glyph-validator
[Measurements]: ../measurements
[Import Layer]: ../../glyphs/layers/import/
[custom data]: ../../temp-font-libs
