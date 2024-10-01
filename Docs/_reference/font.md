---
title  : font
layout : default
---

Tools to modify various kinds of font-level data.
{: .lead }

<ul>
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'font' %}
        {% for subsubitem in subitem.submenu %}
          <li><a href='{{ subsubitem.title | slugify }}'>{{ subsubitem.title }}</a></li>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</ul>
