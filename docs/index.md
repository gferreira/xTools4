---
title     : xTools4 user documentation
layout    : default
permalink : /
---

<span class='badge bg-secondary rounded-0'>version {{ site.version }}</span>

xTools4 is a collection of expert tools for typeface design and font production in [RoboFont 4].
{: .lead }

[RoboFont 4]: http://robofont.com/

<div class='row'>

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
explanations
------------

- [overview](explanations/overview)
- [about xTools4](explanations/about)
- [about this documentation](explanations/about-docs)
</div>

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
tutorials
---------

...
</div>

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
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

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
how-tos
-------

- [installing xTools4](how-tos/installing-xtools4)
- [assigning short keys to tools](#)
</div>

</div>


development
-----------

- [source code](http://github.com/gferreira/xTools4)
- [issues](http://github.com/gferreira/xTools4/issues)
- [changelog](changelog)

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
