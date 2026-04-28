import plot_style  # noqa: F401

SEP = "=" * 70
DIV = "-" * 70
W   = 50  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw13_ex8_1(
    t_w     = 0.000445,  # m           wall thickness
    kappa   = 43.24,     # W/(m*K)     average thermal conductivity of wall
    T_g     = 3033.0,    # K           average gas temperature
    T_l     = 311.1,     # K           average liquid bulk temperature
    hg_base = 147.0,     # W/(m^2*K)   baseline gas-film coefficient
    hl_base = 20590.0,   # W/(m^2*K)   baseline liquid-film coefficient (instructor correction)
):
    """
    HW13 / Ex 8-1 -- Effects of varying film coefficients on heat transfer
    and wall temperatures in a liquid-cooled thrust chamber.

    Task: Vary h_g (at constant h_l), then vary h_l (at constant h_g).
    Three requested outputs per case:
      (1) Heat transfer rate q          [Eq. 8-15]
      (2) Gas-side wall temp T_wg       [Eq. 8-16]
      (3) Liquid-side wall temp T_wl    [Eq. 8-18]

    Equations (Sutton & Biblarz, 9th ed., Eqs. 8-13 to 8-18):
      Eq. 8-13: Q/A = -kappa * dT/dL   (Fourier conduction through wall)
      Eq. 8-14: q = h * (T_g - T_l) = Q/A
      Eq. 8-15: q = (T_g - T_l) / (1/h_g + t_w/kappa + 1/h_l)
      Eq. 8-16: q = h_g * (T_g - T_wg)  =>  T_wg = T_g - q/h_g
      Eq. 8-17: q = (kappa/t_w) * (T_wg - T_wl)
      Eq. 8-18: q = h_l * (T_wl - T_l)  =>  T_wl = T_l + q/h_l
    Note: hl_base = 20,590 W/m^2*K per instructor correction (textbook typo).
    """

    def solve(hg, hl):
        """Return (q, T_wg, T_wl) for the given film coefficients."""
        q    = (T_g - T_l) / (1.0/hg + t_w/kappa + 1.0/hl)  # Eq. 8-15
        T_wg = T_g - q / hg                                    # Eq. 8-16
        T_wl = T_l + q / hl                                    # Eq. 8-18
        return q, T_wg, T_wl

    q_base, T_wg_base, T_wl_base = solve(hg_base, hl_base)

    # ---- Output -------------------------------------------------------------
    print(f"\n{SEP}")
    print("  HW13 / Ex 8-1: Film Coefficient Effects -- Liquid-Cooled Chamber")
    print(SEP)
    print("  Inputs:")
    _row("Wall thickness (t_w)",                      f"{t_w*1000:>10.3f}", "mm")
    _row("Thermal conductivity (k)",               f"{kappa:>10.2f}",   "W/(m*K)")
    _row("Average gas temperature (T_g)",              f"{T_g:>10.1f}",     "K")
    _row("Average liquid bulk temperature (T_l)",      f"{T_l:>10.1f}",     "K")
    _row("Baseline gas-film coefficient (hg_base)",    f"{hg_base:>10.1f}", "W/(m^2*K)")
    _row("Baseline liquid-film coefficient (hl_base)", f"{hl_base:>10.1f}", "W/(m^2*K)")
    print(DIV)

    # ---- Parametric table (mirrors Table 8-4) --------------------------------
    # Column widths: gas%, liq%, q, q/qbase%, T_wg, T_wl
    C = [9, 9, 13, 10, 9, 9]

    def _thdr():
        print(f"  {'Gas Film':>{C[0]}}  {'Liq Film':>{C[1]}}  "
              f"{'q':>{C[2]}}  {'q/q_base':>{C[3]}}  "
              f"{'T_wg':>{C[4]}}  {'T_wl':>{C[5]}}")
        print(f"  {'(%)':>{C[0]}}  {'(%)':>{C[1]}}  "
              f"{'(W/m^2)':>{C[2]}}  {'(%)':>{C[3]}}  "
              f"{'(K)':>{C[4]}}  {'(K)':>{C[5]}}")

    def _trow(pct_g, pct_l, q, T_wg, T_wl):
        print(f"  {pct_g:>{C[0]}g}  {pct_l:>{C[1]}g}  "
              f"{q:>{C[2]}.0f}  {100*q/q_base:>{C[3]}.1f}  "
              f"{T_wg:>{C[4]}.1f}  {T_wl:>{C[5]}.1f}")

    _thdr()
    print(DIV)
    print("  Part 1 -- Vary h_g (h_l held at baseline):")
    for pct_g in [50.0, 100.0, 200.0, 400.0]:
        q, T_wg, T_wl = solve(hg_base * pct_g / 100.0, hl_base)
        _trow(pct_g, 100.0, q, T_wg, T_wl)

    print()
    print("  Part 2 -- Vary h_l (h_g held at baseline):")
    for pct_l in [100.0, 50.0, 25.0, 12.5, 6.25]:
        q, T_wg, T_wl = solve(hg_base, hl_base * pct_l / 100.0)
        _trow(100.0, pct_l, q, T_wg, T_wl)

    # ---- Three requested outputs (baseline: 100 % / 100 %) ------------------
    print(DIV)
    print("  Three Requested Outputs (baseline: h_g = 100%, h_l = 100%):")
    _row("(1) Heat transfer rate (q)            [Eq. 8-15]",
         f"{q_base:>10.0f}", "W/m^2")
    _row("(2) Gas-side wall temperature (T_wg)  [Eq. 8-16]",
         f"{T_wg_base:>10.1f}", "K")
    _row("(3) Liquid-side wall temp (T_wl)      [Eq. 8-18]",
         f"{T_wl_base:>10.1f}", "K")
    print(f"{SEP}\n")

    return q_base, T_wg_base, T_wl_base


if __name__ == "__main__":
    hw13_ex8_1()
