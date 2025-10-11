---
title     : Rounding format
layout    : default
permalink : /reference/rounding-format/
---

A data format to store points which are modified to produce rounded sources.
{: .lead}


Python example
--------------

```python
{
    'D' : {
        'corners' : [0, 1],
    },
    'E' : {
        'caps' : [(2, 3), (10, 11), (6, 7)],
        'corners' : [0, 1],
    },
    'I' : {
        'caps' : [(1, 2), (3, 0)],
    },
    'T' : {
        'caps' : [(4, 5), (6, 7), (3, 0)],
    },
}

```
