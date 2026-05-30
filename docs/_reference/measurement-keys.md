---
title     : Measurement keys
layout    : default
permalink : /reference/measurement-keys/
---

Proposal of an extensible syntax for measurement keys.
{: .lead}

<span class='badge bg-danger rounded-0'>draft</span>

* Table of Contents
{:toc}

<style>
    td:nth-child(1) { width: 10em; }
</style>


Context
-------

- beyond a certain level of complexity, 4-letter naming system makes it hard to create meaningful parameter names
- [UFO proposal] to store named values in the font lib, with a focus on stems
- it would be useful for us to store measurements in the font lib too

The syntax below started as a counter-proposal. The main ideas behind it are:

- allow the creation of other measurements (not just stems)
- allow different levels of specificity

[UFO proposal]: http://github.com/unified-font-object/ufo-spec/issues/237#issuecomment-3094462560


Syntax
------

`script.measurement.direction.glyph`
{: .fs-4 }


Level 1
-------

Font-wide parametric axes.

| tag  | key           |
|------|---------------|
| XOPQ | `stem.x`      |
| YOPQ | `stem.y`      |
| XTRA | `counter.x`   |
| YTOS | `overshoot.y` |
| XSHA | `hserif.x`    |
| YSHA | `hserif.y`    |
| XSVA | `vserif.x`    |
{: .table .mb-4 }


```python
font.lib['com.xTools4.measurements'] = {
    'stem.x'      : 89,
    'stem.y'      : 31,
    'counter.x'   : 299,
    'overshoot.y' : 22,
    'hserif.x'    : 103,
    'hserif.y'    : 31,
    'vserif.x'    : 25,
}
```


Level 2
-------

Splits font-wide axes into cases.

| tag  | key          |
|------|--------------|
| XOUC | `stem.x.H`   |
| XOLC | `stem.x.n`   |
| XOFI | `stem.x.one` |
{: .table }

```python
font.lib['com.xTools4.measurements'] = {
    'stem.x.H'   : 89,
    'stem.x.n'   : 69,
    'stem.x.one' : 74,
}
```


Level 3
-------

Splits cases into shape groups.

| tag  | key           |
|------|---------------|
| XTUC | `counter.x.H` |
| XTUR | `counter.x.O` |
| XTUD | `counter.x.V` |
{: .table }

```python
font.lib['com.xTools4.measurements'] = {
    'counter.x.H' : 299,
    'counter.x.O' : 459,
    'counter.x.V' : 380,
}
```

Level 4
-------

Splits axes into scripts (with prefix).

| tag  | key                       |
|------|---------------------------|
| ???? |  `latin.counter.x.etc`    |
| ???? |  `cyrillic.counter.x.etc` |
| ???? |  `greek.counter.x.etc`    |
{: .table }

