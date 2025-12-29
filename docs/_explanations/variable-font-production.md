---
title     : Variable font production with xTools4
layout    : page
permalink : /explanations/variable-font-production
---

Introducing the main ideas behind the variable font production tools in xTools4.
{: .lead }

* Table of Contents
{:toc}


Challenges in variable font production
-------------------------------------

When working on variable font sources, the designer needs to know, at a glance, what is changing in a source in relation to the default.

Changes from the default should all be intentional, and not caused by errors and imprecision during a manual design process.

Visual proof is not sufficient: glyphs that appear equal may be numerically different!

As designspaces become larger, it becomes exponentially harder to keep track of what is changing where.


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

- equal to default / different from default
- contours only / components only
- errors: mixed contours & components, nested components

##### 3. Measurements (font- and glyph-level)

- distances between pairs of points

##### 4. Point deltas in relation to the default

- points which don’t move
- points which move only in x/y direction
- points which move in both x/y directions


The approach of xTools4
-----------------------

Functionality of variable tools is divided across several specific tools that can work together, following the [general design pattern of hTools](overview#modular).

xTools4 reduces the cognitive burden of dealing with very large designspaces by using colors to filter out the noise and focus the designer’s attention at the relevant bits of font source data.


Color codes
-----------

Throughout the variable toolkit, two separate color codes are used consistently, allowing the designer to see everything he needs at a glance.

##### Check colors

| expression     | marks, values |
| representation | low-level comparison of attributes, values |
{: .table }

##### Validation colors

| expression     | cell color |
| representation | categorization of glyphs based on low-level checks |
{: .table }


Variable Tools supporting color codes
-------------------------------------

- [GlyphValidator](../reference/tools/variable/glyph-validator/) (1+2)
- [GlyphSetProofer](../reference/tools/variable/glyphset-proofer/) (2)
- [Measurements](../reference/tools/variable/measurements/) (1)
- [VarGlyphAssistant](../reference/tools/variable/varglyph-assistant/) (1)
- [VarFontAssistant](../reference/tools/variable/varfont-assistant/) (1)
- [VarGlyphViewer](../reference/tools/variable/varglyph-viewer/) (1)
