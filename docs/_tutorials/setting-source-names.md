---
title     : Setting source names from measurements
layout    : default
permalink : /tutorials/setting-source-names
---

Parametric source names are set automatically from an actual measurement in the font.
{: .lead }

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Source naming scheme
--------------------

| family type         | source name (example)           | formatting syntax                                     |
|---------------------|---------------------------------|-------------------------------------------------------|
| single-style family | MyFamily_XOUC310.ufo            | `f'{familyName}_{parameter}{value}.ufo'`              |
| multi-style family  | MyFamily-SubFamily_XOUC310.ufo  | `f'{familyName}-{subFamily}_{parameter}{value}.ufo'`  |
{: .table .table-hover }


Setting source names automatically
----------------------------------

```python
p = MyController(folder, 'My New Typeface')
p.setSourceNamesFromMeasurements(preflight=True)
```
