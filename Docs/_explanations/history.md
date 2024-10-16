---
title     : History of xTools4
layout    : page
order     : 2
permalink : /explanations/history
---

xTools4 is a fusion of hTools3 and variableValues extensions, updated to the new RoboFont 4 APIs: Merz, Subscriber, and EZUI.
{: .lead}

* Table of Contents
{:toc}


### xTools4

xTools4 is a collection of expert tools for typeface design and font production in RoboFont 4.

xTools4 is a fusion of [hTools3] and [variableValues] extensions, updated to the new [RoboFont 4] APIs: [Merz], [Subscriber], and [EZUI].

xTools4 is available under an open-source license from the [xTools4] repository on GitHub.

[hTools3]: http://hipertipo.gitlab.io/htools3-extension/
[variableValues]: http://gferreira.github.io/fb-variable-values/
[RoboFont 4]: http://robofont.com/announcements/RoboFont-4.0/
[Merz]: http://robofont.com/documentation/topics/merz/
[Subscriber]: http://robofont.com/documentation/topics/subscriber/
[EZUI]: http://typesupply.github.io/ezui/
[xTools4]: http://github.com/gferreira/xTools4

### RoboFont 4

RoboFont 4, released in July 2021, introduces 3 new APIs:

- Merz, a completely new drawing back-end based on Apple’s Core Animation Layer framework. It is significantly faster than the previous API, and has an object-oriented approach.
- Subscriber, a new notification manager that is meant to work along with Merz. It makes subscribing to application events easier and more efficient.
- Ezui, a new toolkit that makes it easier to build user interfaces. It’s built on top of and is fully interoperable with [vanilla].

### VariableValues

[VariableValues] is an open-source extension developed since 2022 to assist in variable font production projects for FontBureau. It contains tools to view and edit data in multiple designspace sources, tools to validate source glyphs against a default font, tools to measure glyph parameters, tools to work with sparse sources, etc.

While VariableValues works on RoboFont 4, it was written using the old RoboFont3 APIs.

### hTools3





- [History of hTools](http://hipertipo.gitlab.io/htools3-extension/history/)
- [A roadmap for hTools4 (20 September 2021)](http://www.hipertipo.com/en/log/2021-09-20-hTools4-roadmap/)
- [hTools4 development postponed (01 January 2022)](http://www.hipertipo.com/en/log/2022-01-01-hTools4-postponed/)
