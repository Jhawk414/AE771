import plot_style  # noqa: F401
import numpy as np
from scipy.optimize import brentq
from constants import STD_ATMOSPHERE_SI, P_SL

SEP = "=" * 60
DIV = "-" * 60
W   = 40  # label column width

# ISA standard troposphere constants (valid for h < 11,000 m)
_T0      = 288.15    # K        sea-level temperature
_L       = 0.0065    # K/m      temperature lapse rate
_g       = 9.80665   # m/s²     standard gravity
_R_air   = 287.053   # J/(kg·K) dry air gas constant
_ISA_EXP = _g / (_R_air * _L)  # ≈ 5.2558


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def _isa_altitude(P_Pa):
    """
    Altitude [m] for a given pressure [Pa] using the ISA troposphere model.

    P(h) = P_SL * (1 - L*h/T0)^(g/(R_air*L))
    Inverted: h = T0/L * (1 - (P/P_SL)^(R_air*L/g))

    Valid for h < 11,000 m (troposphere).
    """
    return (_T0 / _L) * (1.0 - (P_Pa / P_SL) ** (1.0 / _ISA_EXP))


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


def hw7_ex3_4(
    p1_atm=20.0,        # atm  — chamber pressure
    k=1.30,             # —    — specific heat ratio
    eps=6.0,            # —    — nozzle expansion area ratio  ε = A2/At
    alt_compare=10_000, # m    — altitude for thrust comparison
):
    """
    HW7 / Ex 3-4 — Thrust coefficient variation and optimum expansion altitude.

    Part A: Solve Eq. 3-25 numerically for the exit pressure ratio P2/P1 given ε.
            P2/P1 cannot be isolated algebraically, so brentq is used on the
            supersonic branch (P2/P1 < sonic pressure ratio).

    Part B: Evaluate CF (Eq. 3-30) at sea level and at alt_compare, then compute
            the percentage thrust increase.

    Part C: Find the optimum expansion altitude (where P3 = P2) analytically.
            At optimum, the pressure correction term in Eq. 3-30 vanishes, so
            CF_opt = momentum term only — no graphical lookup required.
            The corresponding altitude is found via the ISA troposphere model
            (more accurate than a polynomial curve fit to sparse table data).

    Equations:
      Eq. 3-25: 1/ε = ((k+1)/2)^(1/(k-1)) * (P2/P1)^(1/k)
                      * sqrt((k+1)/(k-1) * [1 - (P2/P1)^((k-1)/k)])

      Eq. 3-30: CF = sqrt(2k^2/(k-1) * (2/(k+1))^((k+1)/(k-1))
                          * [1 - (P2/P1)^((k-1)/k)])
                    + (P2 - P3)/P1 * ε
    """
    # ------------------------------------------------------------------ Part A
    # Solve Eq. 3-25 for P2/P1 on the supersonic branch using brentq.
    # LHS = 1/ε = At/A2; RHS is a function of P2/P1.
    lhs = 1.0 / eps

    def _rhs(x):
        """RHS of Eq. 3-25 as a function of P2/P1 = x."""
        return (
            ((k + 1) / 2.0) ** (1.0 / (k - 1))
            * x ** (1.0 / k)
            * np.sqrt((k + 1) / (k - 1) * (1.0 - x ** ((k - 1) / k)))
        )

    # Sonic (throat) pressure ratio — upper bound of supersonic solution search
    p_sonic = (2.0 / (k + 1)) ** (k / (k - 1))
    p2_p1   = brentq(lambda x: _rhs(x) - lhs, 1e-9, p_sonic - 1e-9)
    p2_atm  = p2_p1 * p1_atm            # exit pressure [atm]
    p2_Pa   = p2_atm * P_SL             # exit pressure [Pa]
    rhs_val = _rhs(p2_p1)               # should equal lhs (sanity check)

    # ------------------------------------------------------------------ Part B
    # Momentum term of Eq. 3-30 — depends only on k and P2/P1, not on altitude.
    momentum = np.sqrt(
        (2.0 * k**2 / (k - 1))
        * (2.0 / (k + 1)) ** ((k + 1) / (k - 1))
        * (1.0 - p2_p1 ** ((k - 1) / k))
    )

    def _CF(p3_atm):
        """Eq. 3-30: thrust coefficient at ambient pressure p3 [atm]."""
        return momentum + (p2_atm - p3_atm) / p1_atm * eps

    p3_sl  = 1.0                                          # sea-level [atm]
    p3_cmp = STD_ATMOSPHERE_SI[alt_compare].P / P_SL     # comparison altitude [atm]

    CF_sl  = _CF(p3_sl)
    CF_cmp = _CF(p3_cmp)
    thrust_pct = (CF_cmp - CF_sl) / CF_sl * 100.0

    # ------------------------------------------------------------------ Part C
    # At optimum expansion P3 = P2, so pressure correction = 0:
    #   CF_opt = momentum term  (analytic — no graphical reading of Fig. 3-7 needed)
    CF_opt     = momentum
    alt_opt_m  = _isa_altitude(p2_Pa)    # ISA troposphere (accurate to ~10 m)
    alt_opt_km = alt_opt_m / 1000.0

    # ------------------------------------------------------------------ Output
    print(f"\n{SEP}")
    print("  HW7 / Ex 3-4: Thrust Coefficient Variation and Optimum Altitude")
    print(SEP)
    print("  Inputs:")
    _row("Chamber pressure (p1)",               f"{p1_atm:>10.1f}", "atm")
    _row("Specific heat ratio (k)",             f"{k:>10.2f}")
    _row("Nozzle area ratio (eps = A2/At)",    f"{eps:>10.2f}")
    _row("Comparison altitude",                f"{alt_compare / 1000:>10.0f}", "km")

    print(DIV)
    print("  Part A -- Exit Pressure (Eq. 3-25, numerical solve):")
    _row("LHS  =  1/eps  (= At/A2)",            f"{lhs:>10.6f}")
    _row("P2/P1  (brentq, supersonic branch)",  f"{p2_p1:>10.6f}")
    _row("RHS check  f(P2/P1)",                 f"{rhs_val:>10.6f}")
    _row("Exit pressure (P2)",                  f"{p2_atm:>10.4f}", "atm")

    print(DIV)
    print("  Part B -- Thrust Coefficient (Eq. 3-30):")
    hdr = f"    {'Altitude':<16} {'P3 [atm]':>10}  {'P1/P3':>6}  {'CF':>8}"
    sep = f"    {'-'*16} {'-'*10}  {'-'*6}  {'-'*8}"
    print(hdr)
    print(sep)
    print(f"    {'Sea level':<16} {p3_sl:>10.5f}  {p1_atm / p3_sl:>6.2f}  {CF_sl:>8.5f}")
    print(f"    {f'{alt_compare/1000:.0f} km':<16} {p3_cmp:>10.5f}  {p1_atm / p3_cmp:>6.2f}  {CF_cmp:>8.5f}")
    _row(f"Thrust increase (SL -> {alt_compare/1000:.0f} km) [Eq. 3-30]",
         f"{thrust_pct:>10.1f}", "%")

    print(DIV)
    print("  Part C -- Optimum Expansion Altitude:")
    _row("CF at optimum (P2=P3, analytic)  [Eq. 3-30]", f"{CF_opt:>10.4f}")
    _row("Optimum ambient pressure  P3 = P2",            f"{p2_atm:>10.4f}", "atm")
    _row("Optimum altitude  (ISA troposphere model)",     f"{alt_opt_km:>10.2f}", "km")
    print(f"{SEP}\n")

    return CF_sl, CF_cmp, thrust_pct, CF_opt, alt_opt_km


if __name__ == "__main__":
    #hw7_ex3_3()
    hw7_ex3_4()
