from xTools4.modules.encoding import char2psname

# diacritics per language
# source: Diacritics Project
# http://diacritics.typo.cz/index.php?id=49

diacriticsChars = {
    'albanian' : [
        'ç ë',
        'Ç Ë',
    ],
    'bosnian' : [
        'č ć đ š ž',
        'Č Ć Đ Š Ž',
    ],
    'catalan' : [
        'à ç è é í ï ŀ ò ó ú ü',
        'À Ç È É Í Ï Ŀ Ò Ó Ú Ü',
    ],
    'croatian' : [
        'č ć đ š ž',
        'Č Ć Đ Š Ž',
    ],
    'czech' : [
        'á č ď é ě í ň ó ř š ť ú ů ý ž',
        'Á Č Ď É Ě Í Ň Ó Ř Š Ť Ú Ů Ý Ž',
    ],
    'danish' : [
        'å æ é ø á í ó ú ý',
        'Å Æ É Ø Á Í Ó Ú Ý',
    ],
    'dutch' : [
        'á é í ó ú à è ë ï ö ü ĳ',
        'Á É Í Ó Ú À È Ë Ï Ö Ü Ĳ',
    ],
    'estonian' : [
        'ä õ ö š ü ž',
        'Ä Õ Ö Š Ü Ž',
    ],
    'faroese' : [
        'á æ ð í ó ø ú ý',
        'Á Æ Ð Í Ó Ø Ú Ý',
    ],
    'finish' : [
        'å ä ö š ž',
        'Å Ä Ö Š Ž',
    ],
    'french' : [
        'à â æ ç è é ê ë î ï ô œ ù û ü ÿ',
        'À Â Æ Ç È É Ê Ë Î Ï Ô Œ Ù Û Ü Ÿ',
    ],
    'german' : [
        'ä ö ü ß',
        'Ä Ö Ü',
    ],
    'hungarian' : [
        'á é í ó ö ő ú ü ű',
        'Á É Í Ó Ö Ő Ú Ü Ű',
    ],
    'icelandic' : [
        'á æ ð é í ó ö þ ú ý',
        'Á Æ Ð É Í Ó Ö Þ Ú Ý',
    ],
    'indonesian' : [
        'é',
        'É',
    ],
    'irish' : [
        'á ḃ ċ ḋ é ḟ ġ ḣ í ṁ ó ṗ ṡ ṫ ú',
        'Á Ḃ Ċ Ḋ É Ḟ Ġ Ḣ Í Ṁ Ó Ṗ Ṡ Ṫ Ú',
    ],
    'italian' : [
        'á à é è ì í î ï ò ó ù ú',
        'È À Ì Ò Ù É Í Á Ó Ú Ï Î',
    ],
    'latvian' : [
        'ā č ē ģ ī ķ ļ ņ š ū ž ō ŗ',
        'Ā Č Ē Ģ Ī Ķ Ļ Ņ Š Ū Ž Ō Ŗ',
    ],
    'lithuanian' : [
        'ą č ę ė į š ų ū ž',
        'Ą Č Ę Ė Į Š Ų Ū Ž',
    ],
    'maltese' : [
        'à ċ è ġ ħ ì î ò ù ż',
        'À Ċ È Ġ Ħ Ì Î Ò Ù Ż',
    ],
    'maori' : [
        'ā ē ī ō ū',
        'Ā Ē Ī Ō Ū',
    ],
    'norwegian' : [
        'æ ø å à é ê ó ò ô',
        'Æ Ø Å À É Ê Ó Ò Ô',
    ],
    'polish' : [
        'ą ć ę ł ń ó ś ż ź',
        'Ą Ć Ę Ł Ń Ó Ś Ż Ź',
    ],
    'portuguese' : [
        'à á â ã ç é ê í ó ô õ ú',
        'À Á Â Ã Ç É Ê Í Ó Ô Õ Ú ',
    ],
    'romanian' : [
        'â ă î ș ț',
        'Â Ă Î Ș Ț',
    ],
    'sanskrit' : [
        'ā ḍ ḥ ī ḷ ṁ ṅ ṇ ñ ṛ ṝ ś ṣ ṭ ū',
        'Ā Ḍ Ḥ Ī Ḷ Ṁ Ṅ Ṇ Ñ Ṛ Ṝ Ś Ṣ Ṭ Ū',
    ],
    'serbian' : [
        'č ć đ š ž',
        'Č Ć Đ Š Ž',
    ],
    'slovak' : [
        'á ä č ď é í ĺ ľ ň ó ô ŕ š ť ú ý ž',
        'Á Ä Č Ď É Í Ĺ Ľ Ň Ó Ô Ŕ Š Ť Ú Ý Ž',
    ],
    'slovenian' : [
        'č š ž',
        'Č Š Ž',
    ],
    'spanish' : [
        'á é í ó ú ü ñ',
        'Á É Í Ó Ú Ü Ñ',
    ],
    'swedish' : [
        'ä å é ö á à ë ü',
        'Ä Å É Ö Á À Ë Ü',
    ],
    'turkish' : [
        'â ç ğ î ı ö ş û ü',
        'Â Ç Ğ Î İ Ö Ş Û Ü',
    ],
    'welsh' : [
        'à â è é ê ë î ï ô ù û ü ÿ ẁ ẃ ẅ ỳ ý ŵ ŷ',
        'À Â È É Ê Ë Î Ï Ô Ù Û Ü Ÿ Ẁ Ẃ Ẅ Ỳ Ý Ŵ Ŷ',
    ],
}

def chars2psnames(chars):
    return [char2psname(char) for char in chars if char is not None]

def chars2glyphnames(charsDict):
    glyphNames = {}
    for lang in charsDict.keys():
        glyphNames[lang] = []
        # get lc/uc character strings
        lc, uc = charsDict[lang]
        # get characters as lists
        lcChars = lc.split()
        ucChars = uc.split()
        # get glyph names from characters
        lcGlyphNames = chars2psnames(lcChars)
        ucGlyphNames = chars2psnames(ucChars)
        # append lists of glyph names to dict
        glyphNames[lang].append(lcGlyphNames)
        glyphNames[lang].append(ucGlyphNames)
    return glyphNames

def checkLanguageCoverage(language, glyphNames):
    lc, uc = diacriticsGlyphnames[language]
    langNames = lc + uc
    # check matching glyphs
    notInFont = []
    for langName in langNames:
        if langName not in glyphNames:
            notInFont.append(langName)
    # done
    return notInFont

def checkLanguagesCoverage(glyphNames, n=50):
    # check language support
    supportedLangs = []
    notSupportedLangs = {}
    for lang in diacriticsGlyphnames.keys():
        missingGlyphs = checkLanguageCoverage(lang, glyphNames)
        if len(missingGlyphs) == 0:
            supportedLangs.append(lang)
        else:
            notSupportedLangs[lang] = missingGlyphs
    notSupportedOrdered = notSupportedLangs.keys()
    # print info
    print('fully supported languages:')
    print('-' * n)
    print('%s\n' % ' '.join(sorted(supportedLangs)))
    print('not fully supported:')
    print('-' * n)
    print('%s\n' % ' '.join(sorted(notSupportedLangs.keys())))
    print('missing glyphs for each language:')
    print('-' * n)
    for lang in sorted(notSupportedLangs.keys()):
        print('%s (%s):' % (lang, len(notSupportedLangs[lang])))
        print('%s\n' % ' '.join(notSupportedLangs[lang]))

diacriticsGlyphnames = chars2glyphnames(diacriticsChars)


if __name__ == '__main__':
    
    
    from fontParts.world import OpenFont
    
    f = OpenFont('/hipertipo/fonts/Publica/_varfont/555A.ufo')
    print(f)
    print(checkLanguagesCoverage(f.keys()))
    
