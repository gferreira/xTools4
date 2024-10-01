---
title  : glyphs
layout : default
---

Tools to apply actions to the current glyph or to selected glyphs.
{: .lead }

<div class="accordion accordion-flush" id="glyphsIndex">
  {% for item in site.data.menu %}
    {% for subitem in item.submenu %}
      {% if subitem.title == 'glyphs' %}
        {% for subsubitem in subitem.submenu %}
          <div class='accordion-item'>
            <h2 class="accordion-header" id="_heading_{{ subsubitem.title | slugify }}">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#_collapse_{{ subsubitem.title | slugify }}" aria-expanded="false" aria-controls="_collapse_{{ subsubitem.title | slugify }}">
                {{ subsubitem.title }}
              </button>
            </h2>
            <div id="_collapse_{{ subsubitem.title | slugify }}" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#glyphsIndex">
              <div class="accordion-body">
              <ul>
                {% for subsubsubitem in subsubitem.submenu %}
                <li>
                  {% capture subsubsubitem_url %}{{ subitem.title }}/{{ subsubitem.title | slugify }}/{{ subsubsubitem.title | slugify }}{% endcapture %}
                  <a href='{{ subsubsubitem_url | relative_url }}'>{{ subsubsubitem.title }}</a>
                </li>
                {% endfor %}
              </ul>
              </div>
            </div>
          </div>
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endfor %}
</div>
