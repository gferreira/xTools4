---
title     : Measurement scales and thresholds
layout    : default
permalink : /reference/measurement-scales-thresholds/
---

Measurement scales reveal the proportion between a given measurement and its parent value, font value, or default value.
{: .lead}

* Table of Contents
{:toc}


Measurement scales
------------------

### Parent scale

The **p-scale** (`A÷B`) is the scale of a font-level measurement (`A`) in relation to its parent measurement (`B`).

Example:

| ref.    | description            | name   | glyph | source  | value |
|---------|------------------------|--------|-------|---------|-------|
| `A`     | font-level measurement | `XOLC` | `n`   | current | 170   |
| `B`     | font-level measurement | `XOPQ` | `H`   | current | 180   |
| `A÷B`   | p-scale                |        |       |         | 0.944 |
{: .table .table-hover }

*“The general thickness of lowercase vertical stems is 94,4% of the general thickness of the uppercase vertical stems.”*

### Font scale
{: .mt-4 }

The **f-scale** (`A÷B`) is the scale of a glyph-level measurement (`A`) in relation to the font-level value of the same name (`B`).

Example:

| ref.    | description             | name   | glyph | source  | value |
|---------|-------------------------|--------|-------|---------|-------|
| `A`     | glyph-level measurement | `XOLC` | `u`   | current | 168   |
| `B`     | font-level measurement  | `XOLC` | `n`   | current | 170   |
| `A÷B`   | f-scale                 |        |       |         | 0.988 |
{: .table .table-hover }

*“The thickness of a vertical stem in **u** is 98,8% of the general lowercase vertical stem thickness, which is taken from the **n**.”*

### Default scale
{: .mt-4 }

The **d-scale** (`A÷B`) is the scale of a font- or glyph-level measurement (`A`) in relation to the same measurement in the default font (`B`).

Example:

| ref.    | description             | name   | glyph | source  | value |
|---------|-------------------------|--------|-------|---------|-------|
| `A`     | glyph-level measurement | `XOLC` | `u`   | current | 586   |
| `B`     | glyph-level measurement | `XOLC` | `u`   | default | 168   |
| `A÷B`   | d-scale                 |        |       |         | 3.488 |
{: .table .table-hover }

*“The thickness of a vertical stem in **u** is 348,8% thicker than that same stem in the default font.”*


Measurement thresholds
---------------------
{: .mt-4 }

Each measurement scale has a corresponding *threshold value* which can be used to validate a measurement against a reference value in the same font or in another font.

| scale   | threshold   | validation against                           |
|---------|------------|----------------------------------------------|
| p-scale | p-threshold | parent font-level measurement                |
| f-scale | f-threshold | font-level measurement                       |
| d-scale | d-threshold | default font- or glyph-level measurement     |
{: .table .table-hover }


Measurement validation
----------------------
{: .mt-4 }

Based on its threshold value, a scale can be in one of three value ranges in relation to its reference value.

Each value range can be represented by a different color, allowing visual validation in tables with multiple scales and measurements.

<table class='table table-hover'>
  <tr>
    <th>range</th>
    <th>color</th>
    <th>meaning</th>
  </tr>
  <tr>
    <td>equal</td>
    <td class='blue'>blue</td>
    <td>equal to the reference value</td>
  </tr>
  <tr>
    <td>within</td>
    <td class='green'>green</td>
    <td>different from the reference value, but within the threshold for this scale</td>
  </tr>
  <tr>
    <td>beyond</td>
    <td class='red'>red</td>
    <td>different from the reference value, and beyond the threshold for this scale</td>
  </tr>
</table>
