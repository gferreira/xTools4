---
title     : Overview
layout    : page
order     : 1
permalink : /explanations/overview
---

A high-level introduction to xTools4.
{: .lead }

* Table of Contents
{:toc}


Contexts
--------

The xTools4 toolkit is organized around **5** main *contexts* or *scopes* for performing tasks while working on fonts:

| context                 | description                                                        |
|-------------------------|--------------------------------------------------------------------|
| [glyph](../glyph)       | tools for visualizing and editing the current glyph                |
| [glyphs](../glyphs)     | tools for applying actions to selected glyphs or the current glyph |
| [font](../font)         | tools for editing various kinds of font-level data                 |
| [batch](../batch)       | tools for applying actions to multiple fonts at once               |
| [variable](../variable) | tools for visualizing and editing variable font sources            |
{: .table .table-hover }

These contexts are used to organize the tools internally in the code library and externally in the menu.

The *glyphs* group is the most numerous one. Tools in this group are further subdivided based on the type of font data they manipulate.


Interface
---------

The extension adds a *xTools4* entry to the main application menu, from which all individual dialogs are accessible.

Custom keyboard shortcuts can be assigned to any dialog using the [RoboFont Preferences](http://robofont.com/documentation/workspace/preferences-window/short-keys/).

{% comment %}
All dialogs in xTools4 inherit from the same base class and use the same interface and interaction defaults, which gives the toolkit a unified look and feel. Numerical input is done using a modified text input field which supports arrow keys and modifiers for increasing / decreasing the value interactively.
{% endcomment %}

Tools which modify the current glyph offer an optional interactive preview. Some attributes of the preview can be adjusted in the [preferences](../reference/dialogs/preferences).
