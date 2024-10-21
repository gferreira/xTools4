---
title     : About xTools4
layout    : page
permalink : /explanations/about
---

xTools4 is a fusion of hTools3 and variableValues extensions, updated to the new RoboFont 4 APIs: Merz, Subscriber, and EZUI.
{: .lead}

* Table of Contents
{:toc}


[RoboFont 4], released in July 2021, introduces 3 new APIs:

- [Merz], a completely new drawing back-end based on Apple’s [Core Animation Layer] framework. It is significantly faster than the previous API, and has an object-oriented approach.
- [Subscriber], a new notification manager that is meant to work along with Merz. It makes subscribing to application events easier and more efficient.
- [Ezui], a new toolkit that makes it easier to build user interfaces. It’s built on top of and is fully interoperable with [vanilla].

RoboFont 3 tools still work in RoboFont 4, with some limitations such as blurry previews as slower performance.

[RoboFont 4]: http://robofont.com/announcements/RoboFont-4.0/
[Merz]: http://robofont.com/documentation/topics/merz/
[Subscriber]: http://robofont.com/documentation/topics/subscriber/
[EZUI]: http://typesupply.github.io/ezui/
[vanilla]: http://vanilla.robotools.dev/
[Core Animation Layer]: https://developer.apple.com/documentation/quartzcore


### VariableValues

VariableValues is an open-source extension to assist in the production of variable fonts. It contains tools to view and edit data in multiple designspace sources, validate source glyphs against a default font, measure glyph parameters, work with sparse sources, etc.

*While VariableValues still works in RoboFont 4, it was written using the old RoboFont 3 APIs, and does not take advantage of the new APIs introduced in RoboFont 4.*


### hTools3

hTools3 is a closed-source, commercial extension for RoboFont 3. It is a modular toolkit containing several small tools for basic font production tasks.

*While hTools3 still works in RoboFont 4, it was written using the old RoboFont 3 APIs, and does not take advantage of the new APIs introduced in RoboFont 4.*


### xTools4

xTools4 is a collection of expert tools for typeface design and font production in RoboFont 4.

xTools4 is a fusion of [hTools3] and [VariableValues] extensions, updated to the new [RoboFont 4] APIs: [Merz], [Subscriber], and [EZUI].

xTools4 is available as an open-source extension from the [xTools4 repository][xTools4] on GitHub.

<div class="card text-dark bg-light my-3 rounded-0">
<div class="card-header"> note</div>
<div class="card-body" markdown='1'>
xTools4 is a work in progress — not all tools have been converted to the new RF4 APIs yet.  

The status of each tool is indicated in its page in the [reference](../reference) by one of the following labels:  

<span class="badge text-bg-warning rounded-0 user-select-none">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  
<span class="badge text-bg-danger  rounded-0 user-select-none">RF3</span> RoboFont 3 code which does no longer work in RoboFont 4.  
<span class="badge text-bg-success rounded-0 user-select-none">RF4</span> Rewritten using the new RoboFont 4 APIs.  
<span class="badge text-bg-primary rounded-0 user-select-none">RF4</span> RoboFont 3 code which does not need to change for RoboFont 4.  

This documentation will be updated as more tools are updated or rewritten. Keep an eye on the [changelog](../changelog) for the latest changes.
{: .card-text }
</div>
</div>

[hTools3]: http://hipertipo.gitlab.io/htools3-extension/
[variableValues]: http://gferreira.github.io/fb-variable-values/
[xTools4]: http://github.com/gferreira/xTools4
