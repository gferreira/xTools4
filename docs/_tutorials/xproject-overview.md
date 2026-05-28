---
title     : Overview of the xProject model
layout    : default
permalink : /tutorials/xproject-overview/
---

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Introduction
------------

The “xProject model” is an attempt to systematize and automate the production of parametric variable fonts.

The model consists of a standard set of data files, and a Python object to manage these files and perform various tasks during font development. This is not unlike UFO (data format) and `RFont` (Python object).

These are some of the tasks handled by the xProject controller:

- measuring and automatically naming UFO sources
- automatically building the designspace from sources
- blending typographic styles from parametric axes
- cleaning up and normalizing UFO sources
- copying default data to all other sources
- navigating and filtering the glyph set
- building composite glyphs
- generating different kinds of proofs
- building variable fonts

The `xProject` object provides a basic set of functions which are essential to any parametric variable font project. Project-specific attributes and behavior can be added by subclassing and modifying this object.

This system was originally developed for the production of [AmstelvarA2], and is now being refined and expanded for use in other projects.

[AmstelvarA2]: http://github.com/googlefonts/amstelvar-avar2

### Why is automation needed?
{: .h5 }

All general reasons for employing automation in the production of complex font projects apply:

- greater precision and consistency
- reduce repetitive tasks, focus on typeface design
- more flexibility for changes during the development process
- handle a very large number of glyphs, axes and sources

### Control glyphs as single source of truth
{: .h5 }

Parametric variable fonts introduce one additional challenge: keeping the parametric source names and designspace locations in synch with the actual measurements in the font.

In xProject, the control glyphs are the [single source of truth]; source names and locations are derived automatically from them. This ensures that the parametric system is consistent and the numbers are meaningful.

[single source of truth]: http://en.wikipedia.org/wiki/Single_source_of_truth


File formats
------------

<style>
.icon { width: 128px; float: right; margin-left: 2em; }
</style>

### Designspace file
{: .h5 }

![]({{ site.url }}/images/icons/designspace.png){: .icon }

The designspace file describes the complete font variation space, with all parametric axes and sources, blended axes, mappings, and everything needed to build a parametric variable font.

In xProject, the designspace file is not edited directly – it is built by the controller using data assembled from various source files. This automated approach ensures that font names and parametric locations stay in synch with the actual measurements in the font.

### Default source
{: .h5 }

![]({{ site.url }}/images/icons/ufo.png){: .icon }

The default source is the origin of the designspace. All other sources are created from it.

The default source is usually named `wght400`. It contains quadratic contours with two off-curve points per curve segment.

Various kinds of data are copied from the default to all other sources: glyph order, unicodes, features, font info, etc.

### Measurements file
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The measurements file defines a set of measurements which can be taken from the sources of a given designspace.

Each measurement is defined as a pair of points. Contour points are identified by their index. Additional reference points (glyph margins, vertical metrics) are identified by one-letter codes.

There are *font-level measurements*, which are defined by key glyphs and represent the whole font; and there are *glyph-level measurements* for each glyph which is made out of contours (composite glyphs don’t have measurements).

The measurement definitions are stored in a JSON file, usually next to the designspace. The actual distances are not stored but measured in real-time for each source.

### Parametric sources
{: .h5 }

![]({{ site.url }}/images/icons/ufo.png){: .icon }

Each parametric source modifies only one parameter (measurement) of the default font.

Parametric source files are named with the actual measured value in the font. Such file names can be set automatically by the controller.

Some parametric sources may need to use an arbitrary scale, independent from a measurement (for example: `GRAD`). Handling of these special cases must be hard-coded in the controller.

Parametric sources are expected to have the same glyphset as the default (non-sparse sources).

There may be two parametric sources (min and max) for the same parameter, or just one (just min or just max).

### Blends file
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The blends file contains a definition of the blended axes, and the mappings from blended styles to parametric locations. A typical blended designspace with `opsz`, `wght`, `wdth` axes contains mappings for all 27 corners.

The blends data is stored in a JSON file, usually next to the designspace.

### Tuning sources
{: .h5 }

...

### Smart sets file
{: .h5 }

![]({{ site.url }}/images/icons/smartsets.png){: .icon }

The smart sets file contains various sets of glyph names, which can be used to group, filter and navigate the glyphs in a large font project.

The smart sets are stored in a `.roboFontSets` file, usually next to the designspace. Smart sets may contain glyphs which are not (yet) included in the fonts.

### Glyph construction file
{: .h5 }

![]({{ site.url }}/images/icons/file.png){: .icon }

The glyph construction file contains recipes in [Glyph Construction Language](#) for building composite glyphs from other glyphs. Most glyph recipes use anchors to align components to base glyph.

The glyph construction file has a `.glyphConstruction` extension, and is usually stored next to the designspace.

### Features file
{: .h5 }

![]({{ site.url }}/images/icons/fea.png){: .icon }

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





