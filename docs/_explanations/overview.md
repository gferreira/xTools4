---
title     : Overview
layout    : page
permalink : /explanations/overview
---

A high-level introduction to the xTools4 toolkit.
{: .lead }

* Table of Contents
{:toc}


Modular
-------

xTools4 contains many small and very specific tools that are intended to be used together. 

This approach is inspired by the [Unix design philosophy](http://en.wikipedia.org/wiki/Unix_philosophy).


Contexts
--------

The xTools4 toolkit is organized around **5** main *contexts* or *scopes* for performing tasks while working on fonts:

| context                                  | description                                                         |
|------------------------------------------|---------------------------------------------------------------------|
| [glyph](../reference/tools/glyph)        | tools for visualizing and editing the current glyph                 |
| [glyphs](../reference/tools/glyphs)      | tools for applying actions to selected glyphs or the current glyph  |
| [font](../reference/tools/font)          | tools for editing various kinds of font-level data                  |
| [batch](../reference/tools/batch)        | tools for applying actions to multiple fonts at once                |
| [variable](../reference/tools/variable)  | tools for visualizing and editing variable font sources             |
{: .table .table-hover }

These contexts are used to organize the tools internally in the code library and externally in the menu.

The *glyphs* group is the largest one. Tools in this group are further subdivided based on the type of font data they manipulate (for example *anchors*, *interpolation*, *layers*, etc).


Interface
---------

The extension adds a *xTools4* entry to the main application menu, from which all individual dialogs are accessible.

The interface of all tools is designed to be space-efficient. All *glyph* and *glyphs* windows have the same width and can be tiled on the side of the screen without taking up too much space.

Custom keyboard shortcuts can be assigned to any dialog using the [RoboFont Preferences](http://robofont.com/documentation/workspace/preferences-window/short-keys/).

Tools which modify the current glyph offer an optional interactive preview. Some attributes of the preview can be adjusted in the [preferences](../reference/tools/preferences).
