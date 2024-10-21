---
title     : Measurements
layout    : default
permalink : /reference/tools/variable/measurements/
---

A tool to create and visualize font- and glyph-level measurements.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.  


font
----

Use the **font** tab to create and edit font-level measurements.

![]({{ site.url }}/images/variable/Measurements_font.png){: .img-fluid}

add
: Add a new empty font-level measurement to the list.  

remove
: Delete the selected font-level measurement(s) from the list.  

load…
: Load measurement data from an external JSON file into the UI.

save…
: Save the current measurement data to an external JSON file.

default…
: Select and load the default font source for comparison.

p-treshold
: Treshold value for validating the scale of the font measurement in relation to its parent value.

d-treshold
: Treshold value for validating the scale of the font measurement in relation to the default font.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column of the table see [Measurements format > Font-level measurements] and [Measurement scales and tresholds].
{: .card-text }
</div>
</div>


glyph
-----

Use the **glyph** tab to create and edit glyph-level measurements.

![]({{ site.url }}/images/variable/Measurements_glyph.png){: .img-fluid}

add
: Select two points and click on the + button to add a new empty glyph-level measurement to the list.

remove
: Delete the selected glyph-level measurement(s) from the list.

f-treshold
: Treshold value for validating the scale of the glyph measurement in relation to the font-level value.

d-treshold
: Treshold value for validating the scale of the glyph measurement in relation to the default font.

display
: Turn the Glyph Editor visualization of the measurements on / off.

color
: Choose a color for the measurement lines and captions in the Glyph Editor visualization.

flip
: Invert the direction of selected measurements by swapping point indexes 1 and 2.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column see [Measurements format > Glyph-level measurements] and [Measurement scales and tresholds].
{: .card-text }
</div>
</div>


Preview
-------

The Glyph View displays a visualization of the measurements in the current glyph:

![]({{ site.url }}/images/variable/Measurements_preview.png){: .img-fluid}

- Dotted lines indicate a measurement between pairs of points.
- Select one or more measurements in the dialog to highlight and show their name, direction and distance.



- - -

<!--
New features
------------

- using table cell colors for validation
- treshold values for parent, font, and default values
- loading of default font
-->


Missing features
----------------

- drag to reorder font-level measurements
- indicator for glyph-level measurements in Font Overview glyph cells


Know bugs
---------

- flip button is not working (reverts to previous value after editing)
- “ghost” measuremements from previous glyph are displayed in glyphs with no measurements


[Measurements format > Font-level measurements]: ../../../measurements-format/#font-level-measurements
[Measurements format > Glyph-level measurements]: ../../../measurements-format/#glyph-level-measurements
[Measurement scales and tresholds]: ../../../measurement-scales-tresholds
