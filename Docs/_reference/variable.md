---
title  : variable
layout : default
---

Tools to visualize and edit variable font sources.
{: .lead }

<ul>
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'variable' %}
        {% for subsubitem in subitem.submenu %}
          <li><a href='{{ subsubitem.title | slugify }}'>{{ subsubitem.title }}</a></li>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</ul>
