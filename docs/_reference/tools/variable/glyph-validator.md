---
title     : GlyphValidator
layout    : default
permalink : /reference/tools/variable/glyph-validator/
---

A tool to validate glyphs in the current font against glyphs from another source.
{: .lead}


<div class='row'>
<div class='col-4' markdown='1'>
![]({{ site.url }}/images/variable/GlyphValidator.png){: .img-fluid}
</div>
<div class='col-8' markdown='1'>
designspace…
: Open a dialog to select a designspace file.

reload
: Reload the previously selected designspace file.

checks
: Select which glyph attributes to check and report on.

mark groups
: Apply mark colors to indicate different validation groups.

validation groups
: Select which validation groups to use to filter the font overview.

filter glyphs
: Filter the font overview to show only glyphs in the selected validation group(s).

font window
: Show/hide check results in the Font Overview’s glyph cells.

glyph window
: Show/hide check results in the Glyph View.
</div>
</div>


Checks
------

Glyph attributes in the current font are checked against attributes of the same glyph in the default font.

- width
- left
- right
- points
- components
- anchors
- unicode


Validation groups
-----------------

Based on the results of the attribute checks, a glyph can be categorized as belonging to one of five validation groups.

= contours
: Glyphs consisting only of contours (or empty), equal to the default.

≠ contours
: Glyphs consisting only of contours (or empty), different from the default.

= components
: Glyphs consisting only of components, equal to the default.

≠ components
: Glyphs consisting only of components, different from the default.

‼ not allowed
: Glyphs which are not allowed: nested contours, mixed contours and components.


Display options
---------------

### Font window
{: .h5 }

If the option *font window* is activated, the validation results are shown in the Font Overview’s glyph cells:

- labels with check results are displayed at the top left of each cell
- a colored triangular patch indicating the validation group is shown at the top right (see below)

![]({{ site.url }}/images/variable/GlyphValidator_font-window.png){: .img-fluid}

### Glyph window
{: .h5 }

Labels with check results are shown in the Glyph View if the option *glyph window* is activated.

![]({{ site.url }}/images/variable/GlyphValidator_glyph-window.png){: .img-fluid}


Validation details
------------------

### Color codes
{: .h5 }

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

### Compatibility checks
{: .h5 }

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

### Equality checks
{: .h5 }

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
    <td>same advance width</td>
  </tr>
  <tr>
    <td>left margin</td>
    <td>L</td>
    <td>same left margin (rounded)</td>
  </tr>
  <tr>
    <td>right margin</td>
    <td>R</td>
    <td>same right margin (rounded)</td>
  </tr>
  <tr>
    <td>points</td>
    <td>P</td>
    <td>same point positions</td>
  </tr>
  <tr>
    <td>components</td>
    <td>C</td>
    <td>same point positions (decomposed)</td>
  </tr>
  <tr>
    <td>anchors</td>
    <td>A</td>
    <td>same anchor positions</td>
  </tr>
  <tr>
    <td>unicodes</td>
    <td>U</td>
    <td>same unicode value(s)</td>
  </tr>
</table>

### Validation group colors
{: .h5 }

See [GlyphSetProofer > Validation details > Cell colors](../glyphset-proofer) for the meaning of each color.

![]({{ site.url }}/images/variable/GlyphValidator_mark-colors.png){: .img-fluid}
