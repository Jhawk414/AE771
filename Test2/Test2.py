import numpy as np
from constants import g0_eng, R_UNIV_ENG

SEP = "=" * 65
DIV = "-" * 65
W   = 48  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def test2(
    # ---- Problem statement givens ------------------------------------------
    F       = 1_500_000.0,  # lbf        design thrust
    p1      = 1000.0,       # psia       chamber pressure
    p3      = 14.696,       # psia       SL ambient (= p2 for optimum expansion)
    eta_v   = 0.98,         # --         velocity / Isp correction factor
    eta_CF  = 0.97,         # --         thrust coefficient correction factor
    # ---- Table 5-5: LOX/RP-1, r = 2.24, p1 = 1000 psia (frozen) ----------
    T1_K    = 3571.0,       # K          chamber temperature
    k       = 1.24,         # --         specific heat ratio (frozen)
    M_w     = 21.9,         # lbm/lbmol  molecular weight of combustion products
    r       = 2.24,         # --         mixture ratio O/F by mass
    # ---- Propellant physical properties ------------------------------------
    rho_LOX = 71.1,         # lbf/ft^3   LOX density   [Table 7-1]
    rho_RP1 = 50.45,        # lbf/ft^3   RP-1 density  [Tables 5-5/7-1]
    # ---- Part 2 ------------------------------------------------------------
    t_burn  = 2.75,         # minutes    burn time (ignore startup/shutoff)
):
    """Test 2 -- F-1 Engine Redesign (LOX/RP-1, Sea-Level Optimum Expansion)."""
    # ---- Derived constants --------------------------------------------------
    p2     = p3                              # optimum expansion at design alt
    T1     = T1_K * 1.8                      # K -> °R
    R_gas  = R_UNIV_ENG * g0_eng / M_w      # ft^2/(s^2*°R)  specific gas const
    p2_p1  = p2 / p1                         # exit-to-chamber pressure ratio
    t      = t_burn * 60.0                   # min -> s
    pr_exp = (k - 1.0) / k                  # isentropic exponent (k-1)/k

    # ======================================================================
    #  PART 1 -- Engine Performance  (a through i)
    # ======================================================================

    # a) Ideal exhaust velocity -- Eq. 3-16
    v2 = np.sqrt(
        (2.0 * k / (k - 1.0)) * R_gas * T1
        * (1.0 - p2_p1 ** pr_exp)
    )

    # b) Theoretical specific impulse
    Isp_ideal = v2 / g0_eng

    # c) Actual specific impulse
    Isp_actual = eta_v * Isp_ideal

    # g) Area ratio -- Eq. 3-25 (computed before CF; needed if p2 != p3)
    At_A2 = (
        ((k + 1.0) / 2.0) ** (1.0 / (k - 1.0))
        * p2_p1 ** (1.0 / k)
        * np.sqrt((k + 1.0) / (k - 1.0) * (1.0 - p2_p1 ** pr_exp))
    )
    epsilon = 1.0 / At_A2

    # d) Ideal thrust coefficient -- Eq. 3-30
    CF_momentum = np.sqrt(
        (2.0 * k**2 / (k - 1.0))
        * (2.0 / (k + 1.0)) ** ((k + 1.0) / (k - 1.0))
        * (1.0 - p2_p1 ** pr_exp)
    )
    CF_ideal = CF_momentum + epsilon * (p2 - p3) / p1  # pressure term = 0

    # e) Actual thrust coefficient
    CF_actual = eta_CF * CF_ideal

    # f) Actual throat area & radius:  F = CF_act * p1 * At
    At    = F / (CF_actual * p1)             # in^2
    Rt    = np.sqrt(At / np.pi)              # in
    Rt_ft = Rt / 12.0                        # ft

    # h) Actual nozzle exit area
    A2     = epsilon * At                    # in^2
    A2_ft2 = A2 / 144.0                      # ft^2

    # i) Exit Mach number (ideal) -- Eq. 3-13 inverse
    M2 = np.sqrt(
        ((1.0 / p2_p1) ** pr_exp - 1.0) * 2.0 / (k - 1.0)
    )

    # ======================================================================
    #  PART 2 -- Propellant Budget  (j through s)
    # ======================================================================

    # j) Total propellant weight flowrate: Isp = F/w_dot => w_dot = F/Isp
    w_dot = F / Isp_actual                   # lbf/s

    # l) Oxidizer weight flowrate -- Eq. 6-3
    w_dot_ox = r / (r + 1.0) * w_dot        # lbf/s

    # m) Fuel weight flowrate -- Eq. 6-4
    w_dot_f = 1.0 / (r + 1.0) * w_dot       # lbf/s

    # n) Oxidizer volume flowrate
    V_dot_ox = w_dot_ox / rho_LOX            # ft^3/s

    # o) Fuel volume flowrate
    V_dot_f = w_dot_f / rho_RP1              # ft^3/s

    # k) Total propellant volume flowrate
    V_dot = V_dot_ox + V_dot_f               # ft^3/s

    # p, q) Total weights over burn
    W_ox = w_dot_ox * t                      # lbf
    W_f  = w_dot_f  * t                      # lbf

    # r, s) Total volumes over burn
    Vol_ox = V_dot_ox * t                    # ft^3
    Vol_f  = V_dot_f  * t                    # ft^3

    # ======================================================================
    #  OUTPUT
    # ======================================================================
    print(f"\n{SEP}")
    print("  Test 2: F-1 Engine Redesign (LOX/RP-1, Sea-Level Design)")
    print(SEP)

    print("  Inputs  (* = Table 5-5, LOX/RP-1, r = 2.24, p1 = 1000 psia):")
    _row("Design thrust (F)",                          f"{F:>12,.0f}", "lbf")
    _row("Chamber pressure (p1)",                      f"{p1:>12.1f}", "psia")
    _row("Ambient pressure (p3 = p2, optimum)",        f"{p3:>12.3f}", "psia")
    _row("Velocity correction factor (eta_v)",         f"{eta_v:>12.2f}")
    _row("Thrust coeff. correction (eta_CF)",          f"{eta_CF:>12.2f}")
    _row("* Chamber temperature (T1)",                 f"{T1_K:>12.1f}", f"K  ({T1:.1f} °R)")
    _row("* Specific heat ratio (k)",                  f"{k:>12.2f}")
    _row("* Molecular weight (Mw)",                    f"{M_w:>12.2f}", "lbm/lbmol")
    _row("* Mixture ratio O/F (r)",                    f"{r:>12.2f}")
    _row("  => Gas constant (R = Ru*g0/Mw)",           f"{R_gas:>12.2f}", "ft^2/(s^2*°R)")
    _row("LOX density",                                f"{rho_LOX:>12.2f}", "lbf/ft^3")
    _row("RP-1 density",                               f"{rho_RP1:>12.2f}", "lbf/ft^3")
    _row("Burn time",                                  f"{t_burn:>12.2f}", f"min  ({t:.0f} s)")

    print(DIV)
    print("  Part 1 -- Engine Performance:")
    _row("a) Exhaust velocity (v2)        [Eq. 3-16]", f"{v2:>12.1f}", "ft/s")
    _row("b) Theoretical Isp              [v2/g0]",    f"{Isp_ideal:>12.2f}", "s")
    _row("c) Actual Isp                 [eta_v*Isp]",  f"{Isp_actual:>12.2f}", "s")
    _row("d) Ideal thrust coeff. (CF)     [Eq. 3-30]", f"{CF_ideal:>12.4f}")
    _row("e) Actual thrust coeff.        [eta_CF*CF]",  f"{CF_actual:>12.4f}")
    _row("f) Actual throat area (At)",                  f"{At:>12.2f}", "in^2")
    _row("   Actual throat radius (Rt)",                f"{Rt_ft:>12.4f}", f"ft  ({Rt:.3f} in)")
    _row("g) Area ratio (epsilon)         [Eq. 3-25]", f"{epsilon:>12.4f}")
    _row("h) Actual nozzle exit area (A2)",             f"{A2_ft2:>12.2f}", f"ft^2  ({A2:.0f} in^2)")
    _row("i) Exit Mach number (M2)        [Eq. 3-13]", f"{M2:>12.4f}")

    print(DIV)
    print(f"  Part 2 -- Propellant Budget (t = {t_burn} min = {t:.0f} s):")
    _row("j) Total wt. flowrate (w_dot)",               f"{w_dot:>12.2f}", "lbf/s")
    _row("k) Total vol. flowrate (V_dot)",              f"{V_dot:>12.2f}", "ft^3/s")
    _row("l) Oxidizer wt. flowrate        [Eq. 6-3]",  f"{w_dot_ox:>12.2f}", "lbf/s")
    _row("m) Fuel wt. flowrate            [Eq. 6-4]",  f"{w_dot_f:>12.2f}", "lbf/s")
    _row("n) Oxidizer vol. flowrate",                   f"{V_dot_ox:>12.2f}", "ft^3/s")
    _row("o) Fuel vol. flowrate",                       f"{V_dot_f:>12.2f}", "ft^3/s")
    _row("p) Oxidizer weight (W_ox)",                   f"{W_ox:>12,.0f}", "lbf")
    _row("q) Fuel weight (W_f)",                        f"{W_f:>12,.0f}", "lbf")
    _row("r) Oxidizer volume (Vol_ox)",                 f"{Vol_ox:>12,.1f}", "ft^3")
    _row("s) Fuel volume (Vol_f)",                      f"{Vol_f:>12,.1f}", "ft^3")

    print(DIV)
    print("  Verification:")
    _row("   Table 5-5 Isp frozen",                    f"{285.4:>12.1f}", "s")
    _row("   Computed Isp_ideal",                       f"{Isp_ideal:>12.2f}", "s")
    _row("   Total propellant weight",                  f"{W_ox + W_f:>12,.0f}", "lbf")
    _row("   w_dot check (ox + fuel)",                  f"{w_dot_ox + w_dot_f:>12.2f}",
         f"lbf/s  (target {w_dot:.2f})")
    print(f"{SEP}\n")

    return (v2, Isp_ideal, Isp_actual, CF_ideal, CF_actual,
            At, Rt_ft, epsilon, A2_ft2, M2,
            w_dot, V_dot, w_dot_ox, w_dot_f,
            V_dot_ox, V_dot_f, W_ox, W_f, Vol_ox, Vol_f)


if __name__ == "__main__":
    test2()
