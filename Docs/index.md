---
title  : xTools4 user documentation
layout : default
---

<span class='badge bg-secondary rounded-0'>version {{ site.version }}</span>

xTools4 is a collection of expert tools for typeface design and font production in [RoboFont 4].
{: .lead}

[RoboFont 4]: http://robofont.com/

<div class='row'>

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
explanations
------------

- [overview](explanations/overview)
- [history](explanations/history)
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
</div>

<div class='col-12 col-md-6 col-xl-3' markdown='1'>
how-tos
-------

- [installing xTools4](how-tos/installing-xtools4)
- [assigning short keys to tools](#)
</div>

</div>


{% comment %}

<div class="alert alert-light my-4 rounded-0" role="alert" markdown=1>
The structure of this documentation is based on [The Documentation System]:

<table class='table'>
  <tr>
    <td width='30%'></td>
    <th width='35%' class='text-body-secondary'>useful when studying</th>
    <th width='35%' class='text-body-secondary'>useful when working</th>
  </tr>
  <tr>
    <th class='text-body-secondary'>theoretical knowledge</th>
    <td>
      <strong><a href='explanations'>explanations</a></strong><br/>
      <em>understanding-oriented</em>
    </td>
    <td>
      <strong><a href='reference'>reference</a></strong><br/>
      <em>information-oriented</em>
    </td>
  </tr>
  <tr>
    <th class='text-body-secondary'>practical steps</th>
    <td>
      <strong><a href='tutorials'>tutorials</a></strong><br/>
      <em>learning-oriented</em>
    </td>
    <td>
      <strong><a href='how-tos'>how tos</a></strong><br/>
      <em>problem-oriented</em>
    </td>
  </tr>
</table>

</div>

[The Documentation System]: http://docs.divio.com/documentation-system/

{% endcomment %}


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
