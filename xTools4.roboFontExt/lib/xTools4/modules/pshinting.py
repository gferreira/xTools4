try:
    from mojo.tools import IntersectGlyphWithLine
except:
    pass

def getStemsV(font, glyphs=['l', 'I']):
    ref_y = font.info.xHeight / 2.0
    stems = []
    for glyph_name in glyphs:
        if glyph_name in font:
            g = font[glyph_name]
            if len(g):
                intersections = IntersectGlyphWithLine(g,
                        ((0, ref_y), (g.width, ref_y)),
                        canHaveComponent=False, addSideBearings=False)
                try:
                    # get margins
                    left_edge, right_edge = intersections
                    # calculate stem from margins
                    stem = abs(int(right_edge[0] - left_edge[0]))
                    if stem not in stems:
                        stems.append(stem)
                except ValueError:
                    print(f'could not get vertical stems from {font.info.familyName} {font.info.styleName}')
                    pass
    return stems

def getStemsH(font, glyphs=['H']):
    stems = []
    for glyph_name in glyphs:
        if glyph_name in font:
            g = font[glyph_name]
            ref_x = g.width / 2
            if len(g):
                # get margins
                intersections = IntersectGlyphWithLine(g,
                            ((ref_x, 0), (ref_x, font.info.capHeight)),
                            canHaveComponent=False, addSideBearings=False)
                try:
                    bottom_edge, top_edge = intersections
                    # calculate stem from margins
                    stem = abs(int(top_edge[1] - bottom_edge[1]))
                    stems.append(stem)
                except ValueError:
                    print(f'could not get horizontal stems from {font.info.familyName} {font.info.styleName}')
                    pass
    return stems

# -------------
# ps blue zones
# -------------

def getBlueZones(font, verbose=False):
    _zones = []
    # baseline
    if 'o' in font and font['o'].bounds:
        _zones.append((font['o'].bounds[1], 0))
    # xheight
    if 'o' in font and font['o'].bounds:
        _zones.append((font.info.xHeight, font['o'].bounds[3]))
    # descender
    if 'g' in font and font['g'].bounds:
        _zones.append((font['g'].bounds[1], font.info.descender))
    # ascender
    if 'f' in font and font['f'].bounds:
        _zones.append((font.info.ascender, font['f'].bounds[3]))
    # capheight
    if 'O' in font and font['O'].bounds:
        _zones.append((font.info.capHeight, font['O'].bounds[3]))
    # remove flat zones & compile
    zones = []
    for z in _zones:
        if len(set(z)) == 2:
            zones += list(z)
    # done
    return sorted([int(z) for z in zones])
