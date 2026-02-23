---
title     : VarFontAssistant
layout    : default
permalink : /reference/tools/variable/varfont-assistant/
---

A tool to view and edit font-level values in multiple designspace sources.
{: .lead}


Designspace
-----------

Use the **designspace** tab to define which designspaces and font sources to look into.

![]({{ site.url }}/images/variable/VarFontAssistant_designspace.png){: .img-fluid}

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


Font info
---------

Visualize ~~and edit~~ font values in selected sources.

![]({{ site.url }}/images/variable/VarFontAssistant_fontinfo.png){: .img-fluid}

attributes
: A list of font attributes for which to display collected values.

values
: Values for the selected font attribute across all selected sources.  


Kerning
-------

Visualize ~~and edit~~ kerning values in selected sources.

![]({{ site.url }}/images/variable/VarFontAssistant_kerning.png){: .img-fluid}

pairs
: A list of all kerning pairs in all selected sources.

values
: Values for the selected kerning pair across all selected sources.  


Measurements
------------

Collect custom measurements from the selected sources.

![]({{ site.url }}/images/variable/VarFontAssistant_measurements.png){: .img-fluid}

load…
: Open a dialog to select a measurements file and load its data into the UI.

measurements
: A list of measurement definitions contained in the selected file.  

d-threshold
: Threshold value for validating the scale of the glyph measurement in relation to the default font.


[measurement definitions]: ../../../measurements-format/


Validation
----------

![]({{ site.url }}/images/variable/VarFontAssistant_validation.png){: .img-fluid}

checks
: Select which glyph attributes to check against the default source.

validate
: Validate the selected sources.

result
: The result is printed to the output area once the validation process is completed.
