---
title     : BatchValidator
layout    : default
permalink : /reference/batch-validator/
---

<nav aria-label="breadcrumb">
  <ol class="breadcrumb small">
    <li class="breadcrumb-item"><a href="{{ site.url }}">Index</a></li>
    <li class="breadcrumb-item"><a href="{{ site.url }}/reference">Reference</a></li>
    <li class="breadcrumb-item active" aria-current="page">{{ page.title }}</li>
  </ol>
</nav>

A tool to batch validate glyphs in a set of fonts against glyphs from another font.
{: .lead}

* Table of Contents
{:toc}


Options
-------

<div class='row'>
<div class='col' markdown='1'>
![]({{ site.url }}/images/BatchValidator.png){: .img-fluid}
</div>
<div class='col' markdown='1'>
default font
: Drag one or more default `.ufo` sources into the top list.

target fonts
: Drag one or more `.ufo` sources to be checked into the bottom list.

validate
: ^
  Select target fonts to validate.  
  Click on the button to perform glyph tests in all glyphs of all selected fonts.  
</div>
</div>


Output
------

<div class='row'>
<div class='col' markdown='1'>
![]({{ site.url }}/images/BatchValidator-1.png){: .img-fluid}
</div>
<div class='col' markdown='1'>
A report of the test results is printed to RoboFont’s Output window.  
</div>
</div>
