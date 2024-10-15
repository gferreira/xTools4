---
title     : import layer
layout    : page
permalink : /reference/tools/glyphs/layers/import
---

Import glyphs from an external UFO font into a new layer of the current font.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'> 
![]({{"images/glyphs/layersImport.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'> 
get ufo
: select UFO font from which to import glyphs

source layer
: select layer from which to import the glyphs

target layer
: ^
  use the imported font’s name for the new layer,  
  or define a custom layer name

import
: import glyphs from external UFO into the selected glyphs
</div>

</div>


{% comment %}
- add a preview
{% endcomment %}