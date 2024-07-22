# menuTitle : adjust dimensions

from importlib import reload
import hTools4.dialogs.font.adjustVerticalMetrics
reload(hTools4.dialogs.font.adjustVerticalMetrics)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.font.adjustVerticalMetrics import AdjustVerticalMetricsDialog

OpenWindow(AdjustVerticalMetricsDialog)
