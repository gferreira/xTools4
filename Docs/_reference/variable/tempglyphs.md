---
title     : TempGlyphs
layout    : default
permalink : /reference/tempglyphs
---

A tool to import glyphs from another font into a sparse source, and easily keep or discard them.
{: .lead}


Options
-------

<div class='row'>
<div class='col' markdown='1'>
![]({{ site.url }}/images/TempGlyphs.png){: .img-fluid}
</div>
<div class='col' markdown='1'>
sources
: One or more sources to import into the current font.

import
: Import glyphs from the selected font into the selected template glyphs in the current font.

toggle
: Keep the selected glyphs in the current font.

clear
: Remove imported glyphs from the current font.
</div>
</div>


Workflow
--------

1\. Open a sparse source, and open the TempGlyphs window. The sparse source should have empty template glyphs in place of missing glyphs.

![]({{ site.url }}/images/TempGlyphs_font-sparse.png){: .img-fluid}

2\. Define a full source to import glyphs from: select a UFO file in Finder, and drag and drop it into the sources list.

3\. Define which glyphs you would like to impor by selecting template glyphs in the current. In this example, we select all the remaining lowercase glyphs.

4\. Click on the *import* button to copy glyphs from the selected full source into the selected template glyphs of the current font. The imported glyphs are added to the `skipExport` list, as indicated by the red cross in their glyph cells.

![]({{ site.url }}/images/TempGlyphs_font-temp.png){: .img-fluid}

5\. You can now edit the non-imported glyphs using the imported glyphs as context.

6\. To keep any of the imported glyphs in the sparse source, click on the *toggle* button to remove it from the `skipExport` list.

7\. Once you're finished with editing, click on the *clear* button to have all imported glyphs removed from the sparse source.

8\. Save and close the sparse source.
