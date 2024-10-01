---
title  : print glyphs list
layout : page
---

Print the selected glyphs in multiple modes and formats.
{: .lead }


<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{"images/glyphs/namesPrint.png" | relative_url }}){: .img-fluid}
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

### plain string (glyph names)

```
A B C D a b c d zero one two three
```

### plain string (characters)

```
A B C D a b c d 0 1 2 3
```

### plain list (glyph names)

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

### Python string (glyph names)

```
"A B C D a b c d zero one two three"
```

### Python list (glyph names)

```
["A", "B", "C", "D", "a", "b", "c", "d", "zero", "one", "two", "three"]
```

