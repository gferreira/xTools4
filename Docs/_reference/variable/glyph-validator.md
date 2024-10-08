---
title     : GlyphValidator
layout    : default
permalink : /reference/dialogs/variable/glyph-validator
---

A tool to validate glyphs in the current font against glyphs from another source.
{: .lead}


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/GlyphValidator.png){: .img-fluid}
</div>
<div class='col-8' markdown='1'>
get default…
: Open a dialog to select the source to check against the _current font_ 

reload
: Reload the selected source from disk (in case it has changed).

checks
: Select which glyph attributes to check and report on.

font window
: Show/hide check results in the Font Overview’s glyph cells.

glyph window
: Show/hide check results in the Glyph View.

mark glyphs
: Apply mark colors to different types of glyphs.

</div>
</div>


Check results
-------------

##### Font window

Labels with check results are shown in the Font Overview’s glyph cells if the option *font window* is activated.

![]({{ site.url }}/images/variable/GlyphValidator_font-window.png){: .img-fluid}

##### Glyph window

Labels with check results are shown in the Glyph View if the option *glyph window* is activated.

![]({{ site.url }}/images/variable/GlyphValidator_glyph-window.png){: .img-fluid}


Validation details
------------------

##### Color codes

Check results are displayed as a string of colored labels. Label colors have the following meaning:

<!--
| color                                                 | meaning        |
|-------------------------------------------------------|----------------|
| <span style='color:red;'>red</span>                   | not compatible |
| <span style='color:rgba(0, 216.75, 0);'>green</span>  | compatible     |
| <span style='color:rgba(0, 114.75, 255);'>blue</span> | equal\*        |
{: .table .table-hover }
-->

<table class='table table-hover'>
<tr>
<th>glyph attribute</th>
<th>label</th>
<th>red</th>
<th>green</th>
<th>blue</th>
</tr>
<tr>
<td>width</td>
<td>W</td>
<td><span class='red'>different</span></td>
<td><span class='green'>equal</span></td>
<td>–</td>
</tr>
<tr>
<td>left margin</td>
<td>L</td>
<td><span class='red'>different</span></td>
<td><span class='green'>equal</span></td>
<td>–</td>
</tr>
<tr>
<td>right margin</td>
<td>R</td>
<td><span class='red'>different</span></td>
<td><span class='green'>equal</span></td>
<td>–</td>
</tr>
<tr>
<td>points</td>
<td>P</td>
<td><span class='red'>incompatible</span></td>
<td><span class='green'>compatible</span></td>
<td><span class='blue'>equal</span></td>
</tr>
<tr>
<td>components</td>
<td>C</td>
<td><span class='red'>incompatible</span></td>
<td><span class='green'>compatible</span></td>
<td><span class='blue'>equal</span></td>
</tr>
<tr>
<td>anchors</td>
<td>A</td>
<td><span class='red'>incompatible</span></td>
<td><span class='green'>compatible</span></td>
<td><span class='blue'>equal</span></td>
</tr>
<tr>
<td>unicodes</td>
<td>U</td>
<td><span class='red'>different</span></td>
<td><span class='green'>equal</span></td>
<td>–</td>
</tr>
</table>

##### Compatibility checks

Glyph attributes are considered **compatible** if the following conditions are met:

<table class='table table-hover'>
<tr>
<th>glyph attribute</th>
<th>label</th>
<th>conditions</th>
</tr>
<tr>
<td>points</td>
<td>P</td>
<td markdown='1'>
- same number of contours
- same number of segments
- same segment types
- same number of points (implied)
</td>
</tr>
<tr>
<td>components</td>
<td>C</td>
<td markdown='1'>
- same number of components
- same component names
- same component order
</td>
</tr>
<tr>
<td>anchors</td>
<td>A</td>
<td markdown='1'>
- same number of anchors
- same anchor names
- same anchor order
</td>
</tr>
</table>

##### Equality checks

Glyph attributes are considered **identical** if the following conditions are met:

<table class='table table-hover'>
<tr>
<th>glyph attribute</th>
<th>label</th>
<th>conditions</th>
</tr>
<tr>
<td>width</td>
<td>W</td>
<td markdown='1'>
- same advance width
</td>
</tr>
<tr>
<td>left margin</td>
<td>L</td>
<td markdown='1'>
- same left margin (rounded)
</td>
</tr>
<tr>
<td>right margin</td>
<td>R</td>
<td markdown='1'>
- same right margin (rounded)
</td>
</tr>
<tr>
<td>points</td>
<td>P</td>
<td markdown='1'>
- same point positions
</td>
</tr>
<tr>
<td>components</td>
<td>C</td>
<td markdown='1'>
- same point positions (flattened)
</td>
</tr>
<tr>
<td>anchors</td>
<td>A</td>
<td markdown='1'>
- same anchor positions
</td>
</tr>
<tr>
<td>unicodes</td>
<td>U</td>
<td markdown='1'>
- same unicode value(s)
</td>
</tr>
</table>


##### Mark colors 

See [GlyphSetProofer > Validation details > Cell colors](glyphset-proofer).

