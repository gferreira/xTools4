---
title     : Overview of the xProject model
layout    : default
permalink : /tutorials/xproject-overview/
---

Introducing the xProject data model and scripting API.
{: .lead }

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Introduction
------------

The “xProject model” is an attempt to systematize and automate the production of parametric variable fonts (avar2).

The model consists of a standard set of data files, and a Python object to manage these files and perform various tasks during font development. This is not unlike [UFO] (data format) and [RFont] (Python object).

[UFO]: http://unifiedfontobject.org/
[RFont]: http://fontparts.robotools.dev/en/stable/objectref/objects/font.html

### Tasks of the xProject controller
{: .h5 }

- measuring and automatically naming UFO sources
- automatically building the designspace from source files
- blending typographic styles from parametric axes
- cleaning up and normalizing UFO sources
- copying data from the default to all other sources
- navigating and filtering the glyph set
- building and validating composite glyphs
- generating different kinds of PDF proofs
- building variable fonts and instances

### A base object providing core attributes and functions
{: .h5 }

The `xProject` object provides an [API][xProject API] for core attributes and functions, streamlining the development of any parametric variable font. In this method, the source data is stored in human-readable formats which are easy to edit, and the designspace is built automatically by the controller. Project-specific attributes and behavior are added by subclassing `xProject` and modifying the controller.

This system was originally developed for the production of [AmstelvarA2], and is now being refined and expanded for use in other projects. We are also developing [Computer Modern avar2] as a demo project for this documentation.

[xProject API]: ../../reference/xproject/
[AmstelvarA2]: http://github.com/googlefonts/amstelvar-avar2
[Computer Modern avar2]: http://github.com/gferreira/computer-modern-avar2

### Control glyphs as the single source of truth
{: .h5 }

One of the main challenges in the production of parametric variable fonts is keeping the parametric source names and designspace locations in synch with the actual measurements in the font.

In xProject, the control glyphs are the [single source of truth]; source names and locations are derived automatically from them. This ensures that the parametric system is consistent and the numbers are meaningful.

[single source of truth]: http://en.wikipedia.org/wiki/Single_source_of_truth

### Advantages of designspace automation
{: .h5 }

- greater precision and consistency
- reduce repetitive tasks, focus on typeface design
- more flexibility for changes during the development process
- handle a very large number of glyphs, axes and sources




<!--
### A pilot system
{: .h5 }

> Where a new system concept or new technology is used, one has to build a system to throw away, for even the best planning is not so omniscient as to get it right the first time. Hence plan to throw one away; you will, anyhow.  
>
> — Fred Brooks, The Mythical Man-Month

xProject is a [pilot system], a first implementation that will eventually lead to a complete redesign of the system.

[pilot system]: https://en.wikipedia.org/wiki/The_Mythical_Man-Month#The_pilot_system
-->


File formats
------------

<style>
.icon { width: 128px; float: right; margin-left: 2em; }
</style>

### Designspace file (required)
{: .h5 }

![]({{ site.url }}/images/icons/designspace.png){: .icon }

The designspace file describes the complete font variation space, with all parametric axes and sources, blended axes, mappings, and everything needed to build a parametric variable font.

In xProject, the designspace file is not edited directly – it is built by the controller using data assembled from various source files. This automated approach ensures that font names and parametric locations stay in synch with the actual measurements in the font.

### Default source (required)
{: .h5 }

![]({{ site.url }}/images/icons/ufo.png){: .icon }

The default source is the origin of the designspace. All other sources are created from it.

The default source is usually named `wght400`. It contains quadratic contours with two off-curve points per curve segment.

Various kinds of data are copied from the default to all other sources: glyph order, unicodes, features, font info, etc.

### Measurements file (required)
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The measurements file defines a set of measurements which can be taken from the sources of a given designspace.

Each measurement is defined as a pair of points. Contour points are identified by their index. Additional reference points (glyph margins, vertical metrics) are identified by one-letter codes.

There are *font-level measurements*, which are defined by key glyphs and represent the whole font; and there are *glyph-level measurements* for each glyph which is made out of contours (composite glyphs don’t have measurements).

The measurement definitions are stored in a JSON file, usually next to the designspace. The actual distances are not stored but measured in real-time for each source.

### Parametric sources (required)
{: .h5 }

![]({{ site.url }}/images/icons/ufo.png){: .icon }

Each parametric source modifies only one parameter (measurement) of the default font.

Parametric source files are named with the actual measured distance in the font (as a permille value). For example: `XOPQ310.ufo` or `MyFamily_XOPQ310.ufo`. Such file names are set automatically by the controller.

Some parametric sources may need to use an arbitrary scale, independent from a measurement (for example: `GRAD`). Handling of these special cases must be added to the project’s controller.

Parametric sources are expected to have the same glyphset as the default (non-sparse sources).

There may be two parametric sources (both min and max) for the same parameter, or just one (just min or just max).

### Smart sets file (required)
{: .h5 }

![]({{ site.url }}/images/icons/smartsets.png){: .icon }

The smart sets file contains various sets of glyph names, which can be used to group, filter and navigate the glyphs in a large font project.

The smart sets are stored in a `.roboFontSets` file, usually next to the designspace. Smart sets may contain glyphs which are not (yet) included in the fonts.

### Glyph construction file (required)
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The glyph construction file contains recipes in [Glyph Construction Language](#) for building composite glyphs from other glyphs. Most glyph recipes use anchors to align components to base glyph.

The glyph construction file has a `.glyphConstruction` extension, and is usually stored next to the designspace.

### Features file (required)
{: .h5 }

![]({{ site.url }}/images/icons/fea.png){: .icon }

...

### Blends file (required)
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The blends file contains a definition of the blended axes, and the mappings from blended styles to parametric locations. A typical blended designspace with `opsz`, `wght`, `wdth` axes contains mappings for all 27 corners.

The blends data is stored in a JSON file, usually next to the designspace.

### Tuning sources (optional)
{: .h5 }

...



Source folder examples
----------------------

### Single-style family
{: .h5 }

The simplest example is a simple folder with parametric sources, using the default xProject folder structure and file naming scheme.

```
Sources
├── MyFamily.designspaces         <-- designspace file
├── MyFamily_wght400.ufo          <-- default source
├── MyFamily_XOPQ3.ufo            <-- parametric sources
├── MyFamily_XOPQ305.ufo
├── MyFamily_XTRA54.ufo
├── MyFamily_XTRA496.ufo
├── MyFamily_YOPQ2.ufo
├── MyFamily_YOPQ96.ufo
├── ...
├── measurements.json             <-- measurements file
├── blends.json                   <-- blends file
├── MyFamily.roboFontSets         <-- smart sets file
├── MyFamily.glyphConstruction    <-- glyph construction file
├── features/
│   └── MyFamily.fea              <-- features file
└── tuning/
    ├── opsz8_wdth50.ufo          <-- tuning sources (optional)
    ├── opsz8_wdth125.ufo
    ├── opsz8_wght100_wdth50.ufo
    └── ...
```

Different folder structure and file names can be used by subclassing the `xProject` object and overriding individual attributes and methods.

### Multi-style family
{: .h5 }

The example below shows a family with two subfamilies, with two separate designspaces, managed with a single controller.

```
Sources
├── Roman/
│   ├── MyFamily-Roman.designspaces
│   ├── MyFamily-Roman_wght400.ufo
│   ├── MyFamily-Roman_XOPQ3.ufo
│   ├── ...
│   ├── measurements.json
│   ├── blends.json
│   ├── MyFamily-Roman.roboFontSets
│   ├── MyFamily-Roman.glyphConstruction
│   ├── features/
│   └── tuning/
└── Italic/
    ├── MyFamily-Italic.designspaces
    ├── MyFamily-Italic_wght400.ufo
    ├── MyFamily-Italic_XOPQ3.ufo
    ├── ...
    ├── measurements.json
    ├── blends.json
    ├── MyFamily-Italic.roboFontSets
    ├── MyFamily-Italic.glyphConstruction
    ├── features/
    └── tuning/
```

Other folder structures and file naming systems are possible with some custom code. The system is designed to be flexible – you don’t need to force your idea into a certain format or structure, you can build your custom structure around it.


Controller examples
-------------------

### Single-style family
{: .h5 }

```python
from xTools4.modules.xproject import xProject

class MyFamilyController(xProject):
    pass

p = MyFamilyController('/Users/gferreira/fontbureau/MyFamily', 'My Family')
p.printSettings()
```

### Multi-style family
{: .h5 }

```python
import os
from xTools4.modules.xproject import xProject

class MyFamilySubfamilyController(xProject):

    def __init__(self, folder, familyName, subFamily):
        self.baseFolder = folder
        self.familyName = familyName
        self.subFamily = subFamily

    @property
    def designspaceFile(self):
        return f"{self.familyName}-{self.subFamily}.designspace".replace(' ', '')

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, self.sourcesFolderName, self.subFamily)

    @property
    def defaultSourcePath(self):
        return os.path.join(self.sourcesFolder, f"{self.familyName}-{self.subFamily}_{self.defaultName}.ufo".replace(' ', ''))

    @property
    def varFontFile(self):
        return f"{self.familyName}-{self.subFamily}_avar2.ttf".replace(' ', '')

p = MyFamilySubfamilyController('/Users/gferreira/fontbureau/MyFamily', 'My Family', 'Roman')
p.printSettings()
```





