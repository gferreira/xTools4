---
title  : Changelog
layout : page
class  : __changelog
order  : 5
---

<!--

All notable changes to hTools3 are documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).
hTools3 adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

semantic versioning: MAJOR.MINOR.PATCH
see http://keepachangelog.com/

| MAJOR | incompatible API changes                           |
| MINOR | new functionality in a backwards compatible manner |
| PATCH | backwards compatible bug fixes                     |

additional labels for pre-release and build 
as extensions to the MAJOR.MINOR.PATCH format

types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

-->

0.6.5
-----

Released on 02 February 2022.

- <span class='badge'>Changed</span> Adding option to create new glyphs in *[font > set glyph order](../font/set-glyph-order/)*.
- <span class='badge'>Changed</span> Adding support for slant angle in *[glyphs > metrics > center glyph](../glyphs/metrics/center/)*.
- <span class='badge'>Changed</span> Various updates to variable font and webfont builders (API).
- <span class='badge'>Added</span> Added missing developer documentation for several modules.
- <span class='badge'>Fixed</span> Created new private access token (valid until 31/12/2024) after the previous one expired.

0.6.4
-----

Released on 24 August 2021.

- <span class='badge'>Changed</span> Moved outline transformation scripts to new menu subfolder *glyphs > contours*.
- <span class='badge'>Changed</span> The *[layers](../glyphs/modifiers/layers)* modifier dialog now allows empty selection, which returns the current layer.
- <span class='badge'>Changed</span> Made the width of the *[preferences](../preferences)* dialog standard, renamed window title to *settings*.
- <span class='badge'>Added</span> Adding new tool *[glyphs > anchors > copy](../glyphs/anchors/copy)* to transfer anchors between fonts and/or layers.
- <span class='badge'>Added</span> Adding new tool *[glyphs > contours > outline](../glyphs/contours/outline)* to expand contours by a given offset.
- <span class='badge'>Added</span> Adding new tool *[glyphs > layers > lock](../glyphs/layers/lock-widths)* to lock/unlock the width of all layers in a glyph.
- <span class='badge'>Fixed</span> Fixed `hProject` bug when setting neutral font info in generated variable sources.

0.6.3
-----

Released on 16 May 2021.

- <span class='badge'>Changed</span> Rebuilt user docs using [Bootstrap] to make it responsive and usable on mobile devices.
- <span class='badge'>Changed</span> Renaming color conversion functions in [`hTools3.modules.color`].
- <span class='badge'>Added</span> Adding new tool *[glyph > display options](../glyph/display-options)* to quickly toggle display options in the Glyph Editor.
- <span class='badge'>Added</span> Adding new page with information about [licensing] to the user docs.
- <span class='badge'>Added</span> Adding new page with [Single User License] document (draft).
- <span class='badge'>Added</span> Adding instructions to install hTools3 from the source code.

[Bootstrap]: http://getbootstrap.com/
[licensing]: ../licensing
[Single User License]: ../licensing/single-user-license
[`hTools3.modules.color`]: http://hipertipo.gitlab.io/hTools3/modules/color.html

0.6.2
-----

Released on 26 January 2021.

- <span class='badge'>Changed</span> Switching from popup list to plain list for target layer selection in *glyphs > metrics > copy*.
- <span class='badge'>Added</span> New script *[glyphs > guidelines > new from selection](../glyphs/guidelines/new-from-selection)*.
- <span class='badge'>Fixed</span> Fixed bug with layer selection in the current glyph.

0.6.1
-----

Released on 12 January 2021.

- <span class='badge'>Changed</span> Adding support for multiple layers and decomposition preview in *glyphs > transform > actions*.
- <span class='badge'>Changed</span> Adding balance handles to *glyphs > transform > actions*.
- <span class='badge'>Changed</span> Updating and improving the [developer docs].
- <span class='badge'>Added</span> Making user docs and API docs available from the *Extensions > hTools3* menu.
- <span class='badge'>Fixed</span> Fixed bug with decomposing glyphs in *glyphs > transform > actions*.

[developer docs]: http://hipertipo.gitlab.io/hTools3/

0.6.0
-----

Released on 31 December 2020.  
**Trial period terminated.** [Get in touch](mailto:gustavo@hipertipo.com) if you would like to acquire a license.

- <span class='badge'>Changed</span> Switching from steppers to text boxes with support for arrow keys for numerical input.
- <span class='badge'>Changed</span> Adding slant angle to *font > adjust vmetrics*, renaming tool to *adjust dimensions*.
- <span class='badge'>Changed</span> Adding new *duplicate and rename* section to *batch > build glyphs*.
- <span class='badge'>Changed</span> Adding editing area and export button to *glyphs > components > build glyph constructions*.
- <span class='badge'>Changed</span> Moving changelog from standalone `.txt` file into the documentation.
- <span class='badge'>Changed</span> Renaming tools and menus in the docs, redoing all screenshots, reviewing content, etc.
- <span class='badge'>Changed</span> Improved mechanism to activate *projections* mode in *glyph > link points*.
- <span class='badge'>Changed</span> Standardizing all tools as floating windows without the title bar.
- <span class='badge'>Added</span> Enabling drag-and-drop of font files into all batch tools.
- <span class='badge'>Added</span> New scripts *font > invert selection* amd *new glyphs from templates*.
- <span class='badge'>Added</span> New tool *font > export layers*.
- <span class='badge'>Added</span> New script *glyphs > glyph names > skip export*.
- <span class='badge'>Added</span> New introductory pages in the documentation: History, Overview, Installation, etc.
- <span class='badge'>Added</span> New glyph output mode as unicode character in *glyphs > glyph names > print list*.
- <span class='badge'>Added</span> Created new icon representing *toolkit for digital punchcuters*.

0.5.4
-----

Released on 29 August 2020.

- <span class='badge'>Added</span> New tool *font > set glyph order*.
- <span class='badge'>Added</span> New tool *glyphs > components > build constructions*.
- <span class='badge'>Added</span> New script *glyphs > components > decompose*.
- <span class='badge'>Changed</span> Centered preview in *glyph > interpolation*.

0.5.3
-----

Released on 04 June 2020.

- <span class='badge'>Changed</span> Trial period extended until 31/12/2020.
- <span class='badge'>Fixed</span> Reverting default selection of template glyphs.

0.5.2
-----

Released on 02 June 2020.

- <span class='badge'>Changed</span> Trial period extended for 2 more months.
- <span class='badge'>Fixed</span> Glyph selection algorithm in Single Window Mode.
- <span class='badge'>Added</span> New module functions to generate variable fonts and webfonts.

0.5.1
-----

Released on 22 April 2020.

- <span class='badge'>Added</span> New tool *glyphs > actions* + documentation.
- <span class='badge'>Added</span> Option to clear layers in *font > clear data*.
- <span class='badge'>Fixed</span> Bug in *glyph > measurements* which caused components to be deleted.
- <span class='badge'>Fixed</span> Bug in *glyphs > copy width* which raised an error.

0.5.0
-----

Released on 03 April 2020.  
Initial public release as a trial extension.

- <span class='badge'>Added</span> New online documentation and GitLab Pages workflow.
