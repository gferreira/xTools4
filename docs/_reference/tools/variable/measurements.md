---
title     : Measurements
layout    : default
permalink : /reference/tools/variable/measurements/
---

A tool to create and visualize font- and glyph-level measurements.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.  


![]({{ site.url }}/images/variable/Measurements_font.png){: .img-fluid}

designspace…
: Load a designspace file and linked measurements data into the UI.

reload
: Reload the previously selected designspace file.

save
: Save the measurements data back to the external JSON file from which it was loaded.

italic correction
: Enable or disable italic angle and offset correction.


Font
----

Use the **font** tab to create and edit font-level measurements.

add (+)
: Add a new empty font-level measurement to the list.  

remove (-)
: Delete the selected font-level measurement(s) from the list.  

p-threshold
: Treshold value for validating the scale of the font measurement in relation to its parent value.

d-threshold
: Treshold value for validating the scale of the font measurement in relation to the default font.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column of the table see [Measurements format > Font-level measurements] and [Measurement scales and thresholds].
{: .card-text }
</div>
</div>


Glyph
-----

Use the **glyph** tab to create and edit glyph-level measurements.

![]({{ site.url }}/images/variable/Measurements_glyph.png){: .img-fluid}

add (+)
: Select two points and click on the + button to add a new empty glyph-level measurement to the list.

remove (-)
: Delete the selected glyph-level measurement(s) from the list.

f-threshold
: Treshold value for validating the scale of the glyph measurement in relation to the font-level value.

d-threshold
: Treshold value for validating the scale of the glyph measurement in relation to the default font.

display
: Turn the Glyph Editor visualization of the measurements on / off.

color
: Choose a color for the measurement lines and captions in the Glyph Editor visualization.

permill
: Switch interactive measurements from units to permill values.

flip
: Invert the direction of selected measurements by swapping point indexes 1 and 2.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about each column see [Measurements format > Glyph-level measurements] and [Measurement scales and thresholds].
{: .card-text }
</div>
</div>


Preview
-------
{: .mt-4 }

### Font overview
{: .h5 }

Glyphs containing measurements are marked with a letter **M** in the Font Overview glyph cells.

![]({{ site.url }}/images/variable/Measurements_glyph-cells.png){: .img-fluid}

### Glyph window
{: .h5 }

The Glyph View displays a visualization of the measurements in the current glyph:

<div class='row'>
<div class='col-lg' markdown='1'>
![]({{ site.url }}/images/variable/Measurements_preview.png){: .img-fluid}
</div>
<div class='col-lg' markdown='1'>
![]({{ site.url }}/images/variable/Measurements_preview-italic.png){: .img-fluid}
</div>
</div>

- Dotted lines indicate a measurement between pairs of points.
- Select one or more measurements in the list to highlight and show their direction and distance.
- Use the color button to change the color of the measurements.


{% comment %}

Missing features
----------------

- [ ] drag to reorder font-level measurements


Know bugs
---------

- [ ] “ghost” measuremements from previous glyph are displayed in glyphs with no measurements

{% endcomment %}


[Measurements format > Font-level measurements]: ../../../measurements-format/#font-level-measurements
[Measurements format > Glyph-level measurements]: ../../../measurements-format/#glyph-level-measurements
[Measurement scales and thresholds]: ../../../measurement-scales-thresholds
