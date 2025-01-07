---
title     : VarGlyphAssistant
layout    : default
permalink : /reference/tools/variable/varglyph-assistant/
---

A tool to view and edit glyph-level values in multiple designspace sources.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.


Designspace
-----------

Use the **designspace** tab to define which designspaces and font sources to look into.

![]({{ site.url }}/images/variable/VarGlyphAssistant-designspace.png){: .img-fluid}

designspaces
: Drag one or more `.designspace` files into the list.

sources
: ^
  A list of all sources in the selected designspace.  
  Select which sources to display values from in the next tabs.  

open
: Use the open button to open the selected sources in the UI.

reload
: Use the reload button to update the font data for all sources.


Attributes
----------

Use the **attributes** tab to visualize ~~and edit~~ glyph attributes in the selected glyph of the selected sources.

![]({{ site.url }}/images/variable/VarGlyphAssistant-attributes.png){: .img-fluid}

Double-click on a source to open the font in the UI.  
Click on the column headers to sort the list based on a specific attribute.

### Color codes
{: .h5 }

- Values in <span class='green'>green</span> are equal to the default.
- Values in <span class='red'>red</span> are different from the default.

{% comment %}
points
------

Use the **compatibility** tab to visualize contour segments in the selected glyph of the selected sources.

**Not implemented yet.**
{% endcomment %}


Measurements
------------

Use the **measurements** tab to visualize glyph measurements in the selected glyph of the selected sources.

![]({{ site.url }}/images/variable/VarGlyphAssistant-measurements.png){: .img-fluid}

load…
: Open a dialog to select a measurements file and load its data into the UI.

d-threshold
: Threshold value for validating the scale of the glyph measurement in relation to the default font.

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
For more information about measurements see [Measurements format] and [Measurement scales and thresholds].
{: .card-text }
</div>
</div>


[Measurements format]: ../../../measurements-format/
[Measurement scales and thresholds]: ../../../measurement-scales-thresholds
