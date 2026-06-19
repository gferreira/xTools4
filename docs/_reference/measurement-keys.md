---
title     : Measurement keys
layout    : default
permalink : /reference/measurement-keys/
---

Proposal of an extensible syntax for measurement names.
{: .lead}

<span class='badge bg-danger rounded-0'>draft</span>

* Table of Contents
{:toc}

<style>
    td:nth-child(1) { width: 10em; }
    td:nth-child(2) { width: 15em; }
</style>


Context
-------

Because measurements are tied to variation axes, it is common for measurement names to follow the same convention of 4-letter tags (`XOPQ`, `XTRA`, etc). This system, however, works only until a certain level of complexity; as the number of axes/measurements increases (think of multi-script fonts), it gets harder to create meaningful names with only 4 letters – measurement names become cryptic, arbitrary, and hard to remember.

The [measurements format] itself allows strings of arbitrary length as measurement names. 

The syntax below is a more expressive alternative to the 4-letter tags. It was sketched as a response to a [proposal to store named values in the font lib], but could have other uses too.

[measurements format]: ../measurements-format
[proposal to store named values in the font lib]: http://github.com/unified-font-object/ufo-spec/issues/237#issuecomment-3094462560


Level 1
-------

The simpler 3-part syntax is sufficient for naming measurements in single-script fonts:

`measurement.direction.glyph`
{: .fs-4 }

This syntax can be used to name global measurements, case-specific measurements, and subgroup-specific measurements.

### Global measurements
{: .h5 }

| tag  | key             | description                  |
|------|-----------------|------------------------------|
| XOPQ | `stem.x.H`      | general x opaque             |
| YOPQ | `stem.y.H`      | general y opaque             |
| XTRA | `counter.x.H`   | general x transparent        |
| YTOS | `overshoot.y.O` | overshoot                    |
| XSHA | `hserif.x.H`    | general x horizontal serifs  |
| YSHA | `hserif.y.H`    | general y horizontal serif   |
| XSVA | `vserif.x.T`    | general x vertical serifs    |
{: .table .table-hover .mb-4 }

### Case-specific measurements
{: .h5 }

| tag  | key               | description              |
|------|-------------------|--------------------------|
| XTUC | `counter.x.H`     | x transparent uppercase  |
| XTLC | `counter.x.n`     | x transparent lowercase  |
| XTFI | `counter.x.zero`  | x transparent figures    |
{: .table .table-hover .mb-4 }

### Subgroup-specific measurements
{: .h5 }

| tag  | key           | description                       |
|------|---------------|-----------------------------------|
| XTUC | `counter.x.H` | x transparent uppercase straight  |
| XTUR | `counter.x.O` | x transparent uppercase round     |
| XTUD | `counter.x.V` | x transparent uppercase diagonal  |
{: .table .table-hover .mb-4 }


Level 2
-------

The 4-part syntax is intended for multi-script fonts. It extends the 3-part syntax above with a script prefix:

`script.measurement.direction.glyph`
{: .fs-4 }

### Script-specific measurements
{: .h5 }

| tag  | key                 | description               |
|------|---------------------|---------------------------|
| XOUC | `latin.stem.x.H`    | latin x opaque uppercase  |
| YOUC | `latin.stem.y.H`    | latin y opaque uppercase  |
| XOAR | `arabic.stem.x.??`  | arabic x opaque           |
| YOAR | `arabic.stem.y.??`  | arabic y opaque           |
| XOCH | `chinese.stem.x.??` | chinese x opaque          |
| YOCH | `chinese.stem.y.??` | chinese y opaque          |
{: .table .table-hover .mb-4 }

