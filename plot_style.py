"""
Apply the AE771 matplotlib style.

Import this module before any plotting code:

    import plot_style  # noqa: F401
"""
from pathlib import Path
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

_HERE = Path(__file__).parent

fm.fontManager.addfont(str(_HERE / 'Charter Regular.ttf'))
plt.style.use(_HERE / 'ae771.mplstyle')
