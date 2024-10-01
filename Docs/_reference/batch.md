---
title  : batch
layout : default
---

Tools to apply actions to multiple fonts at once (closed or open).
{: .lead }

<ul>
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'batch' %}
        {% for subsubitem in subitem.submenu %}
          <li><a href='{{ subsubitem.title | slugify }}'>{{ subsubitem.title }}</a></li>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</ul>
