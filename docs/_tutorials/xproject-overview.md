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

The “xProject model” is an attempt to systematize and automate the production of parametric variable fonts. It defines a set of data files which are used for various tasks during font development: measuring and automatically naming the sources, navigating the glyph set, building composite glyphs, automatically building the designspace, and much more.

This system is being developed for the production of [AmstelvarA2](#), and is now beginning to be used to produce other variable fonts too.

**This is all still highly experimental and unstable! Your feedback is welcome.**

### Why is automation needed?
{: .h5 }

- greater precision and consistency
- reduce repetitive tasks, focus on the design of the typeface
- more flexibility for changes during the development process
- handle a very large number (50+) of axes and sources


Example source folders
----------------------

### Single-style family
{: .h5 }

The example below shows a simple folder with parametric variable font sources, using the default xProject folder structure and naming conventions.

```
Sources
├── corners/
│   ├── opsz8_wdth50.ufo  (tuning sources)
│   ├── opsz8_wdth125.ufo
│   ├── opsz8_wght100_wdth50.ufo
│   └── ...
├── features/
│   └── MyFamily.fea
├── MyFamily.designspace
├── MyFamily_wght400.ufo  (default source)
├── MyFamily_XOPQ3.ufo    (parametric sources)
├── MyFamily_XOPQ305.ufo
├── MyFamily_XTRA54.ufo
├── MyFamily_XTRA496.ufo
├── MyFamily_YOPQ2.ufo
├── MyFamily_YOPQ96.ufo
├── ...
├── measurements.json
├── blends.json
├── MyFamily.roboFontSets
└── MyFamily.glyphConstruction
```

It is possible to use a different folder structure and file names by [subclassing the xProject object](#) and overriding individual attributes and methods.

### Multi-style family
{: .h5 }

The example below shows a family with two subfamilies, with two separate designspaces, managed with a single controller.

```
Sources
├── Roman/
│   ├── corners/                    (tuning sources)
│   ├── features/
│   ├── MyFamily-Roman.designspace
│   ├── MyFamily-Roman_wght400.ufo  (default source)
│   ├── MyFamily-Roman_XOPQ3.ufo    (parametric sources)
│   ├── ...
│   ├── measurements.json
│   ├── blends.json
│   ├── MyFamily-Roman.roboFontSets
│   └── MyFamily-Roman.glyphConstruction
└── Italic/
    ├── corners/                    (tuning sources)
    ├── features/
    ├── MyFamily-Italic.designspace
    ├── MyFamily-Italic_wght400.ufo (default source)
    ├── MyFamily-Italic_XOPQ3.ufo   (parametric sources)
    ├── ...
    ├── measurements.json
    ├── blends.json
    ├── MyFamily-Italic.roboFontSets
    └── MyFamily-Italic.glyphConstruction
```

Other folder structures and file naming systems are possible with some custom code. The system is designed to be flexible – you don’t need to force your idea into a certain format or structure, you can build your custom structure around it.


File formats
------------

### Designspace file
{: .h5 }

...

### Default source
{: .h5 }

The default source is the origin of the designspace. All other sources are created from it.

The default source is usually named `wght400`, and it contains quadratic contours with two off-curve points per curve segment.

### Measurements file
{: .h5 }

The measurements file defines a set of measurements which can be taken in the sources of a given designspace.

Each measurement is defined as a pair of points. Contour points are identified by their index.

There are *font-level measurements*, which are defined by key glyphs and represent the whole font; and there are *glyph-level measurements* for each glyph which is made out of contours (composite glyphs don’t have measurements).

The measurement definitions are stored in a JSON file, usually next to the designspace. The actual distances are not stored but measured in real-time for each source.

### Parametric sources
{: .h5 }

Each parametric source modifies only one parameter (measurement) of the default font.

Parametric source files are named with the actual measured value in the font. Such file names can be set automatically by the controller.

Some parametric sources may need to use an arbitrary scale, independent from a measurement (for example: `GRAD`). Handling of these special cases must be hard-coded in the controller.

Parametric sources are expected to have the same glyphset as the default (non-sparse sources).

There may be two parametric sources (min and max) for the same parameter, or just one (just min or just max).

### Smart sets file
{: .h5 }

The smart sets file contains various sets of glyph names, which can be used to group, filter and navigate the glyphs in a large font project.

The smart sets are stored in a `.roboFontSets` file, usually next to the designspace. Smart sets may contain glyphs which are not (yet) included in the fonts.

### Glyph construction file
{: .h5 }

The glyph construction file contains recipes in [Glyph Construction Language](#) for building composite glyphs from other glyphs. Most glyph recipes use anchors to align components to base glyph.

The glyph construction file has a `.glyphConstruction` extension, and is usually stored next to the designspace.

### Blends file
{: .h5 }

The blends file contains a definition of the blended axes, and the mappings from blended locations to parametric ones. A blended designspace with `opsz`, `wght` and `wdta axes typically contains locations for all 27 corners.

The blends data is stored in a JSON file, usually next to the designspace.

### Tuning sources
{: .h5 }

...

### Features
{: .h5 }

...
