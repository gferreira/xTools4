---
title     : VarFontAssistant
layout    : default
permalink : /reference/tools/variable/varfont-assistant/
---

A tool to view and edit font-level values in multiple designspace sources.
{: .lead}


Designspace
-----------

Define which designspaces and font sources to look into.

![]({{ site.url }}/images/variable/VarFontAssistant-designspace.png){: .img-fluid}

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

![]({{ site.url }}/images/variable/VarFontAssistant-fontinfo.png){: .img-fluid}

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

![]({{ site.url }}/images/variable/VarFontAssistant-kerning.png){: .img-fluid}

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
: Click the button to save the edited values back into the fonts.


Measurements
------------

Collect custom measurements from the selected sources.

![]({{ site.url }}/images/variable/VarFontAssistant-measurements.png){: .img-fluid}

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


[measurement definitions]: ../measurements-format/