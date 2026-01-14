---
title     : print glyphs list
layout    : page
permalink : /reference/tools/glyphs/glyph-names/print-list/
---

Print the selected glyphs in multiple modes and formats.
{: .lead }

<span class="badge text-bg-warning rounded-0">RF3</span> RoboFont 3 code which still works in RoboFont 4. Not updated to the new RoboFont 4 APIs yet.  


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/glyphs/namesPrint.png){: .img-fluid}
</div>

<div class='col-sm-4' markdown='1'>
output mode
: choose between output as glyph names or as characters

format options
: ^
  choose one of the available formatting options  
  see the examples below

print
: print the names of the selected glyphs to the console

sort names
: sort the list of glyph names or characters alphabetically
</div>

</div>


Examples
--------

##### plain string / glyph names

```
A B C D a b c d zero one two three
```

##### plain string / characters

```
A B C D a b c d 0 1 2 3
```

##### plain list / glyph names

```
A
B
C
D
a
b
c
d
zero
one
two
three
```

##### Python string / glyph names

```
"A B C D a b c d zero one two three"
```

##### Python list / glyph names

```
["A", "B", "C", "D", "a", "b", "c", "d", "zero", "one", "two", "three"]
```
