# menuTitle : visualize curvature

from importlib import reload
import xTools4.dialogs.glyph.curvatureVisualizer
reload(xTools4.dialogs.glyph.curvatureVisualizer)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyph.curvatureVisualizer import CurvatureVisualizerController

OpenWindow(CurvatureVisualizerController)
