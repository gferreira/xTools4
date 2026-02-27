---
title  : Changelog
layout : page
class  : __changelog
order  : 5
---

All notable changes to xTools4 are documented in this file.
{: .lead }


0.2.9
-----

- <span class='badge rounded-0'>Changed</span> Include open fonts in the list of UFOs in the new overlay tool.
- <span class='badge rounded-0'>Changed</span> Adding support for composite glyphs in BlendsPreview.
- <span class='badge rounded-0'>Changed</span> Rewriting glyph construction builder with validation and composite filtering.
{: ._changelog .mb-4 }


0.2.8
-----

- <span class='badge rounded-0'>Added</span> Adding new tool to overlay UFOs in the background of the current glyph view.
{: ._changelog .mb-4 }


0.2.7
-----

- <span class='badge rounded-0'>Added</span> Adding GlyphMemeProofer to visualize all parametric sources of a glyph as a multi-page PDF.
- <span class='badge rounded-0'>Added</span> Adding mark glyph by type to glyphs > mark colors menu.
- <span class='badge rounded-0'>Changed</span> Adding support for italic angle in VarGlyphViewer deltas and margins.
- <span class='badge rounded-0'>Changed</span> Select designspace file when saving measurements from the Measurements tool.
- <span class='badge rounded-0'>Changed</span> Removing notes about RoboFont version from the documentation.
- <span class='badge rounded-0'>Fixed</span> Fixing font-level measurements in temporary fonts.
{: ._changelog .mb-4 }


0.2.6
-----

- <span class='badge rounded-0'>Added</span> Adding GlyphTuning tool to quickly open all corner tuning sources of a single glyph for editing.
- <span class='badge rounded-0'>Added</span> Adding documentation of custom libs in temporary fonts, and tools that support them.
- <span class='badge rounded-0'>Changed</span> Implemented color codes in VarGlyphViewer to differentiate three types of point delta.
- <span class='badge rounded-0'>Changed</span> Adding window identifiers to all dialogs for compatibility with the [Workspaces](http://github.com/typesupply/workspaces) extension.
- <span class='badge rounded-0'>Removed</span> Removing GlyphGauge tool (superseded by the Measurements tool).
{: ._changelog .mb-4 }


0.2.5
-----

- <span class='badge rounded-0'>Changed</span> Making designspace files the single entry point for variable tools.
{: ._changelog .mb-4 }


0.2.4
-----

- <span class='badge rounded-0'>Added</span> Adding BlendsPreview tool to preview locations in blended axes of a parametric designspace.
{: ._changelog .mb-4 }


0.2.3
-----

- <span class='badge rounded-0'>Fixed</span> Fixing copy width bug in mask tool.
- <span class='badge rounded-0'>Fixed</span> Fixing lost glyph set path when flipping layers in GlyphMeme tool.
{: ._changelog .mb-4 }


0.2.2
-----

- <span class='badge rounded-0'>Added</span> Adding RoundingTool UI to create and preview rounded stroke caps and corners.
{: ._changelog .mb-4 }


0.2.1
-----

- <span class='badge rounded-0'>Added</span> Adding RoundingTools module to assist in the creation of min/max round sources.
{: ._changelog .mb-4 }


0.2.0
-----

- <span class='badge rounded-0'>Added</span> Adding workspace window identifier to some tools (experimental).
- <span class='badge rounded-0'>Changed</span> Improving support for temporary fonts in various tools.
- <span class='badge rounded-0'>Changed</span> Adding Italian and Indonesian to the languages module.
{: ._changelog .mb-4 }


0.1.9
-----

- <span class='badge rounded-0'>Added</span> Adding new tool GlyphMeme to quickly open all parametric sources of a single glyph for editing.
{: ._changelog .mb-4 }


0.1.8
-----

- <span class='badge rounded-0'>Changed</span> Making measurement and validation tools work with temporary fonts.
{: ._changelog .mb-4 }


0.1.7
-----

- <span class='badge rounded-0'>Changed</span> Improving TempEdit temporary font setup.
{: ._changelog .mb-4 }


0.1.6
-----

- <span class='badge rounded-0'>Added</span> Adding italic angle and offset correction to the Measurements tool.
- <span class='badge rounded-0'>Added</span> Adding option to toggle between font units and permill values when visualizing measurements.
- <span class='badge rounded-0'>Changed</span> Rewriting GlyphValidator filters to improve performance.
{: ._changelog .mb-4 }


0.1.5
-----

- <span class='badge rounded-0'>Added</span> Adding validation colors to the font info and kerning tabs in VarFontAssistant.
- <span class='badge rounded-0'>Added</span> Adding validation colors to the attributes tab in VarGlyphAssistant
- <span class='badge rounded-0'>Changed</span> Moving old versions of variable tools to submenu.
- <span class='badge rounded-0'>Deprecated</span> Retiring GlyphGauge, use the Measurements tool instead.
- <span class='badge rounded-0'>Removed</span> Temporarily removing the points tab in VarGlyphAssistant (not working yet).
{: ._changelog .mb-4 }


0.1.4
-----

- <span class='badge rounded-0'>Fixed</span> Fixing bugs in the Measurements tool (disappearing measurements, creating new measurements file).
- <span class='badge rounded-0'>Fixed</span> Fixing false positives in glyph validation group (equal components with different width).
- <span class='badge rounded-0'>Fixed</span> Fixing bug in glyph construction builder (deleted non-construction glyphs).
- <span class='badge rounded-0'>Fixed</span> Fixing script to center glyphs.
- <span class='badge rounded-0'>Changed</span> Measurements tool loads glyph measurements in the order of font measurements.
{: ._changelog .mb-4 }


0.1.3
-----

- <span class='badge rounded-0'>Fixed</span> Fixing bugs in the logic to assign glyphs to validation groups (empty glyphs, equal contours with different width).
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

- - -
{: .mb-4 }


#### Semantic versioning

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning]:

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

[Keep a Changelog]: http://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: http://semver.org/spec/v2.0.0.html

