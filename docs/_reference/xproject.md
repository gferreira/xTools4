---
title     : xProject
layout    : default
permalink : /reference/xproject/
---

A Pythonic API for scripting font source data for parametric variable fonts.
{: .lead}

<span class='badge bg-warning rounded-0'>draft</span> 

<table class="table table-hover">
<tr>
<td><code>xProject.verbose</code></td>
<td>Enable/disable console output.</td>
</tr>
<tr>
<td><code>xProject.settingsFile</code></td>
<td>The name of the project settings file.</td>
</tr>
<tr>
<td><code>xProject.settingsPath</code></td>
<td>Returns the full path of the settings file.</td>
</tr>
<tr>
<td><code>xProject.designspaceFile</code></td>
<td>Returns the name of the designspace file.</td>
</tr>
<tr>
<td><code>xProject.designspacePath</code></td>
<td>Returns the full path of the designspace file.</td>
</tr>
<tr>
<td><code>xProject.designspace</code></td>
<td>Returns a fontTools designspace object (after building).</td>
</tr>
<tr>
<td><code>xProject.parametricAxes</code></td>
<td>A list of parametric axes as 4-letter tags.</td>
</tr>
<tr>
<td><code>xProject.parametricAxesHidden</code></td>
<td>A switch to make parametric axes hidden (or not).</td>
</tr>
<tr>
<td><code>xProject.sourcesFolderName</code></td>
<td>The name of the sources folder.</td>
</tr>
<tr>
<td><code>xProject.sourcesFolder</code></td>
<td>Returns the full path of the sources folder.</td>
</tr>
<tr>
<td><code>xProject.sourcesPaths</code></td>
<td>Returns a list with the full paths of all parametric UFO sources.</td>
</tr>
<tr>
<td><code>xProject.sources</code></td>
<td>Returns a dict of tuning locations (keys) and their UFO sources (values).</td>
</tr>
<tr>
<td><code>xProject.defaultName</code></td>
<td>The name of the default source.</td>
</tr>
<tr>
<td><code>xProject.defaultSourcePath</code></td>
<td>Returns the full path of the default source.</td>
</tr>
<tr>
<td><code>xProject.defaultLocation</code></td>
<td>Returns the parametric location of the default source.</td>
</tr>
<tr>
<td><code>xProject.defaultFont</code></td>
<td>Returns an RFont object of the default font (cached).</td>
</tr>
<tr>
<td><code>xProject.measurementsFile</code></td>
<td>The name of the measurements file.</td>
</tr>
<tr>
<td><code>xProject.measurementsPath</code></td>
<td>Returns the full path of the measurements file.</td>
</tr>
<tr>
<td><code>xProject.measurements</code></td>
<td>Returns the imported measurements as a dictionary.</td>
</tr>
<tr>
<td><code>xProject.measurementsDefault</code></td>
<td>Returns a dictionary with measurements of the default source.</td>
</tr>
<tr>
<td><code>xProject.smartSetsFile</code></td>
<td>Returns the name of the smart sets file.</td>
</tr>
<tr>
<td><code>xProject.smartSetsPath</code></td>
<td>Returns the full path of the smart sets file.</td>
</tr>
<tr>
<td><code>xProject.smartSets</code></td>
<td>Returns the imported smart sets as a dictionary.</td>
</tr>
<tr>
<td><code>xProject.glyphConstructionsFile</code></td>
<td>Returns the name of the glyph construction file.</td>
</tr>
<tr>
<td><code>xProject.glyphConstructionsPath</code></td>
<td>Returns the full path of the glyph construction file.</td>
</tr>
<tr>
<td><code>xProject.glyphConstructions</code></td>
<td>Returns the imported glyph constructions as a dictionary.</td>
</tr>
<tr>
<td><code>xProject.blendsFile</code></td>
<td>The name of the blends file.</td>
</tr>
<tr>
<td><code>xProject.blendsPath</code></td>
<td>Returns the full path of the blends file.</td>
</tr>
<tr>
<td><code>xProject.blendedAxes</code></td>
<td>Returns the imported blended axes as a dictionary.</td>
</tr>
<tr>
<td><code>xProject.blendedSources</code></td>
<td>Returns the imported blended sources as a dictionary.</td>
</tr>
<tr>
<td><code>xProject.tuning</code></td>
<td>Enable/disable tuning (optional, disabled by default).</td>
</tr>
<tr>
<td><code>xProject.tuningSourcerFolderName</code></td>
<td>The name of the tuning folder.</td>
</tr>
<tr>
<td><code>xProject.tuningSourcesFolder</code></td>
<td>Returns the full path of the tuning sources subfolder.</td>
</tr>
<tr>
<td><code>xProject.tuningSourcesPaths</code></td>
<td>Returns a list with the full paths of all tuning UFO sources.</td>
</tr>
<tr>
<td><code>xProject.tuningSources</code></td>
<td>Returns a dict of tuning locations (keys) and their UFO sources (values).</td>
</tr>
<tr>
<td><code>xProject.instancesFolderName</code></td>
<td>The name of the instances folder.</td>
</tr>
<tr>
<td><code>xProject.instancesFolder</code></td>
<td>Returns the full path of the UFO instances folder.</td>
</tr>
<tr>
<td><code>xProject.fontsFolderName</code></td>
<td>The name of the fonts folder.</td>
</tr>
<tr>
<td><code>xProject.fontsFolder</code></td>
<td>Returns the full path of the binary fonts folder.</td>
</tr>
<tr>
<td><code>xProject.varFontFile</code></td>
<td>Returns the name of the variable font file.</td>
</tr>
<tr>
<td><code>xProject.varFontPath</code></td>
<td>Returns the full path of the variable font file.</td>
</tr>
<tr>
<td><code>xProject.proofsFolderName</code></td>
<td>The name of the proofs folder.</td>
</tr>
<tr>
<td><code>xProject.proofsFolder</code></td>
<td>Returns the full path of the proofs folder.</td>
</tr>
<tr>
<td><code>xProject.setSourceNamesFromMeasurements</code></td>
<td>Set source names from the actual measurement value in each source.</td>
</tr>
<tr>
<td><code>xProject.createParametricSources</code></td>
<td>Create fresh min/max sources for parametric axes from default.</td>
</tr>
<tr>
<td><code>xProject.createMeasurementsFile</code></td>
<td>Create a fresh measurements file.</td>
</tr>
<tr>
<td><code>xProject.createSmartSetsFile</code></td>
<td>Create a fresh smart sets file.</td>
</tr>
<tr>
<td><code>xProject.createGlyphConstructionFile</code></td>
<td>Create a fresh glyph construction file.</td>
</tr>
<tr>
<td><code>xProject.updateGlyphsFromDefault</code></td>
<td>Update default glyphs in all sources.</td>
</tr>
<tr>
<td><code>xProject.copyGlyphsFromDefault</code></td>
<td>Copy glyphs from the default source to other sources.</td>
</tr>
<tr>
<td><code>xProject.copyGroupsFromDefault</code></td>
<td>Copy groups from the default source to other sources.</td>
</tr>
<tr>
<td><code>xProject.copyUnicodesFromDefault</code></td>
<td>Copy unicodes from the default source to all other sources.</td>
</tr>
<tr>
<td><code>xProject.copyGlyphOrderFromDefault</code></td>
<td>Copy glyph order from the default source to all other sources.</td>
</tr>
<tr>
<td><code>xProject.buildCompositeGlyphs</code></td>
<td>Build composite glyphs from glyph constructions.</td>
</tr>
<tr>
<td><code>xProject.splitSources</code></td>
<td>Split new parametric sources from existing sources.</td>
</tr>
<tr>
<td><code>xProject.addParametricAxes</code></td>
<td>Add parametric axes to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addParametricSources</code></td>
<td>Add parametric sources to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addDefaultSource</code></td>
<td>Add the default source to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addTuningAxes</code></td>
<td>Add tuning axes to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addTuningSources</code></td>
<td>Add tuning sources to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addInstances</code></td>
<td>Add instances to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addBlendedAxes</code></td>
<td>Add blended axes to the designspace.</td>
</tr>
<tr>
<td><code>xProject.addBlendedSources</code></td>
<td>Add blended sources (mappings) to the designspace.</td>
</tr>
<tr>
<td><code>xProject.buildDesignspace</code></td>
<td>Build designspace file from source data.</td>
</tr>
<tr>
<td><code>xProject.buildInstances</code></td>
<td>Build UFO instances for blended sources.</td>
</tr>
<tr>
<td><code>xProject.buildVariableFont</code></td>
<td>Build avar2 variable font from designspace.</td>
</tr>
<tr>
<td><code>xProject.cleanupSources</code></td>
<td>Remove unnecessary data from UFO sources.</td>
</tr>
<tr>
<td><code>xProject.normalizeSources</code></td>
<td>Normalize UFO sources.</td>
</tr>
<tr>
<td><code>xProject.addCustomKeysToLib</code></td>
<td>Save paths to data files in the designspace lib.</td>
</tr>
<tr>
<td><code>xProject.save</code></td>
<td>Save current designspace to file.</td>
</tr>
<tr>
<td><code>xProject.printAxes</code></td>
<td>Print a list of all variation axes in this project.</td>
</tr>
<tr>
<td><code>xProject.printSettings</code></td>
<td>Print an overview of this project's settings.</td>
</tr>
<tr>
<td><code>xProject.validateDesignspace</code></td>
<td>Validate range of designspace locations.</td>
</tr>
<tr>
<td><code>xProject.proofGlyphMemes</code></td>
<td>Build glyph meme PDF proofs.</td>
</tr>
<tr>
<td><code>xProject.proofSourcesGlyphSet</code></td>
<td>Build glyph set PDF proofs.</td>
</tr>
<tr>
<td><code>xProject.proofBlends</code></td>
<td>Build PDF proof of blends.</td>
</tr>
</table>
