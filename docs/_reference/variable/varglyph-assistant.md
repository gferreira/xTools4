---
title     : VarGlyphAssistant
layout    : default
permalink : /reference/tools/variable/varglyph-assistant/
---

A tool to view and edit glyph-level values in multiple designspace sources.
{: .lead}

<span class="badge text-bg-success rounded-0">RF4</span> Rewritten using the new RoboFont 4 APIs.


designspace
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
: Use the open button or double-click on a source to open the font in the UI.


attributes
----------

Use the **attributes** tab to visualize ~~and edit~~ glyph attributes in the selected glyph of the selected sources.

![]({{ site.url }}/images/variable/VarGlyphAssistant-attributes.png){: .img-fluid}

- Open one source from this designspace to navigate through the glyphs.
- Click on the column headers to sort the list based on a specific attribute.


points
------

Use the **compatibility** tab to visualize contour segments in the selected glyph of the selected sources.

**Not implemented yet.**


measurements
------------

Use the **measurements** tab to visualize glyph measurements in the selected glyph of the selected sources.

![]({{ site.url }}/images/variable/VarGlyphAssistant-measurements.png){: .img-fluid}

load…
: Open a dialog to select a measurements file and load its data into the UI.

f-threshold
: Treshold value for validating the scale of the glyph measurement in relation to the font-level value.

d-threshold
: Treshold value for validating the scale of the glyph measurement in relation to the default font.
