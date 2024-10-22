---
title     : VarGlyphViewer
layout    : default
permalink : /reference/tools/variable/varglyph-viewer/
---

A tool to visualize and highlight the differences between the current glyph and the same glyph in another font.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.  


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/VarGlyphViewer.png){: .img-fluid }
</div>
<div class='col-8' markdown='1'>
get default…
: Open a dialog to select the source to check against the _current font_.

reload
: Reload the selected source from disk (in case it has changed).

font value
: Compare glyph measurements with their font-level value.

color
: Choose a color for the Glyph Editor visualization.

show equal
: Highlight points which have the same position as the default.

show deltas
: Show delta vectors for points which change position in relation to the default.

show default
: Show the default glyph shape in the background.

selection
: Show measurements in font units.

subtract
: Subtract the default glyph from the current glyph.

add
: Add the default glyph to the current glyph.

show preview
: Turn the visualisation on/off.
</div>
</div>


Preview
-------

![]({{ site.url }}/images/variable/VarGlyphViewer_preview.png){: .img-fluid}


<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more info on adding and subtracting glyphs, see [Using GlyphMath](http://doc.robofont.com/documentation/tutorials/using-glyphmath/).
{: .card-text }
</div>
</div>

