---
title     : SourceValidator
layout    : default
permalink : /reference/dialogs/variable/source-validator
---

A tool to validate glyphs from one or more fonts against glyphs from another font.
{: .lead}


fonts
-----

Use the **fonts** tab to check a set of font sources against a reference font in batch.

![]({{ site.url }}/images/variable/SourceValidator-1.png){: .img-fluid}

reference font
: ^
  Drag one or more `.ufo` sources into the list.  
  Select one reference font against which the other sources will be checked.

other fonts
: ^
  Drag one or more `.ufo` sources into the list.  
  Select which sources to check against the reference font.

checks
: Select which glyph attributes to check.

validate
: Click to check all glyphs in all selected fonts against the reference font.  
  The check results are printed to the Output Window.


glyphs
------

Use the **glyphs** tab to check individual glyphs in the selected fonts against a reference font.

![]({{ site.url }}/images/variable/SourceValidator-2.png){: .img-fluid}

load
: Click to load the names of all glyphs in the reference font into the list.

glyphs
: A list of all glyphs in the reference font.  
  Select a glyph to view the check results for that glyph in all sources.

check results
: ^
  A list of color-coded check results for the current glyph in each selected source.

  🟢 matching  
  🔴 not matching  
  ⚪ missing  

