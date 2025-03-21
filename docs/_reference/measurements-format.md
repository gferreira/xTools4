---
title     : Measurements format
layout    : default
permalink : /reference/measurements-format/
---

A data format to store definitions of font-level and glyph-level measurements.
{: .lead}

* Table of Contents
{:toc}


Data structure
--------------

A measurement establishes a link between two points and allows us to calculate the distance between them.

The order of the points matters: a measurement can be positive or negative.

### Font-level measurements

- A font may contain multiple font-level measurements.
- Font measurement names must be unique.
- The order of the font measurements matters.

| attribute   | description                                            |
|-------------|--------------------------------------------------------|
| name        | name of the measurement                                |
| glyph 1     | name of the glyph containing the 1st measurement point |
| point 1     | index or shortcut of 1st measurement point             |
| glyph 2     | name of the glyph containing the 2nd measurement point |
| point 2     | index or shortcut of 2nd measurement point             |
| direction   | direction of measurement                               |
| parent      | parent measurement (optional)                          |
| description | description of this measurement (optional)             |
{: .table .table-hover }

{% comment %}
<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
The attribute *glyph 2* can probably be deprecated. It was available to allow measurement of overshoots using a straight shape from one glyph and a round shape from another glyph. Overshoot measurement is now possible using [reference points](#reference-points).
{: .card-text }
</div>
</div>
{% endcomment %}

### Glyph-level measurements

- A glyph may contain multiple glyph-level measurements.
- Glyph measurement names are usually related to font-level measurements.
- Glyph measurement names must **not** be unique.
- Glyph measurement identifiers are created from the point indexes.
- The order of glyph measurements follows the order of font measurements.

| attribute | description                                            |
|-----------|--------------------------------------------------------|
| name      | name of the measurement                                |
| point 1   | index or shortcut of 1st measurement point             |
| point 2   | index or shortcut of 2nd measurement point             |
| direction | direction of measurement                               |
{: .table .table-hover }

### Direction keys

The direction of measurement must be one of the following characters:

| characters | description            |
|------------|------------------------|
| x          | horizontal measurement |
| y          | vertical measurement   |
| a          | angled measurement     |
{: .table .table-hover }

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
The sign of the measured value indicates its direction. Some measurements are by definition negative, for example the descender value or a bottom overshoot.
{: .card-text }
</div>
</div>


### Point IDs

Points can be identified by a **number** (point index) or a **letter** (reference point).

#### Point indexes

Contour points are identified by their index (an integer).

#### Reference points

Font-level vertical metrics values are also available using the following shortcut characters:

| character | description | x             | y                     |
|-----------|-------------|---------------|-----------------------|
| A         | ascender    | `0`           | `font.info.ascender`  |
| B         | baseline    | `0`           | `0`                   |
| C         | cap height  | `0`           | `font.info.capHeight` |
| D         | descender   | `0`           | `font.info.descender` |
| X         | x-height    | `0`           | `font.info.xHeight`   |
{: .table .table-hover }


Python example
--------------

The key for font-level measurements is the name of the measurement.

```python
fontMeasurements = {
    'XTUC' : {
        'glyph 1'   : 'H',
        'point 1'   : 11,
        'glyph 2'   : 'H',
        'point 2'   : 8,
        'direction' : 'x',
        'parent'    : 'XTRA',
    },
    # more font-level measurements here ...
}
```

The key for glyph-level measurements is an identifier created from the two point IDs.

```python
glyphMeasurements = {
    "a" : {
      f'{ptID1} {ptID2}' : {
          'name'      : 'XTRA',
          'direction' : 'x',
      },
      # more glyph-level measurements here ...
    },
    # more glyphs here ...
}
```

<div class="card bg-light my-3 rounded-0">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
The current glyph-level measurement format has one limitation: a pair of points can only have one measurement attached to it. It should be possible to have both x and y measurements for same pair of points though, for example the width and height of a serif. The format will be updated to address this.
{: .card-text }
</div>
</div>


JSON format
-----------

Measurements can be stored in standalone JSON files using the format below.

The same set of measurement definitions can be used to measure all sources in a designspace.

```json
{
  "font": {
    "XTUC": {
      "direction": "x",
      "glyph 1": "H",
      "point 1": "11",
      "glyph 2": "H",
      "point 2": "8",
      "parent": "XTRA"
    },
    /* more font-level measurements here ... */
  },
  "glyphs": {
    "n": {
      "0 20": {
        "direction": "x",
        "name": "XOLC"
      },
      "11 12": {
        "direction": "x",
        "name": "XOLC"
      },
      "13 19": {
        "direction": "x",
        "name": "XTLC"
      },
      /* more glyph-level measurements here ... */
    },
    /* more glyphs here ... */
  },
}
```
