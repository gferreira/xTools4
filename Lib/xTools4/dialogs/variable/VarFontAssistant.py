# from importlib import reload
# import variableValues.dialogs.RF4.DesignSpaceSelector
# reload(variableValues.dialogs.RF4.DesignSpaceSelector)

from mojo.roboFont import OpenWindow, OpenFont
from variableValues.dialogs.RF4.DesignSpaceSelector import DesignSpaceSelector_EZUI


class VarFontAssistant_EZUI(DesignSpaceSelector_EZUI):

    title = 'VarFont Assistant'

    columnLeft     = 160
    columnFontName = 240
    columnValue    = 50

    content = DesignSpaceSelector_EZUI.content
    content += '''
    * Tab: font info     @fontInfoTab
    >= HorizontalStack

    >>= VerticalStack
    >>> attributes
    >>> |-----------|
    >>> |           |    @fontInfoAttributes
    >>> |-----------|

    >>= VerticalStack
    >>> values
    >>> |-----------|--------|---------|
    >>> | file name | value  | permill |  @fontInfoValues
    >>> |-----------|--------|---------|

    >= HorizontalStack
    >> ( load )          @loadFontInfoButton
    >> ( save )          @saveFontInfoButton

    * Tab: kerning       @kerningTab
    >= HorizontalStack

    >>= VerticalStack
    >>> pairs
    >>> |-----|-----|
    >>> | 1st | 2nd |    @kerningPairs
    >>> |-----|-----|

    >>= VerticalStack    @kerningPreviewStack
    >>> preview
    >>> * MerzView       @kerningPreview
    >>> values
    >>> |-----------|--------|---------|
    >>> | file name | value  | permill |  @kerningValues
    >>> |-----------|--------|---------|

    >= HorizontalStack
    >> ( load )          @loadKerningButton
    >> ( save )          @saveKerningButton

    * Tab: measurements  @measurementsTab
    >= VerticalStack

    >> measurement files
    >> |-files------------|
    >> | measurementFiles |  @measurementFiles
    >> |------------------|

    >>= HorizontalStack
    >>>= VerticalStack
    >>>> measurements
    >>>> |-----------|
    >>>> |           |   @measurements
    >>>> |-----------|

    >>>= VerticalStack
    >>>> values
    >>>> |-----------|-------|---------|
    >>>> | file name | value | permill |  @measurementValues
    >>>> |-----------|-------|---------|

    >= HorizontalStack
    >> ( load )          @loadMeasurementsButton
    >> ( export )        @exportMeasurementsButton

    * Tab: validation    @validationTab
    >= HorizontalStack
    
    >>= VerticalStack    @checksStack
    >>> checks
    >>> [ ] width        @widthCheckBox
    >>> [ ] left         @leftCheckBox
    >>> [ ] right        @rightCheckBox
    >>> [X] points       @pointsCheckBox
    >>> [X] components   @componentsCheckBox
    >>> [X] anchors      @anchorsCheckBox
    >>> [X] unicodes     @unicodesCheckBox

    >>= VerticalStack
    >>> result
    >>> *EZOutputEditor  @checkResults

    > ( validate )       @validateButton
    '''

    buttonWidth = DesignSpaceSelector_EZUI.buttonWidth

    descriptionData = DesignSpaceSelector_EZUI.descriptionData.copy()
    descriptionData.update(dict(
        # font info
        fontInfoAttributes=dict(
            alternatingRowColors=True,
            width=columnLeft,
        ),
        fontInfoValues=dict(
            alternatingRowColors=True,
            width='auto',
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                ),
                dict(
                    identifier="value",
                    title="value",
                    width=columnValue,
                ),
                dict(
                    identifier="permill",
                    title="permill",
                    width=columnValue,
                ),
            ]
        ),
        loadFontInfoButton=dict(
            width=buttonWidth,
        ),
        saveFontInfoButton=dict(
            width=buttonWidth,
        ),
        # kerning
        kerningPreviewStack=dict(
            distribution="fill",
        ),
        kerningPairs=dict(
            alternatingRowColors=True,
            width=columnLeft*2,
            columnDescriptions=[
                dict(
                    identifier="first",
                    title="1st",
                ),
                dict(
                    identifier="second",
                    title="2nd",
                ),
            ]
        ),
        kerningPreview=dict(
            width='auto',
            height=200,
        ),
        kerningValues=dict(
            alternatingRowColors=True,
            width='auto',
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                ),
                dict(
                    identifier="value",
                    title="value",
                    width=columnValue,
                ),
                dict(
                    identifier="permill",
                    title="permill",
                    width=columnValue,
                ),
            ]
        ),
        loadKerningButton=dict(
            width=buttonWidth,
        ),
        saveKerningButton=dict(
            width=buttonWidth,
        ),
        # measurements
        measurementFiles=dict(
            alternatingRowColors=True,
            height=100,
            itemType="dict",
            acceptedDropFileTypes=[".measurements"],
            allowsDropBetweenRows=True,
            allowsInternalDropReordering=True,
            allowsMultipleSelection=False,
            columnDescriptions=[
                dict(
                    identifier="path",
                    title="path",
                    cellClassArguments=dict(
                        showFullPath=True
                    )
                ),
            ],
        ),
        measurements=dict(
            alternatingRowColors=True,
            width=columnLeft,
        ),
        measurementValues=dict(
            alternatingRowColors=True,
            width='auto',
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                ),
                dict(
                    identifier="value",
                    title="value",
                    width=columnValue,
                ),
                dict(
                    identifier="permill",
                    title="permill",
                    width=columnValue,
                ),
            ]
        ),
        loadMeasurementsButton=dict(
            width=buttonWidth,
        ),
        exportMeasurementsButton=dict(
            width=buttonWidth,
        ),
        # validation
        widthCheckBox=dict(
            width=columnLeft,
        ),
        validateButton=dict(
            width=buttonWidth,
        ),
    ))


if __name__ == '__main__':

    OpenWindow(VarFontAssistant_EZUI)
