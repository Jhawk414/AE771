import plot_style  # noqa: F401
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def hw6_fig3_4(
    k_values=(1.1, 1.25, 1.4, 1.7),  # specific heat ratios to plot
    #k_values=[1.4],    # <-- uncomment to plot single k value
    n_pts=500,                          # number of pressure-ratio points
):
    """
    HW6 — Recreate Fig. 3-4 from Sutton & Biblarz.

    Plots area ratio Ay/At (upper family) and velocity ratio vy/vt
    (lower family) vs. pressure ratio P1/Py on a log-log scale for
    several specific heat ratios k.

    Equations:
      Eq. 3-25 (inverted):
        Ay/At = 1 / [((k+1)/2)^(1/(k-1)) * (Py/P1)^(1/k)
                     * sqrt((k+1)/(k-1) * (1 - (Py/P1)^((k-1)/k)))]

      Eq. 3-26:
        vy/vt = sqrt((k+1)/(k-1) * (1 - (Py/P1)^((k-1)/k)))

    Axis bounds (matching textbook):
      x-axis : P1/Py ∈ [10, 5000],  log scale
      y-axis : ∈ [1, 500],           log scale
    """
    P1Py = np.logspace(np.log10(10), np.log10(5000), n_pts)
    PyP1 = 1.0 / P1Py

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    fig, ax = plt.subplots(figsize=(9, 7))

    for i, k in enumerate(k_values):
        color = colors[i % len(colors)]
        base = (k + 1) / (k - 1) * (1 - PyP1 ** ((k - 1) / k))

        # Eq. 3-25 inverted: At/Ay → Ay/At
        AyAt = 1.0 / (
            ((k + 1) / 2) ** (1 / (k - 1))
            * PyP1 ** (1 / k)
            * np.sqrt(base)
        )
        vyvt = np.sqrt(base)   # Eq. 3-26

        ax.plot(P1Py, AyAt, color=color, lw=1.4)
        ax.plot(P1Py, vyvt, color=color, lw=1.4, ls='--')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(10, 5000)
    ax.set_ylim(1, 500)
    ax.set_xlabel('$P_1 / P_y$')

    # Legend: color encodes k, line style encodes quantity
    handles = [
        *[Line2D([0], [0], color=colors[i % len(colors)], lw=1.4,
                 label=f'$k = {k}$')
          for i, k in enumerate(k_values)],
        Line2D([0], [0], color='k', lw=1.4, ls='-',  label='$A_y / A_t$'),
        Line2D([0], [0], color='k', lw=1.4, ls='--', label='$v_y / v_t$'),
    ]
    ax.legend(handles=handles, loc='upper left', fontsize=9)

    ax.set_title(
        'Figure 3-4: Area and velocity ratios as function of pressure ratio\n'
        'for the diverging section of a supersonic nozzle.'
    )
    ax.grid(True, which='both', ls=':', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    hw6_fig3_4()