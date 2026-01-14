---
title     : Color codes
layout    : default
permalink : /reference/color-codes/
---

The systematic use of colors makes it easy to filter information from noise.
{: .lead }

* Table of Contents
{:toc}

<style>
._table td:nth-child(1) { width: 200px; }
._label1 { margin-right: 0.2em; }
._label2 { padding: 0.1em 0.4em; margin-right: 0.2em; }
._white { border: solid 1px #DDD !important; }
</style>


Check colors
------------

| color set      | <span class='_label1 red'>red</span> <span class='_label1 green'>green</span> <span class='_label1 blue'>blue</span> |
| applied to     | check labels, values, vectors |
| representing   | low-level comparison of attributes, values, positions |
| implemented in | [GlyphValidator]<br/>[GlyphSetProofer]<br/>[Measurements]<br/>[VarGlyphAssistant]<br/>[VarFontAssistant]<br/>[VarGlyphViewer] |
{: .table ._table }


Validation colors
-----------------

| color set      | <span class='_label2 cells-contours-different _white'>white</span> <span class='_label2 cells-contours-equal'>blue</span> <span class='_label2 cells-components-equal'>yellow</span> <span class='_label2 cells-components-different'>orange</span> <span class='_label2 cells-warning'>red</span> |
| applied to     | glyph cell background color |
| representing   | categorization of glyphs based on low-level checks |
| implemented in | [GlyphValidator]<br/>[GlyphSetProofer] |
{: .table ._table }



[GlyphValidator]: ../tools/variable/glyph-validator/
[GlyphSetProofer]: ../tools/variable/glyphset-proofer/
[Measurements]: ../tools/variable/measurements/
[VarGlyphAssistant]: ../tools/variable/varglyph-assistant/
[VarFontAssistant]: ../tools/variable/varfont-assistant/
[VarGlyphViewer]: ../tools/variable/varglyph-viewer/
