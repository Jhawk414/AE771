import plot_style  # noqa: F401
import numpy as np
from constants import STD_ATMOSPHERE_SI

SEP = "=" * 60
DIV = "-" * 60
W   = 40  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw7_ex3_3(
    altitude=25_000,  # m     — operating altitude
    F=5000.0,         # N     — required thrust
    p1=2.039,         # MPa   — chamber pressure
    T1=2800.0,        # K     — chamber temperature
    k=1.20,           # —     — specific heat ratio
    R=360.0,          # J/kg-K — specific gas constant
):
    """
    HW7 / Ex 3-3 — Ideal nozzle design at 25 km altitude (optimum expansion).

    Design an ideal nozzle to deliver 5000 N thrust at 25 km altitude.
    Optimum expansion: p2 = p_ambient, so effective exhaust velocity c = v2.

    Equations:
      Eq. 3-16: v2 = sqrt((2k/(k-1)) * R*T1 * [1 - (p2/p1)^((k-1)/k)])
      Eq. 3-22: Tt = 2*T1 / (k+1)
      Eq. 3-25: At/A2 = ((k+1)/2)^(1/(k-1)) * (p2/p1)^(1/k)
                        * sqrt((k+1)/(k-1) * [1 - (p2/p1)^((k-1)/k)])
      Eq. 3-24: At = (m_dot/p1) * sqrt(R*T1 / (k * (2/(k+1))^((k+1)/(k-1))))
      Eq. 2-16: F = m_dot * c  →  m_dot = F/c
    """
    # Atmospheric exit pressure at altitude (Sutton Appendix 2 / U.S. Std Atm)
    atm        = STD_ATMOSPHERE_SI[altitude]
    p_sl       = STD_ATMOSPHERE_SI[0].P         # sea-level pressure (Pa)
    p2         = atm.P / 1e6                    # exit pressure = ambient (MPa)
    p_ratio_sl = atm.P / p_sl                   # P/P_SL (dimensionless)

    # Controlling pressure ratio
    p2_p1 = p2 / p1

    # Throat temperature — Eq. 3-22
    Tt = 2.0 * T1 / (k + 1)

    # Exit velocity for optimum expansion — Eq. 3-16
    v2 = np.sqrt((2.0 * k / (k - 1)) * R * T1 * (1.0 - p2_p1 ** ((k - 1) / k)))

    # Effective exhaust velocity (ideal, optimum expansion): c = v2  (Eq. 2-15)
    c = v2

    # Mass flow rate — Eq. 2-16 rearranged
    m_dot = F / c

    # Area ratio At/A2 — Eq. 3-25
    At_A2 = (
        ((k + 1) / 2.0) ** (1.0 / (k - 1))
        * p2_p1 ** (1.0 / k)
        * np.sqrt((k + 1) / (k - 1) * (1.0 - p2_p1 ** ((k - 1) / k)))
    )

    # Throat area — Eq. 3-24
    At_m2  = (m_dot / (p1 * 1e6)) * np.sqrt(
        R * T1 / (k * (2.0 / (k + 1)) ** ((k + 1) / (k - 1)))
    )
    At_cm2 = At_m2 * 1e4   # m² → cm²

    # Exit area — from area ratio
    A2_cm2 = At_cm2 / At_A2

    print(f"\n{SEP}")
    print("  HW7 / Ex 3-3: Ideal Nozzle Design at Altitude (Optimum Expansion)")
    print(SEP)
    print("  Inputs:")
    _row("Altitude",                              f"{altitude / 1000:>10.0f}", "km")
    _row("Thrust (F)",                            f"{F:>10.0f}", "N")
    _row("Chamber pressure (p1)",                 f"{p1:>10.4f}", "MPa")
    _row("Chamber temperature (T1)",              f"{T1:>10.0f}", "K")
    _row("Specific heat ratio (k)",               f"{k:>10.2f}")
    _row("Gas constant (R)",                      f"{R:>10.1f}", "J/kg-K")
    print(DIV)
    print("  Intermediate:")
    _row("P/P_SL  (Appendix 2)",                  f"{p_ratio_sl:>10.6f}")
    _row("Exit / ambient pressure (p2)",           f"{p2:>10.6f}", "MPa")
    _row("Pressure ratio (p2/p1)",                 f"{p2_p1:>10.6f}")
    _row("Area ratio (At/A2)          [Eq. 3-25]", f"{At_A2:>10.6f}")
    print(DIV)
    print("  Results:")
    _row("Throat temperature (Tt)     [Eq. 3-22]", f"{Tt:>10.2f}", "K")
    _row("Exit velocity (v2)          [Eq. 3-16]", f"{v2:>10.2f}", "m/s")
    _row("Eff. exhaust velocity (c)             ",  f"{c:>10.2f}", "m/s")
    _row("Mass flow rate (m_dot)      [Eq. 2-16]", f"{m_dot:>10.4f}", "kg/s")
    _row("Throat area (At)            [Eq. 3-24]", f"{At_cm2:>10.4f}", u"cm\u00b2")
    _row("Exit area (A2)                        ",  f"{A2_cm2:>10.2f}",  u"cm\u00b2")
    print(f"{SEP}\n")

    return Tt, v2, At_cm2, A2_cm2


if __name__ == "__main__":
    hw7_ex3_3()
