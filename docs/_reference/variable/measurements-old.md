---
title     : Measurements (old)
layout    : default
permalink : /reference/tools/variable/measurements-old/
---

A tool to create and visualize font- and glyph-level measurements.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. For the new RoboFont 4 version, see [Measurements](../measurements).  


font
----

Use the **font** tab to create and edit font-level measurements.

![]({{ site.url }}/images/variable/Measurements-old_font.png){: .img-fluid}

new
: Click to add a new empty font-level measurement to the list.  
  Double-click the new item's cells to edit its content.

load…
: Load measurement data from an external JSON file into the UI.

save…
: Save the current measurement data to an external JSON file.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column see [Measurements format > Font-level measurements](../../measurements-format/#font-level-measurements).
{: .card-text }
</div>
</div>


glyph
-----

Use the **glyph** tab to create and edit glyph-level measurements.

![]({{ site.url }}/images/variable/Measurements-old_glyph.png){: .img-fluid}

new
: Select two points and click on the button to add a new empty glyph-level measurement to the list.

color
: Choose a color for the measurement lines and captions in the Glyph Editor preview.

flip
: Invert the direction of selected measurements by swapping point indexes 1 and 2.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column see [Measurements format > Glyph-level measurements](../../measurements-format/#glyph-level-measurements).
{: .card-text }
</div>
</div>


Preview
-------

The Glyph View displays a visualization of the measurements in the current glyph:

![]({{ site.url }}/images/variable/Measurements-old_preview.png){: .img-fluid}

- Dotted lines indicate a measurement between pairs of points.
- Select one or more measurements in the dialog to highlight and show their name, direction and distance.

