---
title  : xTools4 documentation
layout : default
---

<span class='badge bg-secondary'>version {{ site.version }}</span>

xTools4 is a collection of tools for typeface design and font production in [RoboFont 4].
{: .lead}

[RoboFont 4]: http://robofont.com/

<div class='row'>

<div class='col' markdown='1'>
reference
---------

- [glyph](glyph)
- [glyphs](glyphs)
- [font](font)
- [batch](batch)
- [variable](variable)
- [preferences](preferences)
</div>

<div class='col' markdown='1'>
links
-----

- [release notes](changelog)
- [source code](http://github.com/gferreira/xTools4)
- [issues](http://github.com/gferreira/xTools4/issues)
- [documentation](http://gferreira.github.io/xTools4)
 </div>

</div>

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
