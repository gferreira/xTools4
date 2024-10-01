---
title     : Measurements
layout    : default
permalink : /variable/measurements
---

A tool to create and visualize font- and glyph-level measurements.
{: .lead}


Font measurements
-----------------

Use the **font** tab to create and edit font-level measurements.

![]({{ site.url }}/images/Measurements_font.png){: .img-fluid}

new
: Click to add a new empty font-level measurement to the list.  
  Double-click the new item's cells to edit its content.

<div class="alert alert-primary" role="alert" markdown='1'>
For more information about each column see [Measurements format > Font-level measurements](../../measurements-format/#font-level-measurements).
{: .card-text }
</div>


Glyph measurements
------------------

Use the **glyph** tab to create and edit glyph-level measurements.

![]({{ site.url }}/images/Measurements_glyph.png){: .img-fluid}

new
: Select two points and click on the button to add a new empty glyph-level measurement to the list.

color
: Choose a color for the measurement lines and captions in the Glyph Editor preview.

flip
: Invert the direction of selected measurements by swapping point indexes 1 and 2.

<div class="alert alert-primary" role="alert" markdown='1'>
For more information about each column see [Measurements format > Glyph-level measurements](../../measurements-format/#glyph-level-measurements).
{: .card-text }
</div>


Glyph measurements preview
--------------------------

The Glyph View displays a visualization of the measurements in the current glyph:

![]({{ site.url }}/images/Measurements_preview.png){: .img-fluid}

- Dotted lines indicate a measurement between pairs of points.
- Select one or more measurements in the dialog to highlight and show their name, direction and distance.


Loading and saving
------------------

Reading and writing measurement data to external files.

load…
: Load measurement data from an external JSON file into the UI.

save…
: Save the current measurement data to an external JSON file.

