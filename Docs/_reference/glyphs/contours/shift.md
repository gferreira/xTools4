---
title     : shift
layout    : page
permalink : /reference/dialogs/glyphs/contours/shift

---

Select and shift all points with coordinates smaller / bigger than a given treshold value.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/shift.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
position
: the selection threshold value

axis
: the selection axis: vertical or horizontal

side
: select points above or below the threshold value

shift
: the direction of the position shift

apply
: select and shift points in the selected glyphs

preview
: show a preview of the result in the background
</div>

</div>


preview
-------

![]({{"images/glyphs/shift_preview.png" | relative_url }}){: .img-fluid}


{% comment %}
> - add option to use slant angle (for italic fonts)
{% endcomment %}

