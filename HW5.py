import plot_style  # noqa: F401
import numpy as np
import matplotlib.pyplot as plt
from constants import g0

SEP = "=" * 60
DIV = "-" * 60
W   = 40  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw5_ex3_2(
    p1=2.068,      # chamber pressure (MPa)
    T1=2222.0,     # chamber temperature (K)
    m_dot=1.0,     # propellant mass flow rate (kg/s)
    k=1.30,        # specific heat ratio
    R=345.7,       # specific gas constant (J/kg-K)
    p3=0.1013,     # ambient pressure for optimum expansion (MPa)
):
    """
    HW5 / Ex 3-2 — Ideal rocket nozzle, sea-level optimum expansion.

    Assumes optimum expansion (p2 = p3), so the effective exhaust velocity
    equals the exit velocity (c = v2).

    Equations:
      Eq. 3-16: v2 = sqrt((2k/(k-1)) * R*T1 * (1 - (p3/p1)^((k-1)/k)))
      Eq. 2-5 : Is = c / g0
      Eq. 2-16: F  = m_dot * c
    """
    v2 = np.sqrt((2*k / (k - 1)) * R * T1 * (1 - (p3 / p1)**((k - 1) / k)))  # Eq. 3-16
    c  = v2           # ideal: c = v2 for optimum expansion
    Is = c / g0       # Eq. 2-5: specific impulse
    F  = m_dot * c    # Eq. 2-16: thrust

    print(f"\n{SEP}")
    print("  HW5 / Ex 3-2: Ideal Rocket — Sea Level Optimum Expansion")
    print(SEP)
    print("  Inputs:")
    _row("Chamber pressure (p1)",                   f"{p1:>10.4f}", "MPa")
    _row("Chamber temperature (T1)",                f"{T1:>10.1f}", "K")
    _row("Mass flow rate (m_dot)",                  f"{m_dot:>10.3f}", "kg/s")
    _row("Specific heat ratio (k)",                 f"{k:>10.2f}")
    _row("Gas constant (R)",                        f"{R:>10.2f}", "J/kg-K")
    _row("Ambient / exit pressure (p3 = p2)",       f"{p3:>10.4f}", "MPa")
    print(DIV)
    print("  Results:")
    _row("Exit velocity (v2)              [Eq. 3-16]", f"{v2:>10.2f}", "m/s")
    _row("Effective exhaust velocity (c)            ",  f"{c:>10.2f}", "m/s")
    _row("Ideal specific impulse (Is)     [Eq. 2-5]",  f"{Is:>10.1f}", "s")
    _row("Ideal thrust (F)                [Eq. 2-16]", f"{F:>10.1f}", "N")
    print(f"{SEP}\n")

    return v2, Is, F


def hw5_fig3_3(
    p1=2.068,      # chamber pressure (MPa)
    T1=2222.0,     # chamber temperature (K)
    m_dot=1.0,     # propellant mass flow rate (kg/s)
    k=1.30,        # specific heat ratio
    R=345.7,       # specific gas constant (J/kg-K)
    p3=0.1013,     # ambient pressure (MPa)
    n_pts=200,     # number of pressure points along the nozzle
):
    """
    HW5 — Recreate Fig. 3-3 from Sutton & Biblarz.

    Plots cross-sectional area A, temperature T, momentum density v/V,
    Mach number M, specific volume V, and velocity v vs. pressure along
    the nozzle.  Pressure decreases left to right (chamber → exit).

    Isentropic relations (Eqs. 3-7):
      T  = T1 * (p/p1)^((k-1)/k)
      V  = V1 * (p1/p)^(1/k)          [V1 = R*T1 / (p1*1e6)]
      v  = sqrt((2k/(k-1))*R*T1*(1-(p/p1)^((k-1)/k)))    [Eq. 3-16]
      A  = m_dot * V / v               (continuity, Eq. 3-3)
      M  = v / sqrt(k*R*T)
    """
    Py = np.linspace(p1, p3, n_pts)   # pressure along nozzle [MPa]

    V1  = R * T1 / (p1 * 1e6)                                                    # chamber specific volume [m^3/kg]
    Vy  = V1 * (p1 / Py)**(1.0 / k)                                              # specific volume [m^3/kg], Eq. 3-7
    Ty  = T1 * (Py / p1)**((k - 1) / k)                                          # temperature [K], Eq. 3-7
    vy  = np.sqrt((2*k / (k - 1)) * R * T1 * (1 - (Py / p1)**((k - 1) / k)))    # velocity [m/s], Eq. 3-16
    My  = vy / np.sqrt(k * R * Ty)                                               # Mach number
    vV  = vy / Vy                                                                 # momentum density [kg/s·m^2]

    # vy = 0 at chamber (Py[0] = p1); use errstate to suppress divide-by-zero
    with np.errstate(divide='ignore', invalid='ignore'):
        Ay = m_dot * (Vy / vy) * 1e4   # area [cm^2], Eq. 3-3

    v2 = vy[-1]   # exit velocity (= v2 at p3)

    # --- Plotting ---
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    (ax1, ax2), (ax3, ax4), (ax5, ax6) = axes

    ax1.plot(Py, Ay);  ax1.set_ylabel(r'Area [cm$^2$]');              ax1.set_ylim(0, 25)
    ax2.plot(Py, Ty);  ax2.set_ylabel('Temperature [K]');             ax2.set_ylim(1100, T1)
    ax3.plot(Py, vV);  ax3.set_ylabel(r'$v/V$ [kg/s·m$^2$]')
    ax4.plot(Py, My);  ax4.set_ylabel('Mach #');                      ax4.set_ylim(0, 3)
    ax5.plot(Py, Vy);  ax5.set_ylabel(r'Specific Volume [m$^3$/kg]')
    ax6.plot(Py, vy);  ax6.set_ylabel('Velocity [m/s]');              ax6.set_ylim(0, v2)

    ax5.set_xlabel('Pressure [MPa]')
    ax6.set_xlabel('Pressure [MPa]')

    # Reverse x-axis on all subplots so pressure runs chamber → exit (left → right)
    for ax in axes.flat:
        ax.set_xlim(p1, 0)
        ax.grid(True)

    fig.suptitle('Figure 3-3 (from Ex 3-2)')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    hw5_ex3_2()
    hw5_fig3_3()