# menuTitle : show curvature

from importlib import reload
import hTools4.dialogs.glyph.curvatureVisualizer
reload(hTools4.dialogs.glyph.curvatureVisualizer)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyph.curvatureVisualizer import CurvatureVisualizerDialog

OpenWindow(CurvatureVisualizerDialog)
