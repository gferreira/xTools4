---
title     : GlyphMeme
layout    : default
permalink : /reference/tools/variable/glyph-meme/
---

A tool to open all parametric sources of a single glyph in a temporary font for editing.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.

<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/GlyphMeme.png){: .img-fluid }
</div>
<div class='col-8' markdown='1'>
get designspace…
: Open a dialog to select a designspace file.

get measurements…
: Open a dialog to select a measurements file.

get smart sets…
: Open a dialog to select a smart sets file.

glyph group
: Select a glyph group from the list (imported from smart sets).

glyph name
: Select a glyph for which to show the memes.

parameters (meme)
: A list of all parameters involved in the variations of the selected glyph.

open
: Import the selected glyph from the selected parametric sources into a temporary font for editing.

save
: Export the selected glyphs back into the UFO sources from where they came from.

</div>
</div>


Example
-------

<img class='img-fluid' src='{{ site.url }}/images/variable/GlyphMeme_font.png' />


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Temporary fonts created with GlyphMeme are compatible with [GlyphValidator] and [Measurements] tools.
{: .card-text }
</div>
</div>

[GlyphValidator]: ../glyph-validator
[Measurements]: ../measurements
