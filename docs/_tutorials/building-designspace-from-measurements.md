---
title     : Building parametric designspace
layout    : default
permalink : /tutorials/building-designspace-from-measurements/
---

Using the controller to automatically build a parametric designspace from measurements.
{: .lead }

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Building the designspace with the controller
--------------------------------------------

```python
p = MyController(folder, 'My Family')

p.parametricAxes = ['XOPQ', 'YOPQ', 'XTRA', 'XTSP']
p.buildDesignspace()
```

### Designspace build steps
{: .h5 }

By default, calling the `buildDesignspace` method will create a new designspace and perform the following actions:

- add blended axes
- add parametric axes
- add tuning axes (if available)
- add blend mappings
- add default source
- add parametric sources
- add tuning sources (if available)
- add custom keys to lib


Creating your own designspace builder
-------------------------------------

The default build designspace procedure can be overwritten by subclassing `xProject` and adding a custom `buildDesignspace` to the controller.

```python
from xTools4.modules.xproject import xProject

class MyController(xProject):

    @property
    def buildDesignspace(self):
        # add your own code here

p = MyController()
p.buildDesignspace()
```
