---
title  : set glyph order
layout : page
---

Set glyph order in the current font from encoding file.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/font/setGlyphOrder.png" | relative_url }}){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
import…
: select `.enc` file with a list of glyph names

set order
: apply the encoding file’s glyph order to the current font

create glyphs
: ^
  select behaviour for glyphs which are not in the font:
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

see also [batch > set data](../../batch/set-data/)
