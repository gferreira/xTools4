# menuTitle : adjust dimensions

from importlib import reload
import xTools4.dialogs.font.adjustVerticalMetrics
reload(xTools4.dialogs.font.adjustVerticalMetrics)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.font.adjustVerticalMetrics import AdjustVerticalMetricsDialog

OpenWindow(AdjustVerticalMetricsDialog)
