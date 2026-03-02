import matplotlib as mpl
import matplotlib.pyplot as plt
from constants import g0, STD_ATMOSPHERE_SI

mpl.rcParams['font.family'] = 'Charter'

SEP = "=" * 60
DIV = "-" * 60
W   = 36  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw3(
    P2=59709.0,        # Nozzle exit pressure (Pa), constant with altitude
    F_sl=865624.0,     # Sea-level thrust (N)
    Isp_sl=254.0,      # Sea-level specific impulse (s)
    A2=1.0594,         # Nozzle exit area (m²)
):
    """
    HW3 — Minuteman first-stage rocket: Thrust & Isp vs. Altitude.

    Plots net thrust (N) and specific impulse (s) against altitude (m) on a
    log-scale x-axis using the U.S. Standard Atmosphere from Appendix 2.

    Approach (per homework hints):
      1. C          = Isp_sl * g0                        (effective exhaust velocity)
      2. m_dot      = F_sl / C                           (mass flow rate)
      3. W_dot      = m_dot * g0                         (weight flow rate)
      4. V2         from sea-level thrust eq. (Eq. 2-13) (nozzle exit velocity)
         F_mom      = m_dot * V2                         (momentum thrust, invariant)
      5. F_net(alt) = F_mom + (P2 - P3(alt))*A2
      6. Isp(alt)   = F_net(alt) / W_dot
    """
    # Step 1: Effective exhaust velocity
    C = Isp_sl * g0                    # m/s

    # Step 2: Mass flow rate
    m_dot = F_sl / C                   # kg/s

    # Step 3: Weight flow rate
    W_dot = m_dot * g0                 # N

    # Step 4: Nozzle exit velocity and momentum thrust at sea level (Eq. 2-13)
    P3_sl      = STD_ATMOSPHERE_SI[0].P              # Pa
    V2         = (F_sl - (P2 - P3_sl) * A2) / m_dot  # m/s
    F_momentum = m_dot * V2                           # N  (invariant with altitude)

    # --- Console header ---
    print(f"\n{SEP}")
    print("  HW3: Minuteman First-Stage — Thrust & Isp vs. Altitude")
    print(SEP)
    print("  Inputs:")
    _row("Exit pressure (P2)",               f"{P2:>10,.1f}",   "Pa")
    _row("Sea-level thrust (F_sl)",          f"{F_sl:>10,.1f}", "N")
    _row("Sea-level specific impulse (Isp)", f"{Isp_sl:>10.1f}", "s")
    _row("Nozzle exit area (A2)",            f"{A2:>10.4f}",    "m²")
    print(DIV)
    print("  Derived (altitude-independent):")
    _row("Effective exhaust velocity (C)",   f"{C:>10.2f}",        "m/s")
    _row("Mass flow rate (m_dot)",           f"{m_dot:>10.2f}",    "kg/s")
    _row("Weight flow rate (W_dot)",         f"{W_dot:>10.0f}",    "N")
    _row("Nozzle exit velocity (V2)",        f"{V2:>10.1f}",       "m/s")
    _row("Momentum thrust (F_momentum)",     f"{F_momentum:>10,.0f}", "N")

    # --- Steps 5 & 6: Altitude sweep ---
    print(DIV)
    print("  Altitude Performance (F_net = F_mom + (P2 - P3)*A2):\n")
    C_col = [14, 12, 20, 16, 10]
    header = (f"  {'Altitude (m)':>{C_col[0]}}"
              f"  {'P3 (Pa)':>{C_col[1]}}"
              f"  {'Press. Thrust (N)':>{C_col[2]}}"
              f"  {'Net Thrust (N)':>{C_col[3]}}"
              f"  {'Isp (s)':>{C_col[4]}}")
    print(header)
    print("  " + "-" * (sum(C_col) + 2 * len(C_col)))

    altitudes = []
    thrusts   = []
    isps      = []

    for alt, atm in STD_ATMOSPHERE_SI.items():
        P3      = atm.P
        F_press = (P2 - P3) * A2
        F_net   = F_momentum + F_press
        Isp     = F_net / W_dot
        altitudes.append(alt)
        thrusts.append(F_net)
        isps.append(Isp)
        print(f"  {alt:>{C_col[0]},}"
              f"  {P3:>{C_col[1]}.3E}"
              f"  {F_press:>{C_col[2]},.0f}"
              f"  {F_net:>{C_col[3]},.0f}"
              f"  {Isp:>{C_col[4]}.1f}")

    print(f"\n{SEP}")

    # --- Plot (skip alt=0; can't appear on log scale) ---
    log_alts    = [a for a in altitudes if a > 0]
    log_thrusts = [t for a, t in zip(altitudes, thrusts) if a > 0]
    log_isps    = [i for a, i in zip(altitudes, isps)    if a > 0]

    color_F   = "#1f4e79"
    color_Isp = "#c55a11"

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xscale("log")

    ln1, = ax1.plot(log_alts, log_thrusts, "o-", color=color_F,   label="Thrust")
    ax1.set_xlabel("Altitude [m]")
    ax1.set_ylabel("Net Thrust [N]", color=color_F)
    ax1.tick_params(axis="y", labelcolor=color_F)

    ax2 = ax1.twinx()
    ln2, = ax2.plot(log_alts, log_isps, "o-", color=color_Isp, label="$I_{sp}$")
    ax2.set_ylabel("Specific Impulse [s]", color=color_Isp)
    ax2.tick_params(axis="y", labelcolor=color_Isp)

    ax1.set_title("Net Thrust & $I_{sp}$ vs. Altitude\nMinuteman First-Stage Rocket Motor")
    ax1.legend(handles=[ln1, ln2], loc="center right")
    ax1.grid(True, which="both", ls="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    hw3()
