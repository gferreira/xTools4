---
title     : Expert tools for variable font production
layout    : page
permalink : /explanations/variable-font-production
---

Introducing the main ideas behind the variable font production tools in xTools4.
{: .lead }

* Table of Contents
{:toc}


Challenges in variable font production
--------------------------------------

{% comment %}

rewrite incl. other general challenges:

- visualizing variation in source font data (GlyphValidator + VarGlyphViewer + VarFontAssistant + VarGlyphAssistant + GlyphProofer)
- creating measurements (Measurements tool + format + scales + production scripts: set UFO names, build parametric designspace)
- editing glyph sources in RoboFont with temporary fonts (TempEdit + GlyphMeme + GlyphTuning + BlendsPreview + compatibility with other tools)
- additional data formats linked to the designspace lib

{% endcomment %}


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

<style>
._ td:nth-child(1) { width: 200px; }
</style>

##### 1. Check colors

| expression     | marks, values |
| representation | low-level comparison of attributes, values |
{: .table ._ }

##### 2. Validation colors

| expression     | cell color |
| representation | categorization of glyphs based on low-level checks |
{: .table ._ }


Variable tools supporting color codes
-------------------------------------

| tool | check colors | validation colors |
|-------------|-------------|
| [GlyphValidator](../reference/tools/variable/glyph-validator/) | <i class="bi bi-check2"></i> | <i class="bi bi-check2"></i> |
| [GlyphSetProofer](../reference/tools/variable/glyphset-proofer/) |   | <i class="bi bi-check2"></i> |
| [Measurements](../reference/tools/variable/measurements/) | <i class="bi bi-check2"></i> |   |
| [VarGlyphAssistant](../reference/tools/variable/varglyph-assistant/) | <i class="bi bi-check2"></i> |   |
| [VarFontAssistant](../reference/tools/variable/varfont-assistant/) | <i class="bi bi-check2"></i> |   |
| [VarGlyphViewer](../reference/tools/variable/varglyph-viewer/) | <i class="bi bi-check2"></i> |   |
{: .table .table-hover }
