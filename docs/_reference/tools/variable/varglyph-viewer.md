---
title     : VarGlyphViewer
layout    : default
permalink : /reference/tools/variable/varglyph-viewer/
---

A tool to visualize and highlight the differences between the current glyph and the same glyph in the default font.
{: .lead}


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/VarGlyphViewer.png){: .img-fluid }
</div>
<div class='col-8' markdown='1'>
get default…
: Open a dialog to select the source to check against the current font.

reload
: Reload the selected source from disk (in case it has changed).

show distance
: Show x and/or y distance of each point in relation to the default.

selection only
: Show the distance visualization only for selected points.

delta values
: Display average delta values.

threshold
: Adjust the threshold value between green and red values.

display
: Turn the visualisation on/off.
</div>
</div>


Display
-------

![]({{ site.url }}/images/variable/VarGlyphViewer_preview.png){: .img-fluid}


Color code
----------

<style>
.table { td:nth-child(1) { width: 8em; }
</style>

##### Delta vectors

| <span class='blue'>blue</span>   | neither x nor y values changing | 
| <span class='red'>red</span>     | only x or y value changing      | 
| <span class='green'>green</span> | both x and y values changing    | 
{: .table .table-hover }

##### Delta values

| <span class='blue'>blue</span>   | no change               | 
| <span class='red'>red</span>     | change beyond threshold | 
| <span class='green'>green</span> | change below threshold  | 
{: .table .table-hover }


Average delta values
--------------------

Average delta values allow us to quantify the variation between two glyphs. This is specially useful when analysing tuning glyphs.

Values are expressed in **average delta units per item**.

The total average delta value (Σ) is computed as the sum of all specific average delta values (points, anchors, components, width), divided by the total item count.

| Σ     | total average delta values / total item count  |
| P     | total point deltas / point count               |
| A     | total anchor deltas / anchor count             |
| C     | total component deltas / component count       |
| W     | width delta                                    |
{: .table .table-hover }

