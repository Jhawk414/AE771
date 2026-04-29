import plot_style  # noqa: F401

from constants import g0_eng

SEP = "=" * 70
DIV = "-" * 70
W   = 50  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw14_prob2(
    T_l      = 100.0,      # deg F            average water temperature
    k_l      = 1.07e-4,    # Btu/(s-ft-deg F) thermal conductivity of water
    T_g      = 4500.0,     # deg F            gas temperature
    mu       = 2.5e-5,     # lbf-s/ft^2       viscosity of water
    cp       = 1.0,        # Btu/(lb-deg F)   specific heat of water
    a_in     = 0.25,       # in               cooling passage width  (1/4 in)
    b_in     = 0.50,       # in               cooling passage height (1/2 in)
    m_dot    = 0.585,      # lb/sec           water flow through passage
    t_w_in   = 0.125,      # in               inner wall thickness   (1/8 in)
    q_given  = 1.3,        # Btu/(in^2-sec)   heat absorbed
    k_wall   = 26.0,       # Btu/(hr-ft^2-deg F/ft) wall thermal conductivity
):
    """
    HW14 / Problem 2 -- Film coefficient and wall temperatures in a
    water-cooled steel thrust chamber during a static test.

    Given the heat flux, coolant properties, passage geometry, and wall
    properties, determine:
      (a) the film coefficient of the coolant
      (b) the wall temperature on the coolant side
      (c) the wall temperature on the gas side

    Equations (Sutton & Biblarz, 9th ed.):
      Eq. 8-17: q = (k_w / t_w) * (T_wg - T_wl)
      Eq. 8-18: q = h_l * (T_wl - T_l)
      Eq. 8-20: Nu = 0.023 * Re^0.8 * Pr^0.4   (Dittus-Boelter)
                h_l = Nu * k_l / D_h

    Hydraulic diameter for rectangular passage:
      D_h = 4*A / P   where A = a*b, P = 2(a+b)

    Unit note: viscosity given in lbf-s/ft^2; converted via g_c to lbm/(ft-s)
    for Reynolds number.
    """
    # -- Unit conversions ------------------------------------------------------
    g_c    = g0_eng                          # 32.174 lbm-ft/(lbf-s^2)
    mu_lbm = mu * g_c                        # lbm/(ft-s)
    t_w    = t_w_in / 12.0                   # ft
    q      = q_given * 144.0                 # Btu/(ft^2-s)  (1 ft^2 = 144 in^2)
    k_w    = k_wall / 3600.0                 # Btu/(s-ft-deg F)

    # -- Passage geometry ------------------------------------------------------
    a_ft  = a_in / 12.0                      # ft
    b_ft  = b_in / 12.0                      # ft
    A_cs  = a_ft * b_ft                      # ft^2   cross-section area
    P_wet = 2.0 * (a_ft + b_ft)             # ft     wetted perimeter
    D_h   = 4.0 * A_cs / P_wet              # ft     hydraulic diameter

    # -- (a) Film coefficient of the coolant [Eq. 8-20] -----------------------
    G   = m_dot / A_cs                       # lbm/(ft^2-s)  mass velocity
    Re  = G * D_h / mu_lbm                   # Reynolds number
    Pr  = cp * mu_lbm / k_l                  # Prandtl number
    Nu  = 0.023 * Re**0.8 * Pr**0.4         # Eq. 8-20
    h_l = Nu * k_l / D_h                    # Btu/(s-ft^2-deg F)

    # -- (b) Wall temperature on the coolant side [Eq. 8-18] ------------------
    T_wl = T_l + q / h_l                    # deg F

    # -- (c) Wall temperature on the gas side [Eq. 8-17] ----------------------
    T_wg = T_wl + q * t_w / k_w             # deg F

    # -- Implied gas-side film coefficient [Eq. 8-16] -------------------------
    h_g = q / (T_g - T_wg)                  # Btu/(s-ft^2-deg F)

    # -- Output ----------------------------------------------------------------
    print(f"\n{SEP}")
    print("  HW14 / Problem 2: Water-Cooled Steel Thrust Chamber (Static Test)")
    print(SEP)

    print("  Inputs:")
    _row("Average water temperature (T_l)",       f"{T_l:>10.1f}",    "deg F")
    _row("Thermal conductivity of water (k_l)",   f"{k_l:>14.2e}",    "Btu/(s-ft-deg F)")
    _row("Gas temperature (T_g)",                 f"{T_g:>10.1f}",    "deg F")
    _row("Viscosity of water (mu)",               f"{mu:>14.2e}",     "lbf-s/ft^2")
    _row("Specific heat of water (cp)",           f"{cp:>10.1f}",     "Btu/(lb-deg F)")
    _row("Cooling passage dimensions",      f"  {a_in:g} x {b_in:g}", "in")
    _row("Water flow through passage (m_dot)",    f"{m_dot:>10.3f}",  "lb/sec")
    _row("Thickness of inner wall (t_w)",         f"{t_w_in:>10.4f}", "in")
    _row("Heat absorbed (q)",                     f"{q_given:>10.1f}", "Btu/(in^2-sec)")
    _row("Thermal conductivity of wall (k_wall)", f"{k_wall:>10.1f}", "Btu/(hr-ft^2-deg F/ft)")

    print(DIV)
    print("  Intermediate:")
    _row("Hydraulic diameter (D_h)",              f"{D_h:>10.6f}",    "ft")
    _row("Passage cross-section area (A)",        f"{A_cs:>14.6e}",   "ft^2")
    _row("Mass velocity (G = m_dot/A)",           f"{G:>10.2f}",      "lbm/(ft^2-s)")
    _row("Viscosity in mass units (mu)",          f"{mu_lbm:>14.6e}", "lbm/(ft-s)")
    _row("Heat flux (q, per ft^2)",               f"{q:>10.2f}",      "Btu/(ft^2-s)")
    _row("Wall conductivity (k_w, per sec)",      f"{k_w:>14.6e}",    "Btu/(s-ft-deg F)")
    _row("Reynolds number (Re)",                  f"{Re:>10.0f}")
    _row("Prandtl number (Pr)",                   f"{Pr:>10.3f}")
    _row("Nusselt number (Nu)         [Eq. 8-20]", f"{Nu:>10.2f}")

    print(DIV)
    print("  Results:")
    _row("(a) Film coeff (h_l)        [Eq. 8-20]", f"{h_l:>10.4f}",  "Btu/(s-ft^2-deg F)")
    _row("(b) Coolant wall temp (T_wl) [Eq. 8-18]", f"{T_wl:>10.1f}", "deg F")
    _row("(c) Gas-side wall temp (T_wg) [Eq. 8-17]", f"{T_wg:>10.1f}", "deg F")
    print(DIV)
    print("  Verification:")
    _row("Implied gas-film coeff (h_g) [Eq. 8-16]", f"{h_g:>10.4f}", "Btu/(s-ft^2-deg F)")
    print(f"{SEP}\n")

    return h_l, T_wl, T_wg


if __name__ == "__main__":
    hw14_prob2()
