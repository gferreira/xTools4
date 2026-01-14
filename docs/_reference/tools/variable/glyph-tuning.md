---
title     : GlyphTuning
layout    : default
permalink : /reference/tools/variable/glyph-tuning/
---

A tool to open all corner-tuning sources of a single glyph in a temporary font for editing.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Written using the new RoboFont 4 APIs.

<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/GlyphTuning.png){: .img-fluid }
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

tuning corners
: Select which tuning corners you would like to edit: *duovars*, *trivars*, *quadvars*.

open
: Import the selected glyph from the selected parametric sources into a temporary font for editing.

save
: Export the selected glyphs back into the UFO sources from where they came from.
</div>
</div>

Example
-------

<img class='img-fluid' src='{{ site.url }}/images/variable/GlyphTuning_font.png' />


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
Temporary fonts created with GlyphTuning are compatible with [GlyphValidator] and [Import Layer] tools.
{: .card-text }
</div>
</div>

[GlyphValidator]: ../glyph-validator
[Import Layer]: ../../glyphs/layers/import/
