'''
Tools and data structures to work with font infos.

'''

FontInfoAttributes = {
    'General' : {
        'Identification' : [
            'familyName',
            'styleName',
            'styleMapFamilyName',
            'styleMapStyleName',
            'versionMajor',
            'versionMinor',
            'year',
        ],
        'Dimensions' : [
            'unitsPerEm',
            'descender',
            'xHeight',
            'capHeight',
            'ascender',
            'italicAngle',
        ],
        'Legal' : [
            'copyright',
            'trademark',
            'openTypeNameLicense',
            'openTypeNameLicenseURL',
        ],
        'Parties' : [
            'openTypeNameDesigner',
            'openTypeNameDesignerURL',
            'openTypeNameManufacturer',
            'openTypeNameManufacturerURL',
        ],
        'Note' : [
            'note'
        ],
    },
    'OpenType' : {
        'gasp Table' : [
            'openTypeGaspRangeRecords',
        ],
        'head Table' : [
            'openTypeHeadCreated',
            'openTypeHeadFlags',
            'openTypeHeadLowestRecPPEM',
        ],
        'name Table' : [
            'openTypeNamePreferredFamilyName',
            'openTypeNamePreferredSubfamilyName',
            'openTypeNameCompatibleFullName',
            'openTypeNameWWSFamilyName',
            'openTypeNameWWSSubfamilyName',
            'openTypeNameVersion',
            'openTypeNameUniqueID',
            'openTypeNameDescription',
            'openTypeNameSampleText',
            'openTypeNameRecords',
        ],
        'hhea Table' : [
            'openTypeHheaAscender',
            'openTypeHheaDescender',
            'openTypeHheaLineGap',
            'openTypeHheaCaretSlopeRise',
            'openTypeHheaCaretSlopeRun',
            'openTypeHheaCaretOffset',
        ],
        'vhea Table' : [
            'openTypeVheaVertTypoAscender',
            'openTypeVheaVertTypoDescender',
            'openTypeVheaVertTypoLineGap',
            'openTypeVheaCaretSlopeRise',
            'openTypeVheaCaretSlopeRun',
            'openTypeVheaCaretOffset',
        ],
        'OS/2 Table' : [
            'openTypeOS2WidthClass',
            'openTypeOS2WeightClass',
            'openTypeOS2Selection',
            'openTypeOS2VendorID',
            'openTypeOS2Type',
            'openTypeOS2UnicodeRanges',
            'openTypeOS2CodePageRanges',
            'openTypeOS2TypoAscender',
            'openTypeOS2TypoDescender',
            'openTypeOS2TypoLineGap',
            'openTypeOS2WinAscent',
            'openTypeOS2WinDescent',
            'openTypeOS2SubscriptXSize',
            'openTypeOS2SubscriptYSize',
            'openTypeOS2SubscriptXOffset',
            'openTypeOS2SubscriptYOffset',
            'openTypeOS2SuperscriptXSize',
            'openTypeOS2SuperscriptYSize',
            'openTypeOS2SuperscriptXOffset',
            'openTypeOS2SuperscriptYOffset',
            'openTypeOS2StrikeoutPosition',
            'openTypeOS2StrikeoutSize',
        ],
        'Panose' : [
            'openTypeOS2FamilyClass',
            'openTypeOS2Panose',
        ],
    },
    'PostScript' : {
        'Identification' : [
            'postscriptFontName',
            'postscriptFullName',
            'postscriptWeightName',
            'postscriptUniqueID',
        ],
        'Hinting' : [
            'postscriptBlueValues',
            'postscriptOtherBlues',
            'postscriptFamilyBlues',
            'postscriptFamilyOtherBlues',
            'postscriptStemSnapH',
            'postscriptStemSnapV',
            'postscriptBlueFuzz',
            'postscriptBlueShift',
            'postscriptBlueScale',
            'postscriptForceBold',
        ],
        'Dimensions' : [
            'postscriptSlantAngle',
            'postscriptUnderlineThickness',
            'postscriptUnderlinePosition',
            'postscriptIsFixedPitch',
            'postscriptDefaultWidthX',
            'postscriptNominalWidthX',
        ],
        'Characters' : [
            'postscriptDefaultCharacter',
            'postscriptWindowsCharacterSet',
        ],
    },
    'WOFF' : {
        'Identification' : [
            'woffMajorVersion',
            'woffMinorVersion',
            'woffMetadataUniqueID',
        ],
        'Vendor' : [
            'woffMetadataVendor',
        ],
        'Credits' : [
            'woffMetadataCredits',
        ],
        'Description' : [
            'woffMetadataDescription',
        ],
        'Legal' : [
            'woffMetadataCopyright',
            'woffMetadataTrademark',
            'woffMetadataLicense',
            'woffMetadataLicensee',
            'woffMetadataExtensions',
        ],
    },
    'Miscellaneous' : {
        'FOND Data' : [
            'macintoshFONDName',
            'macintoshFONDFamilyID',
        ],
    },
}

FontInfoAttributesIgnorePrefix = {
    'General' : {
        'Legal'          : 'openTypeName',
        'Parties'        : 'openTypeName',
    },
    'OpenType' : {
        'gasp Table'     : 'openType',
        'head Table'     : 'openTypeHead',
        'name Table'     : 'openTypeName',
        'hhea Table'     : 'openTypeHhea',
        'vhea Table'     : 'openTypeVhea',
        'OS/2 Table'     : 'openTypeOS2',
        'Panose'         : 'openTypeOS2',
    },
    'PostScript' : {
        'Identification' : 'postscript',
        'Hinting'        : 'postscript',
        'Dimensions'     : 'postscript',
        'Characters'     : 'postscript',
    },
}
