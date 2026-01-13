---
title     : History of xTools4
layout    : page
permalink : /explanations/history
---

xTools4 is a fusion of hTools3 and variableValues extensions, updated to the new RoboFont 4 APIs.
{: .lead}

* Table of Contents
{:toc}


RoboFont 4
----------

[RoboFont 4], released in July 2021, introduces 3 new APIs:

- [Merz], a completely new drawing back-end based on Apple’s [Core Animation Layer] framework. It is significantly faster than the previous API, and has an object-oriented approach.
- [Subscriber], a new notification manager that is meant to work along with Merz. It makes subscribing to application events easier and more efficient.
- [Ezui], a new toolkit that makes it easier to build user interfaces. It’s built on top of and is fully interoperable with [vanilla].

RoboFont 3 tools still work fine in RoboFont 4, with small limitations such as blurry previews.

[RoboFont 4]: http://robofont.com/announcements/RoboFont-4.0/
[Merz]: http://robofont.com/documentation/topics/merz/
[Subscriber]: http://robofont.com/documentation/topics/subscriber/
[EZUI]: http://typesupply.github.io/ezui/
[vanilla]: http://vanilla.robotools.dev/
[Core Animation Layer]: https://developer.apple.com/documentation/quartzcore


VariableValues
--------------

VariableValues is an open-source extension to assist in the production of variable fonts. It contains tools to view and edit data in multiple designspace sources, validate source glyphs against a default font, measure glyph parameters, work with sparse sources, etc.

*While VariableValues still works in RoboFont 4, it was written using the old RoboFont 3 APIs, and does not take advantage of the new APIs introduced in RoboFont 4.*


hTools3
-------

hTools3 is a closed-source, commercial extension for RoboFont 3. It is a modular toolkit containing several small tools for basic font production tasks.

*While hTools3 still works in RoboFont 4, it was written using the old RoboFont 3 APIs, and does not take advantage of the new APIs introduced in RoboFont 4.*


[hTools3]: http://hipertipo.gitlab.io/htools3-extension/
[variableValues]: http://gferreira.github.io/fb-variable-values/
[xTools4]: http://github.com/gferreira/xTools4
