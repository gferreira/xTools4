---
title     : Creating a controller object
layout    : default
permalink : /tutorials/creating-controller
---

The controller object is responsible for building and managing the designspace.
{: .lead }

<span class='badge bg-warning rounded-0'>draft</span>

* Table of Contents
{:toc}


Introduction
------------

In parametric fonts, the designspace is tighly coupled to various measurements (parameters) in the fonts.

During the design stage, the glyph shapes are still changing all the time, and if a measurement changes the parametric designspace must change accordingly.

### Why a controller is needed
{: .h5 }

As designspaces get larger, it becomes harder and harder to keep track and update these relationships by hand.

The controller object takes care of building and managing the designspace, ensuring that file names are consistent and parametric values are always correct and up-do-date.

### Duties of the controller
{: .h5 }

- create new parametric sources
- set source names automatically from measurements
- clean-up and normalize UFO sources
- build the parametric designspace from measurements
- ...

A documentation of the xProject API is on its way.


The controller object
---------------------

The `xProject` controller is a base object which is meant to be subclassed and customized for each project. It provides a basic API for gathering different kinds of data from multiple files and building a parametric variable font from it.

```python
from xTools4.modules.xproject import xProject

folder = 'MyFolder/'

p = xProject(folder, 'My Family')
p.printSettings()
```

### Default project settings
{: .h5 }

| base folder | MyFolder/ |
| family name | My New |
| designspace file | MyFamily.designspace |
| designspace path | MyFolder/Sources/MyFamily.designspace |
| sources folder name | Sources |
| sources folder path | MyFolder/Sources |
| default name | wght400 |
| default path | MyFolder/Sources/MyFamily_wght400.ufo |
| measurements file | measurements.json |
| measurements path | MyFolder/Sources/measurements.json |
| smart sets file | MyFamily.roboFontSets |
| smart sets path | MyFolder/Sources/MyFamily.roboFontSets |
| blends file | blends.json |
| blends path | MyFolder/Sources/blends.json |
| tuning folder name | corners |
| tuning folder path | MyFolder/Sources/corners |
| instances folder name | instances |
| instances folder path | MyFolder/Sources/instances |
| fonts folder name | Fonts |
| fonts folder | MyFolder/Fonts |
| variable font file | MyFamily.ttf |
| variable font path | MyFolder/Fonts/MyFamily.ttf |
{: .table .table-hover }


Creating a custom controller
----------------------------

To create a custom controller for your project, start by subclassing `xProject`. In the example below, we are adding a *subfamily* argument to the project constructor, and changing the designspace file name and the source folder path to accomodate multiple subfamilies.

```python
from xTools4.modules.xproject import xProject

class MyController(xProject):

    def __init__(self, folder, familyName, subFamily):
        self.baseFolder = folder
        self.familyName = familyName
        self.subFamily  = subFamily

    @property
    def designspaceFile(self):
        return f"{self.familyName.replace(' ', '')}-{self.subFamily.replace(' ', '')}.designspace"

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, self.sourcesFolderName, self.subFamily)


p = MyController(folder, 'My Family', 'Roman')
p.printSettings()
```

This will produce the output below. Notice how the subfamily *Roman* is now part of the designspace name and sources folder.

```plaintext
base folder: MyFolder/
family name: My Family

designspace file: MyFamily-Roman.designspace
designspace path: MyFolder/Sources/Roman/MyFamily-Roman.designspace (False)

sources folder name: Sources
sources folder path: MyFolder/Sources/Roman (False)

...
```
