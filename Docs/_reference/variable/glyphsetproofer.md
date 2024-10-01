---
title     : GlyphSetProofer
layout    : default
permalink : /variable/glyphsetproofer
---

A tool to create informative PDF glyphset proofs of designspace sources.
{: .lead}

![]({{ site.url }}/images/GlyphSetProofer.png){: .img-fluid}


designspaces
: Drag one or more `.designspace` files into the list.

sources
: A list of all sources\* in the selected designspace. Select one or more sources to proof.

make proof
: Make a proof document for the selected sources, with one source per page.

save PDF…
: Save the current proof as a PDF file.

\* The default source is always shown in the first page of the proof, and is not included in the sources list.  



Validation details
------------------

##### Check colors

See [GlyphValidator > Validation details > Color codes](glyph-validator).

##### Cell colors

<table class='table'>
<tr>
<th>background color</th>
<th>status</th>
<th>contents</th>
</tr>
<tr>
<td class='cells-contours-equal'>blue</td>
<td>equal to default</td>
<td>contours only</td>
</tr>
<tr>
<td class='cells-contours-different'>white</td>
<td>different from default</td>
<td>contours only</td>
</tr>
<tr>
<td class='cells-components-equal'>light orange</td>
<td>equal to default</td>
<td>components only</td>
</tr>
<tr>
<td class='cells-components-different'>dark orange</td>
<td>different from default</td>
<td>components only</td>
</tr>
<tr>
<td class='cells-warning'>red</td>
<td>warning: not allowed</td>
<td>nested components, or mixed contour/components</td>
</tr>
</table>
