---
title     : xTools4 user documentation
layout    : default
permalink : /
---

<span class='badge bg-secondary rounded-0'>version {{ site.version }}</span>

xTools4 is a collection of expert tools for typeface design and font production in [RoboFont 4].
{: .lead }

[RoboFont 4]: http://robofont.com/

{% comment %}
<div class='row'>

<div class='col-12 col-sm-6 col-xl-3' markdown='1'>
explanations
------------

- [overview](explanations/overview)
- [about xTools4](explanations/about)
- [variable font production tools](explanations/variable-font-production)
- [about this documentation](explanations/about-docs)
</div>

<div class='col-12 col-sm-6 col-xl-3' markdown='1'>
reference
---------

##### tools

- [glyph](reference/tools/glyph)
- [glyphs](reference/tools/glyphs)
- [font](reference/tools/font)
- [batch](reference/tools/batch)
- [variable](reference/tools/variable)
- [preferences](reference/tools/preferences)

##### formats

- [measurements format](reference/measurements-format)
- [measurement scales and thresholds](reference/measurement-scales-thresholds)
</div>

<div class='col-12 col-sm-6 col-xl-3' markdown='1'>
how-tos
-------

- [installing xTools4](how-tos/installing-xtools4)
</div>

<div class='col-12 col-sm-6 col-xl-3' markdown='1'>
tutorials
---------

</div>

</div>

<div id="carouselExample" class="carousel carousel-dark slide" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="{{ site.url }}/images/variable/Measurements_font.png" class="d-block w-100" />
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/variable/Measurements_glyph.png" class="d-block w-100" />
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/variable/VarGlyphAssistant-measurements.png" class="d-block w-100" />
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/variable/BlendsPreview.png" class="d-block w-100" />
    </div>
    <div class="carousel-item">
      <img src="{{ site.url }}/images/variable/GlyphSetProofer.png" class="d-block w-100" />
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

{% endcomment %}

- - -
{: .mb-4 }


development
-----------

- [changelog](changelog)
- [source code](http://github.com/gferreira/xTools4)
- [issues](http://github.com/gferreira/xTools4/issues)

{% comment %}
<script>
var imgs = [
  'xTools4_1.png',
  'xTools4_2.png',
  'xTools4_3.png',
  'xTools4_4.png',
  'xTools4_5.png',
];
var imgPath = "{{ 'images/index/' | relative_url }}" + imgs[Math.floor(Math.random() * imgs.length)];
document.write('<img class="img-fluid" src=' + imgPath + '/>')
</script>
{% endcomment %}
