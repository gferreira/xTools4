---
title     : VarGlyphViewer
layout    : default
permalink : /reference/tools/variable/varglyph-viewer/
---

A tool to visualize and highlight the differences between the current glyph and the same glyph in the default font.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.  


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/VarGlyphViewer.png){: .img-fluid }
</div>
<div class='col-8' markdown='1'>
get default…
: Open a dialog to select the source to check against the current font.

reload
: Reload the selected source from disk (in case it has changed).

show default
: Show the default glyph in the background.

show distance
: Show x and/or y distance of each point in relation to the same point in the default.

selection only
: Show the distance visualization only for selected points.

subtract (-)
: Subtract the default glyph from the current glyph.

add (+)
: Add the default glyph to the current glyph.

display
: Turn the visualisation on/off.
</div>
</div>


Display
-------

![]({{ site.url }}/images/variable/VarGlyphViewer_preview.png){: .img-fluid}



Color code
----------

| <span class='blue'>blue circle</span> | neither x nor y values changing | 
| <span class='red'>red line</span> | only x or y value changing | 
| <span class='green'>green line</span> | both x and y values changing | 
{: .table .table-hover }


<div class="card bg-light mt-5 mb-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more info on adding and subtracting glyphs, see [Using GlyphMath](http://doc.robofont.com/documentation/tutorials/using-glyphmath/).
{: .card-text }
</div>
</div>
