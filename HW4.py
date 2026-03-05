import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

mpl.rcParams['font.family'] = 'Charter'

SEP = "=" * 60
DIV = "-" * 60
W   = 40  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw4_ex3_1(
    k=1.3,       # specific heat ratio of combustion products
    M2=2.52,     # nozzle exit Mach number
    p3=0.1013,   # sea-level ambient pressure (MPa)
):
    """
    HW4 / Ex 3-1 — Ideal rocket engine, optimum expansion at sea level.

    For optimum expansion, exit pressure p2 = ambient pressure p3.
    The ideal chamber pressure equals the stagnation pressure (chamber
    velocity ≈ 0), found by rearranging Eq. 3-13.  The nozzle area ratio
    A2/At is then found from Eq. 3-14 with M_throat = 1.

    Equations:
      Eq. 3-13:  p0/p = [1 + (k-1)/2 * M^2]^(k/(k-1))
      Eq. 3-14:  A2/At = (1/M2) * [(1 + (k-1)/2 * M2^2) / ((k+1)/2)]^((k+1)/(2*(k-1)))
    """
    p2 = p3  # optimum expansion condition

    # Chamber (stagnation) pressure — Eq. 3-13 rearranged for p0
    P0 = p2 * (1 + 0.5 * (k - 1) * M2**2) ** (k / (k - 1))

    # Nozzle area ratio — Eq. 3-14 with M_x = M_t = 1
    A2_At = (1.0 / M2) * (
        (1 + 0.5 * (k - 1) * M2**2) / (0.5 * (k + 1))
    ) ** ((k + 1) / (2 * (k - 1)))

    print(f"\n{SEP}")
    print("  HW4 / Ex 3-1: Ideal Rocket Nozzle — Sea Level (Optimum)")
    print(SEP)
    print("  Inputs:")
    _row("Specific heat ratio (k)",                   f"{k:>10.2f}")
    _row("Exit Mach number (M2)",                     f"{M2:>10.2f}")
    _row("Ambient / exit pressure (p3 = p2)",         f"{p3:>10.4f}", "MPa")
    print(DIV)
    print("  Results:")
    _row("Chamber pressure P0           [Eq. 3-13]",  f"{P0:>10.4f}", "MPa")
    _row("Nozzle area ratio A2/At       [Eq. 3-14]",  f"{A2_At:>10.4f}")
    print(f"{SEP}\n")

    return P0, A2_At


def hw4_fig3_1():
    """
    HW4 — Recreate Fig. 3-1 from Sutton & Biblarz.

    Plots p/p0, T/T0 (left axis) and A/At (right axis) vs. Mach number
    for k = 1.20 (dashed) and k = 1.30 (solid).

    Axis bounds (matching textbook):
      x-axis  : Mach ∈ [0.10, 10],  log scale
      left  y : p/p0 & T/T0 ∈ [0.01, 1.0],  log scale
      right y : A/At  ∈ [1.0, 500],           log scale
    """
    Mach = np.linspace(0.10, 10, 2000)

    c = {'P': '#1f4e79', 'T': '#c00000', 'A': '#000000'}
    specs = [(1.20, '--'), (1.30, '-')]

    fig, ax_l = plt.subplots(figsize=(9, 7))
    ax_r = ax_l.twinx()

    for k, ls in specs:
        P_P0 = (1 + 0.5*(k - 1)*Mach**2) ** (-k / (k - 1))
        T_T0 = 1.0 / (1 + 0.5*(k - 1)*Mach**2)
        A_At = (1.0/Mach) * (
            (1 + 0.5*(k - 1)*Mach**2) / (0.5*(k + 1))
        ) ** ((k + 1) / (2*(k - 1)))

        ax_l.plot(Mach, P_P0, ls=ls, color=c['P'], lw=1.4)
        ax_l.plot(Mach, T_T0, ls=ls, color=c['T'], lw=1.4)
        ax_r.plot(Mach, A_At, ls=ls, color=c['A'], lw=1.4)

    # Scales and axis bounds
    ax_l.set_xscale('log')
    ax_l.set_yscale('log')
    ax_r.set_yscale('log')

    ax_l.set_xlim(0.10, 10)
    ax_l.set_ylim(0.01, 1.0)   # left:  p/p0 and T/T0
    ax_r.set_ylim(1.0,  500)   # right: A/At

    # Labels
    ax_l.set_xlabel('Mach Number')
    ax_l.set_ylabel('Pressure ratio $p/p_0$ and temperature ratio $T/T_0$')
    ax_r.set_ylabel('Area ratio, $A/A_t$')
    ax_l.set_title(
        'Figure 3-1: Area Ratio, Pressure Ratio, and Temperature Ratio\n'
        'vs. Mach Number'
    )

    # Legend: line style encodes k, color encodes quantity
    legend_handles = [
        Line2D([0], [0], ls='--', color='k', lw=1.4, label='$k = 1.20$'),
        Line2D([0], [0], ls='-',  color='k', lw=1.4, label='$k = 1.30$'),
        Line2D([0], [0], ls='-',  color=c['P'], lw=1.4, label='$p/p_0$'),
        Line2D([0], [0], ls='-',  color=c['T'], lw=1.4, label='$T/T_0$'),
        Line2D([0], [0], ls='-',  color=c['A'], lw=1.4, label='$A/A_t$'),
    ]
    ax_l.legend(handles=legend_handles, loc='upper left', fontsize=9)

    ax_l.grid(True, which='both', ls=':', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    hw4_ex3_1()
    hw4_fig3_1()
