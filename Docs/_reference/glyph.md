---
title  : glyph
layout : default
---

Tools to visualize and edit the current glyph.
{: .lead }

<ul>
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'glyph' %}
        {% for subsubitem in subitem.submenu %}
          <li><a href='{{ subsubitem.title | slugify }}'>{{ subsubitem.title }}</a></li>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</ul>

{% comment %}
<div class="card bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
- extend point selection to segment in *selection only*
</div>
</div>
{% endcomment %}
