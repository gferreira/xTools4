---
title     : BlendsPreview
layout    : default
permalink : /reference/tools/variable/blends-preview/
---

A tool for previewing blended locations from a parametric designspace and comparing them to a reference font.
{: .lead}

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.

![]({{ site.url }}/images/variable/BlendsPreview.png){: .img-fluid}

designspace…
: Load designspace data from an external file.

blended axes
: ^
  A list of blended axes (mappings) and values in the loaded designspace.
  The list of values for each axis can be edited.

reference font…
: Load a conventional variable font for comparison.

compare
: Show the reference font in the background for comparison.

margins
: Show left and right margins for each glyph.

points
: Show the contour points for each glyph (wireframe mode).

labels
: Show labels with the location parameters of each glyph.

levels
: Highlight variation levels (duovars, trivars, quadvars) with different colors.

show levels
: Show glyph samples only for the selected threshold levels.

update preview
: Regenerate the preview PDF from the latest files.

save PDF…
: Save the current proof as a PDF file.


<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header"> note</div>
<div class="card-body" markdown='1'>
This tool requires the external library `uharfbuzz` which can be installed in RoboFont using the [Package Installer](http://robofont.com/documentation/reference/workspace/package-installer/).
{: .card-text }
</div>
</div>