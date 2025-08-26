---
title     : Variable font production with xTools4
layout    : page
permalink : /explanations/variable-font-production
---

Introducing the main ideas behind the variable font production tools in xTools4.
{: .lead }

* Table of Contents
{:toc}


Variable Values
---------------

When working on variable font sources, the designer needs to know, at a glance, what is changing in a source in relation to the default.

Changes from the default should all be intentional, and not caused by errors and imprecision during the design process.

Visual proof is not sufficient: glyphs that appear equal may be numerically different.

As designspaces become larger, it becomes harder to keep track of what is changing where.

xTools4 introduces a new set of tools to reduce the cognitive burden of dealing with very large designspaces, using colors to filter out the noise and focus the designer's attention towards the relevant bits of data.


What do we want to track for changes?
-------------------------------------

##### 1. Standard attributes

A. font-level
  - vertical metrics
  - font info
  - kerning pairs / values
  - etc.

B. glyph-level
  - width
  - left / right margin
  - number of contours, points, components, anchors
  - unicode values

##### 2. Validation groups (glyph-level)

- equal to default / contours only
- equal to default / components only
- different from default / contours only
- different from default / components only
- error: mixed contours & components, or nested components

##### 3. Measurements (font- and glyph-level)

- distances between pairs of points
- angles?


Using colors to see everything at a glance 
------------------------------------------

Two color codes…

1. check results (marks, values)
2. validation groups (cell background)

…used consistently in separate tools:

- [GlyphValidator](../reference/tools/variable/glyph-validator/) (1+2)
- [GlyphSetProofer](../reference/tools/variable/glyphset-proofer/) (2)
- [Measurements](../reference/tools/variable/measurements/) (1)
- [VarGlyphAssistant](../reference/tools/variable/varglyph-assistant/) (1)
- [VarFontAssistant](../reference/tools/variable/varfont-assistant/) (1)
