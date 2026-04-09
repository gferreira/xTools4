---
title     : Creating parametric sources from a default
layout    : default
permalink : /tutorials/creating-parametric-sources/
---

<span class='badge bg-warning rounded-0'>draft</span>


### Creating new sources using the controller
{: .h5 }

```python
p = xProject(folder, 'My New Typeface')
p.createParametricSources(['XOPQ', 'YOPQ', 'XTRA'], minSource=True, maxSource=True)
```

- XOPQmin.ufo, XOPQmax.ufo
- YOPQmin.ufo, YOPQmax.ufo
- XTRAmin.ufo, XTRAmax.ufo


### Notes about individual parameters
{: .h5 }

- [XOPQ](XOPQ)
- [XTRA](XTRA)
- [YOPQ](YOPQ)
- [YTRA](#)
- [XTSP](#)
- [XSHA](#)
- [YSHA](#)
- [XQUC](#)
