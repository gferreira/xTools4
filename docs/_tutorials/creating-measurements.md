---
title     : Creating measurements for an existing font or designspace
layout    : default
permalink : /tutorials/creating-measurements/
---

What measurements are, why they are useful, and how you can use them in your project.
{: .lead }

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Introduction
------------

### Measurements in typeface design
{: .h5 }

While working on a font, designers often need to keep track of certain values which should be used consistently throughout a typeface. Design features such as uppercase or lowercase stem thickness, overshoots, height and length of serifs, etc. should usually have the same dimensions across all glyphs in a font, more or less.

In small projects, keeping track of such values can be as simple as writing them down on a piece of paper. For larger projects with multiple variation axes and/or multiple scripts, a spreadsheet is often good enough.

All major font editors have a measuring tool, and their measurements are all not ‘sticky’ – they disappear as soon as the user clicks on another tool, changes the current glyph, or closes the font.

Some specific font dimensions are used when hinting a font: PostScript fonts have slots for vertical and horizontal stems, and alignment zones; TrueType fonts can include a Control Values Table (CVT) with various values to be used by instructions.

Parametric variable fonts ...

### The Measurements tool
{: .h5 }

The [Measurements] tool which is part of xTools4 introduces a new approach which integrates measuring deep into the design process. This approach was developed to enable the production of parametric variable fonts, but it can be useful to any typeface project, as it gives the designer insight into relationships between the glyph shapes in a font, and between multiple locations in a designspace.

The Measurements tool allows you to create a set of measurements for a given designspace, and to store them in a [custom data format]. Measurements can be created at the font level, representing the default values for the whole font; and at the glyph level, indicating relevant measurements in individual glyphs and their relationship to the font-level values.

Once created, measurements can be used to check and compare the dimensions of any source against the default style (assuming the) as long as the point structures between the fonts remain compatible. The interface for measurement data uses a simple color scheme to greatly reduce the effort to make sense of the numbers. The tool also adds an interactive visualization of measurements to the Glyph Editor, giving the typeface designer numerical feedback in real-time while drawing.

[Measurements]: #
[custom data format]: #

### In this tutorial
{: .h5 }

In this tutorial you will learn how to create measurements from scratch for an existing font and/or designspace. We will create font- and glyph-level measurements for common typeface design parameters (vertical and horizontal stems, counters, overshoots, serifs), and store them in an external file.


Creating font-level measurements
--------------------------------

### Parent measurements

We'll start with the three main measurements: vertical and horizontal stems, and counter width. We'll be using parameter names and definitions from the [FontBureau Variations Axes Proposal](#). The *glyph* column indicates in which glyph the measurement will be made. 

name | glyph | description
-----|-------|------------------------------------------------
XOPQ | H     | General x opaque (vertical stem thickness)
YOPQ | H     | General y opaque uppercase (horizontal stem thickness)
XTRA | H     | General x transparent (counter width)
{: .table .table-hover }

Let's begin by opening the [Measurements] tool, and the font you would like to measure. All three measurements above are taken from the glyph `/H`, so we open this glyph in the Glyph Editor.

The first measurement in the list is `XOPQ`, or vertical stem thickness. We'll measure it at the bottom left of the first stem. While in the *fonts* tab, we create the measurement by selecting points `A` and `B`, and clicking on the plus button at the bottom left. A new item will be added the font-level measurements table, with the glyph and point indexes already filled in. Click on the *name* column and type in the name of the measurement: `XOPQ`. Because this measurement starts with an `x`, the tool assumes that the measurement will be made along the x axis, and fills the *direction* column in as `x`; you can change it to `y` (measure along the y axis) or `a` (direct distance between the points). In the *description* column, add a brief description of this measurement.

### Child measurements

name | glyph | description              | parent 
-----|-------|--------------------------|--------
XOUC | H     | x opaque uppercase       | XOPQ   
XOLC | n     | x opaque lowercase       | XOPQ   
XOFI | one   | x opaque figures         | XOPQ   
-----|-------|--------------------------|--------
YOUC | H     | y opaque uppercase       | YOPQ   
YOLC | n     | y opaque lowercase       | YOPQ   
YOFI | zero  | y opaque figures         | YOPQ   
-----|-------|--------------------------|--------
XTUC | H     | x transparent uppercase  | XTRA   
XTLC | n     | x transparent lowercase  | XTRA   
XTFI | zero  | x transparent figures    | XTRA   
{: .table .table-hover }

<!--

### Additional measurements

name | glyph  | description            
-----|--------|-------------------------
YTOS | H      | y transparent overshoot  
WDSP | space  | x word space width
XDOT | period | x dot width
YTUC | H      | 
YTLC | H      | 
YTDE | p      | 
YTAS | d      | 

name | glyph 1 | glyph 2 | description            
-----|---------|---------|-------------------------
YTRA | d       | p       | 




-->


Creating glyph-level measurements
---------------------------------

...


