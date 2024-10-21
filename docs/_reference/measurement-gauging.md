---
title     : Measurement scales and tresholds
layout    : default
permalink : /reference/measurement-scales-tresholds/
---

Measurement scales reveal relationships between a given measurement and its parent, font, and default values.
{: .lead}

* Table of Contents
{:toc}


Measurement scales
------------------

### Parent scale

The **p-scale** (`A÷B`) is the scale of a font-level measurement (`A`) in relation to its parent measurement (`B`).

Example:

| ref.    | description                   | name   | glyph | source  | value |
|---------|-------------------------------|--------|-------|---------|-------|
| `A`     | font-level measurement        | `XOLC` | `n`   | current | 590   |
| `B`     | parent font-level measurement | `XOPQ` | `H`   | current | 621   |
| `A÷B`   | p-scale                       |        |       |         | 0.95  |
{: .table .table-hover }

*“The general thickness of lowercase vertical stems is 95% of the general thickness of the uppercase vertical stems.”*

### Font scale
{: .mt-4 }

The **f-scale** (`A÷B`) is the scale of a glyph-level measurement (`A`) in relation to the font-level value of the same name (`B`).

Example:

| ref.    | description             | name   | glyph | source  | value |
|---------|-------------------------|--------|-------|---------|-------|
| `A`     | glyph-level measurement | `XOLC` | `u`   | current | 586   |
| `B`     | font-level measurement  | `XOLC` | `n`   | current | 590   |
| `A÷B`   | f-scale                 |        |       |         | 0.993 |
{: .table .table-hover }

*“The thickness of a vertical stem in **u** is 99,3% of the general lowercase vertical stem thickness, which is taken from the **n**.”*

### Default scale
{: .mt-4 }

The **d-scale** (`A÷B`) is the scale of a font- or glyph-level measurement (`A`) in relation to the same measurement in the default font (`B`).

Example:

| ref.    | description             | name   | glyph | source  | value |
|---------|-------------------------|--------|-------|---------|-------|
| `A`     | glyph-level measurement | `XOLC` | `u`   | current | 586   |
| `B`     | glyph-level measurement | `XOLC` | `u`   | default | 170   |
| `A÷B`   | d-scale                 |        |       |         | 3.447 |
{: .table .table-hover }

*“The thickness of a vertical stem in **u** is 344,7% thicker than that same stem in the default font.”*


Measurement tresholds
---------------------

Each measurement scale has a corresponding *treshold value* which can be used to validate a measurement against a reference value in the same font or in another font.

| scale   | treshold   | validation against                           |
|---------|------------|----------------------------------------------|
| p-scale | p-treshold | parent font-level measurement                |
| f-scale | f-treshold | font-level measurement                       |
| d-scale | d-treshold | default font- or glyph-level measurement     |
{: .table .table-hover }


Measurement validation
----------------------

Based on the scale and treshold values, a measurement can be in one of three categories in relation to its reference value. Each category is represented by a different color.

<table class='table table-hover'>
  <tr>
    <th>color</th>
    <th>meaning</th>
  </tr>
  <tr>
    <td class='blue'>blue</td>
    <td>equal to</td>
  </tr>
  <tr>
    <td class='green'>green</td>
    <td>different but within treshold</td>
  </tr>
  <tr>
    <td class='red'>red</td>
    <td>different and beyond treshold</td>
  </tr>
</table>
