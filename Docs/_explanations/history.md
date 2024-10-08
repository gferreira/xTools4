---
title     : History of xTools4
layout    : page
order     : 2
permalink : /explanations/history
---

xTools4 is a fusion of [hTools3] and [variableValues] extensions, updated to the new [RoboFont 4] APIs: [Merz], [Subscriber], and [EZUI].
{: .lead}

[hTools3]: http://hipertipo.gitlab.io/htools3-extension/
[variableValues]: http://gferreira.github.io/fb-variable-values/
[RoboFont 4]: http://robofont.com/announcements/RoboFont-4.0/
[Merz]: http://robofont.com/documentation/topics/merz/
[Subscriber]: http://robofont.com/documentation/topics/subscriber/
[EZUI]: http://typesupply.github.io/ezui/


* Table of Contents
{:toc}


History of xTools4
------------------

...



History of variableValues
-------------------------

...


History of hTools
-----------------

### hTools

hTools started in 2005/06 while I was still a student at [TypeMedia]. We all used [FontLab Studio 5] at the time. At first, *hTools* was just the name of a folder where I started to collect [RoboFab] scripts while working and studying. At some point I learned how to create modules, and the *hTools* folder became a Python module from which I could `import` things. That was super useful, so I kept working on making it better.

This first version of hTools was never made public. The name of the module was inspired by the naming scheme used in RoboFab, with a letter prefix for object names (ex: `RFont`, `RGlyph`, etc). The *H* in hTools stands for [Hipertipo], as the tools were originally intended for my personal use only.

[TypeMedia]: http://typemedia.org/
[RoboFab]: http://robofab.org/
[FontLab Studio 5]: http://www.fontlab.com/font-editor/fontlab-studio-5/
[Hipertipo]: http://hipertipo.com/

### hTools2

RoboFont 1 was released in September 2011. I switched to it right away, and began (re)writing small tools which I needed for my work. A first version of hTools2 was made available under an open-source license in December. Nikola Djurek of [Typonine] commissioned me to create new tools and scripts which were added to the toolkit. The following year I was invited to make a [presentation] about hTools2 at the RoboThon conference – this motivated me to improve the code and write some documentation for users.

Over the next years, I continued to use hTools2 extensively in my own type design work, and kept adding new features as I needed them. Some designers and foundries (Typonine, [Underware], [Dinamo]) funded the development of individual new tools, others made donations to support the project ([Klim], [Blackletra]). I also received several contributions in the form of pull requests, bug reports and issues. <!-- *A big thanks to everyone who contributed to hTools2!* -->

[hTools2]: http://github.com/gferreira/hTools2/
[presentation]: https://vimeo.com/38502559
[Typonine]: http://typonine.com/
[Typotheque]: http://typotheque.com/
[Underware]: http://underware.com/
[Dinamo]: http://abcdinamo.com/
[Klim]: http://klim.co.nz/
[Blackletra]: http://blackletra.com/

### hTools3

[RoboFont 3] was released in July 2018. It introduced two big changes: switch from Python 2 to Python 3, and switch from the RoboFab API to the FontParts API. Most existing RF1 tools required small changes to work on RF3. I started making changes to hTools2 code in order to make it compatible with RF3, while still keeping it backwards-compatible with RF1. This involved adding a lot of conditionals to check for the current version – it worked, but the code became ugly and hard to maintain. At this point I decided to start over and work on a new future-oriented version of hTools, dropping support for RF1. The hTools2 code was declared ‘frozen’ and hTools3 development was initiated.

Nikola Djurek (now of [Typotheque]) contributed greatly to the initial work on hTools3. In a meeting at the KABK during the RoboThon conference in 2018, we made a long list of tools which should be included in the kit. Most [font] and [glyphs] tools were based on existing hTools2 tools, while the [batch] tools were all created from scratch using a new accordion-based interface. Nikola/Typotheque funded initial development and provided helpful testing and feedback.

I continued to work on hTools3 independently, improving the code and adding new tools as I needed them. A new set of [glyph] tools was included, containing tools to display special kinds of data while drawing – distances, angles, curvatures, etc. A lot of time was dedicated to making the code clear and maintainable, and to writing documentation. There are now two separate docs for hTools3: a high-level [user documentation] and a low-level [API documentation] for developers. Both docs are built automatically from the source code and are served through [GitLab Pages].

A beta version of hTools3 was made public in March 2020 as a compiled trial extension. The trial extension period, which was initially set for 3 months, was extended until the end of the year. Version 0.6.0, released on 31/12/2020, marked the start of the commercial distribution of hTools3. <!-- *Huge thanks to all users who bought a license!* -->

{% comment %}
- explain why hTools3 is not free & open-source like hTools2
{% endcomment %}

### hTools4

- [A roadmap for hTools4 (20 September 2021)](http://www.hipertipo.com/en/log/2021-09-20-hTools4-roadmap/)
- [hTools4 development postponed (01 January 2022)](http://www.hipertipo.com/en/log/2022-01-01-hTools4-postponed/)

[batch]: ../batch
[font]: ../font
[glyphs]: ../glyphs
[glyph]: ../glyph
[RoboFont 3]: http://robofont.com/documentation/RF3-changes/
[user documentation]: http://hipertipo.gitlab.io/htools3-extension/
[API documentation]: http://hipertipo.gitlab.io/hTools3/
[Jekyll]: http://jekyllrb.com/
[GitLab Pages]: http://docs.gitlab.com/ee/user/project/pages/
