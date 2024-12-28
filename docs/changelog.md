---
title  : Changelog
layout : page
class  : __changelog
order  : 5
---

All notable changes to xTools4 are documented in this file.
{: .lead }

#### Semantic versioning

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html):

> `MAJOR.MINOR.PATCH`
{: .fs-5 }

| `MAJOR` | incompatible API changes                           |
| `MINOR` | new functionality in a backwards compatible manner |
| `PATCH` | backwards compatible bug fixes                     |
{: .table .table-hover }

<!-- Additional labels for pre-release and build as extensions to the `MAJOR.MINOR.PATCH` format. -->

#### Types of changes

- <span class='badge rounded-0'>Added</span> new features
- <span class='badge rounded-0'>Changed</span> changes in existing functionality
- <span class='badge rounded-0'>Deprecated</span> soon-to-be removed features
- <span class='badge rounded-0'>Removed</span> removed features
- <span class='badge rounded-0'>Fixed</span> bug fixes
- <span class='badge rounded-0'>Security</span> fixes for vulnerabilities
{: ._changelog .mb-4 }

- - -
{: .mb-4 }


0.1.4
-----

- <span class='badge rounded-0'>Fixed</span> Fixing bugs in Measurements tool (disappearing measurements, creating new measurements file).
- <span class='badge rounded-0'>Fixed</span> Fixing false positives in glyph validation group (equal components with different width).
- <span class='badge rounded-0'>Fixed</span> Fixing bug in glyph construction builder (deleted non-construction glyphs).
- <span class='badge rounded-0'>Fixed</span> Fixing center glyphs script.
- <span class='badge rounded-0'>Changed</span> Measurements tool loads glyph measurements in the order of font measurements.
{: ._changelog .mb-4 }


0.1.3
-----

- <span class='badge rounded-0'>Fixed</span> Fixing bugs in logic to assign glyphs to validation groups (empty glyphs, equal contours with different width).
- <span class='badge rounded-0'>Fixed</span> Fixing overwrite mode in batch build duplicate glyphs.
- <span class='badge rounded-0'>Fixed</span> Fixing bug with empty glyph selection in Measurements tool.
{: ._changelog .mb-4 }


0.1.2
-----

- <span class='badge rounded-0'>Fixed</span> Fixing bug in the Measurements tool which caused glyph-level measurements to disappear when changing layers.
- <span class='badge rounded-0'>Changed</span> Adding support for avar2 designspaces to TempEdit.
{: ._changelog .mb-4 }


0.1.1
-----

- <span class='badge rounded-0'>Added</span> Adding new module MeasurementsViewer, adding PDF export to the Measurements tool.
{: ._changelog .mb-4 }


0.1.0
-----

Initial internal release.

- Merging [hTools3] and [VariableValues] into a single open-source project.
- All tools work, or almost all. Some have been upgraded to RF4, a few new ones were added.
- The plan is to continue upgrading existing tools, and to continuously improve the toolkit based on user freedback.
- Documentation covering all tools [is available online][docs], including labels to indicate the status of each tool.
- A `.mechanic` file for easy installation and update with [RoboFont Mechanic] is included.

[hTools3]: http://hipertipo.gitlab.io/htools3-extension/
[VariableValues]: http://gferreira.github.io/fb-variable-values/
[docs]: http://gferreira.github.io/xTools4/
[RoboFont Mechanic]: http://robofontmechanic.com/
