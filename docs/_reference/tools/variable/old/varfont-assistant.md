---
title     : VarFontAssistant (old)
layout    : default
permalink : /reference/tools/variable/old/varfont-assistant/
---

A tool to view and edit font-level values in multiple designspace sources.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  


Designspace
-----------

Define which designspaces and font sources to look into.

![]({{ site.url }}/images/variable/old/VarFontAssistant-designspace.png){: .img-fluid}

designspaces
: Drag one or more `.designspace` files into the list.

axes
: ^
  A list of axes in the selected designspace.  
  Drag the items to change the sorting order of the list of sources.


sources
: ^
  A list of all sources in the selected designspace.  
  Select which sources to collect values from in the next tabs.  
  Double-click a source to open the font in the UI.


Font info
---------

Visualize and edit font values in selected sources.

![]({{ site.url }}/images/variable/old/VarFontAssistant-fontinfo.png){: .img-fluid}

load
: Click on the button to collect values from the fonts and display them in the UI.

attributes
: A list of font attributes for which to display collected values.

values
: ^
  Values and visualization of the selected font attribute across all selected sources.  
  Double-click individual values to edit.

save
: Click the button to save the edited values back into the fonts.


Kerning
-------

Visualize and edit kerning values in selected sources.

![]({{ site.url }}/images/variable/old/VarFontAssistant-kerning.png){: .img-fluid}

load
: Click on the button to collect values from the fonts and display them in the UI.

pairs
: A list of all kerning pairs in all selected sources.

preview
: A visual preview of the selected kerning pair in all selected sources.

values
: ^
  Values and visualization of the selected kerning pair across all selected sources.  
  Double-click individual values to edit.

save
: Save the edited values back into the fonts.


Measurements
------------

Collect custom measurements from the selected sources.

![]({{ site.url }}/images/variable/old/VarFontAssistant-measurements.png){: .img-fluid}

measurement files
: Drag one or more `.json` files containing [measurement definitions] into the list.

load
: Click on the button to collect values from the fonts and display them in the UI.

measurements
: ^
  A list of measurement definitions contained in the selected file.  
  Select one measurement to display its values.

value
: Value of the selected measurement across all selected sources in font units.  

permill
: Value of the selected measurement across all selected sources in permill units (thousands of em).

export
: Export the measurements data to an external file.


[measurement definitions]: ../../../../measurements-format/


Validation
----------

![]({{ site.url }}/images/variable/old/VarFontAssistant-validator.png){: .img-fluid}

checks
: Select which glyph attributes to check against the default source.

validate
: Validate the selected sources.

result
: The result is printed to the output area once the validation process is completed.
