---
title  : Overview
layout : page
order  : 1
---

A high-level introduction to hTools3.
{: .lead }


Patterns
--------

The toolkit is organized around 4 main *contexts* or *scopes* for performing tasks while working on fonts:

| scope                | description                                                      |
|----------------------|------------------------------------------------------------------|
| [batch](../batch)    | applying actions to multiple fonts at once                       |
| [font](../font)      | modifying various types of font-level data                       |
| [glyphs](../glyphs)  | applying actions to the selected glyphs and/or the current glyph |
| [glyph](../glyph)    | visualizing and modifying the current glyph                      |
{: .table }

These patterns are used to organize the tools internally in the code library and externally in the menu.

The *glyphs* group is the most numerous one. Tools in this group are further subdivided based on the type of font data they manipulate.


Interface
---------

The extension adds a *hTools3* entry to the main application menu, from which all individual dialogs are accessible. Custom keyboard shortcuts can be assigned to any dialog using the [RoboFont Preferences](http://robofont.com/documentation/workspace/preferences-window/short-keys/).

All dialogs in hTools3 inherit from the same base class and use the same interface and interaction defaults, which gives the toolkit a unified look and feel. Numerical input is done using a modified text input field which supports arrow keys and modifiers for increasing / decreasing the value interactively.

Tools which modify the current glyph offer an optional interactive preview. Some attributes of the preview can be adjusted in the [preferences](../preferences).

