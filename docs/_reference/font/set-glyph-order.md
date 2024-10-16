---
title     : set glyph order
layout    : page
permalink : /reference/tools/font/set-glyph-order/
---

Set glyph order in the current font from encoding file.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/font/setGlyphOrder.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
select…
: select `.enc` file with a list of glyph names

set glyph order
: apply the encoding file’s glyph order to the current font

create glyphs
: ^
  select behavior for glyphs which are not in the font:
  - show as template glyphs (not selected)
  - add new empty glyphs (selected)

paint groups
: mark glyphs from each group with a different color
</div>

</div>


data format
-----------

Groups can be defined in the `.enc` encoding file using the custom syntax shown below.

### glyphorder.enc (plain)

```text
space
a
b
c
d
A
B
C
D
zero
one
two
three
```

### glyphorder.enc (with groups)

```text
%% ExampleFamily
% --------------- spaces
space
% --------------- latin_lc_basic
a
b
c
d
% --------------- latin_uc_basic
A
B
C
D
% --------------- numbers_default
zero
one
two
three
%%
```


<div class="card text-dark bg-light mt-3 rounded-0">
<div class="card-header">see also</div>
<div class="card-body" markdown='1'>
[batch > set data](../../batch/set-data/)
{: .card-text }
</div>
</div>
