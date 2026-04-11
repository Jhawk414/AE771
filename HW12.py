import plot_style  # noqa: F401
import numpy as np

SEP = "=" * 60
DIV = "-" * 60
W   = 42  # label column width

# English-unit physical constants
_g0         = 32.174   # ft/s²                standard gravity
_gc         = 32.174   # lbm·ft/(lbf·s²)      Newton's-law proportionality const
_R_UNIV_ENG = 1545.0   # ft·lbf/(lbmol·°R)   universal gas constant


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw12_ex6_1(
    F      = 10_000.0,  # lbf           thrust
    p1     = 1000.0,    # psia          chamber pressure
    r      = 3.40,      # —             mixture ratio  (w_dot_o / w_dot_f)
    M      = 8.90,      # lbm/lbmol     exhaust mean molecular mass
    T1_F   = 4380.0,    # °F            chamber temperature
    k      = 1.26,      # —             specific heat ratio
    p2     = 1.58,      # psia          nozzle exit pressure (optimum: p2 = p3)
    t_op   = 2.5,       # min           required operation time
    eta_Is = 0.97,      # —             Is_actual / Is_ideal
    eta_CF = 0.98,      # —             CF_actual / CF_ideal
    rho_o  = 71.1,      # lbf/ft³       LOX weight density  (Table 7-1 / Fig 7-1)
    rho_f  = 4.4,       # lbf/ft³       LH2 weight density  (Table 7-1 / Fig 7-1)
):
    """
    HW12 / Ex 6-1 — LOX/LH2 liquid rocket engine performance.

    Optimum expansion at altitude where p3 = p2 = 1.58 psia.
    Computes nozzle areas, sea-level weight/volume flow rates, and
    total propellant requirements for 2.5 min of operation.

    Equations:
      Eq. 3-16: v2 = sqrt(2k/(k-1) * R*T1 * [1 - (p2/p1)^((k-1)/k)])
      Eq. 3-25: At/A2 = ((k+1)/2)^(1/(k-1)) * (p2/p1)^(1/k)
                        * sqrt((k+1)/(k-1) * [1 - (p2/p1)^((k-1)/k)])
      Eq. 3-30: CF_ideal = sqrt(2k^2/(k-1) * (2/(k+1))^((k+1)/(k-1))
                                * [1 - (p2/p1)^((k-1)/k)])
                          [pressure correction = 0 since p2 = p3]
      Eq. 6-2:  w_dot = w_dot_o + w_dot_f
      Eq. 6-3:  w_dot_o = r * w_dot / (r + 1)
      Eq. 6-4:  w_dot_f = w_dot / (r + 1)
    """
    # ---- Unit conversions ------------------------------------------------
    T1_R  = T1_F + 459.67             # °F  -> °R
    t_s   = t_op * 60.0               # min -> s
    p2_p1 = p2 / p1                   # pressure ratio (dimensionless)

    # Specific gas constant for exhaust products  [ft²/(s²·°R)]
    R_gas = _R_UNIV_ENG * _gc / M

    # Shared factor reused in Eq. 3-16, 3-25, and 3-30
    bracket = 1.0 - p2_p1 ** ((k - 1.0) / k)

    # ---- Exit velocity  (Eq. 3-16) ---------------------------------------
    # Optimum expansion: p2 = p3, so effective exhaust velocity c = v2
    v2 = np.sqrt((2.0 * k / (k - 1.0)) * R_gas * T1_R * bracket)  # ft/s

    # ---- Ideal specific impulse  (c = v2 at optimum expansion) ----------
    Is_ideal = v2 / _g0               # s

    # ---- Ideal thrust coefficient  (Eq. 3-30, pressure term = 0) --------
    CF_ideal = np.sqrt(
        (2.0 * k**2 / (k - 1.0))
        * (2.0 / (k + 1.0)) ** ((k + 1.0) / (k - 1.0))
        * bracket
    )

    # ---- Area ratio  (Eq. 3-25) ------------------------------------------
    At_A2 = (
        ((k + 1.0) / 2.0) ** (1.0 / (k - 1.0))
        * p2_p1 ** (1.0 / k)
        * np.sqrt((k + 1.0) / (k - 1.0) * bracket)
    )
    eps = 1.0 / At_A2                 # A2/At

    # ---- Actual (real) performance ----------------------------------------
    Is_real = eta_Is * Is_ideal
    CF_real = eta_CF * CF_ideal

    # ---- Nozzle areas  (F = CF * p1[psia] * At[in²] -> At in in²) --------
    At_in2 = F / (CF_real * p1)       # in²
    A2_in2 = eps * At_in2             # in²

    # ---- Propellant weight flow rates  (Eq. 6-2 / 6-3 / 6-4) -----------
    w_dot   = F / Is_real                   # lbf/s  total   [Eq. 6-2 rearranged]
    w_dot_o = r     * w_dot / (r + 1.0)    # lbf/s  oxidizer [Eq. 6-3]
    w_dot_f =         w_dot / (r + 1.0)    # lbf/s  fuel     [Eq. 6-4]

    # ---- Volumetric flow rates  (sea level) ------------------------------
    Q_o = w_dot_o / rho_o                  # ft³/s
    Q_f = w_dot_f / rho_f                  # ft³/s

    # ---- Total propellant for t_op minutes --------------------------------
    W_o     = w_dot_o * t_s                # lbf
    W_f     = w_dot_f * t_s               # lbf
    W_total = w_dot   * t_s               # lbf

    # ---- Output ----------------------------------------------------------
    print(f"\n{SEP}")
    print("  HW12 / Ex 6-1: LOX/LH2 Liquid Rocket Engine Performance")
    print(SEP)
    print("  Inputs:")
    _row("Thrust (F)",                                f"{F:>10.0f}", "lbf")
    _row("Chamber pressure (p1)",                     f"{p1:>10.0f}", "psia")
    _row("Mixture ratio (r)",                         f"{r:>10.2f}")
    _row("Exhaust mean mol. mass (M)",                f"{M:>10.2f}", "lbm/lbmol")
    _row("Chamber temperature (T1)",                  f"{T1_F:>10.0f}", "degF")
    _row("Specific heat ratio (k)",                   f"{k:>10.2f}")
    _row("Exit/ambient pressure (p2 = p3)",           f"{p2:>10.2f}", "psia")
    _row("Operation time",                            f"{t_op:>10.1f}", "min")
    _row("Is correction factor (eta_Is)",             f"{eta_Is:>10.2f}")
    _row("CF correction factor (eta_CF)",             f"{eta_CF:>10.2f}")
    _row("LOX weight density (Table 7-1)",            f"{rho_o:>10.1f}", "lbf/ft^3")
    _row("LH2 weight density (Table 7-1)",            f"{rho_f:>10.1f}", "lbf/ft^3")
    print(DIV)
    print("  Intermediate:")
    _row("Chamber temp (T1)",                         f"{T1_R:>10.2f}", "degR")
    _row("Pressure ratio (p2/p1)",                    f"{p2_p1:>10.6f}")
    _row("Area ratio (eps = A2/At)     [Eq. 3-25]",  f"{eps:>10.3f}")
    print(DIV)
    print("  Performance:")
    _row("Exit velocity (v2)           [Eq. 3-16]",  f"{v2:>10.0f}", "ft/s")
    _row("CF (ideal)                   [Eq. 3-30]",  f"{CF_ideal:>10.4f}")
    _row("CF (actual = 0.98 * ideal)",                f"{CF_real:>10.4f}")
    _row("Is (ideal)",                                f"{Is_ideal:>10.1f}", "s")
    _row("Is (actual = 0.97 * ideal)",                f"{Is_real:>10.1f}", "s")
    print(DIV)
    print("  Nozzle Areas:")
    _row("Throat area (At)",                          f"{At_in2:>10.3f}", "in^2")
    _row("Exit area (A2)",                            f"{A2_in2:>10.1f}", "in^2")
    print(DIV)
    print("  Propellant Flow Rates (sea level):")
    _row("Total weight flow (w_dot)",                 f"{w_dot:>10.3f}", "lbf/s")
    _row("Oxidizer flow (w_dot_o)       [Eq. 6-3]",  f"{w_dot_o:>10.3f}", "lbf/s")
    _row("Fuel flow (w_dot_f)           [Eq. 6-4]",  f"{w_dot_f:>10.3f}", "lbf/s")
    _row("LOX vol. flow (Q_o)",                       f"{Q_o:>10.4f}", "ft^3/s")
    _row("LH2 vol. flow (Q_f)",                       f"{Q_f:>10.4f}", "ft^3/s")
    print(DIV)
    print(f"  Total Propellants for {t_op:.1f} min ({t_s:.0f} s):")
    _row("Oxidizer (W_o)",                            f"{W_o:>10.1f}", "lbf")
    _row("Fuel (W_f)",                                f"{W_f:>10.1f}", "lbf")
    _row("Total propellant (W_total)",                f"{W_total:>10.1f}", "lbf")
    print(f"{SEP}\n")

    return (Is_ideal, Is_real, CF_ideal, CF_real,
            At_in2, A2_in2,
            w_dot, w_dot_o, w_dot_f,
            Q_o, Q_f,
            W_o, W_f, W_total)


if __name__ == "__main__":
    hw12_ex6_1()
