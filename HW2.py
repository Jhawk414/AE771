import math
from constants import g0, STD_ATMOSPHERE_SI

SEP  = "=" * 60
DIV  = "-" * 60
W    = 34  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def example_2_1(
    m0=200.0,        # Initial mass (kg)
    mf=130.0,        # Mass after rocket operation (kg)
    m_payload=110.0, # Payload + nonpropulsive structure (kg)
    t_burn=3.0,      # Rocket operation duration (s)
    Isp=240.0,       # Average specific impulse (s)
    a_limit_g=35.0,  # Acceleration limit for sensitive equipment (g0)
):
    """
    Example 2-1 — Rocket vehicle performance (Sutton & Biblarz).

    Solves for mass ratios, propellant mass fraction, effective exhaust
    velocity, total impulse, and checks max acceleration against a limit.
    """
    # --- Calculations ---
    m_prop      = m0 - mf
    m_ps_0      = m0 - m_payload            # initial propulsion system mass
    MR_vehicle  = mf / m0
    MR_prop     = (mf - m_payload) / m_ps_0
    zeta        = m_prop / m_ps_0           # propellant mass fraction of propulsion system
    c           = Isp * g0                  # effective exhaust velocity (m/s)
    m_dot       = m_prop / t_burn           # average mass flow rate (kg/s)
    F           = m_dot * c                 # thrust (N)
    I_t         = F * t_burn                # total impulse (N·s)
    It_W0_ratio = I_t / (m_ps_0 * g0)      # impulse-to-weight ratio (s)
    a_max       = F / mf                    # max acceleration at burnout (m/s^2)
    a_max_g     = a_max / g0               # max acceleration in g0's
    limit_ok    = a_max_g <= a_limit_g

    # --- Output ---
    print(f"\n{SEP}")
    print(f"  Example 2-1: Rocket Vehicle Performance")
    print(SEP)
    print("  Inputs:")
    _row("Initial mass (m0)",                f"{m0:>8.2f}", "kg")
    _row("Final mass (mf)",                  f"{mf:>8.2f}", "kg")
    _row("Payload + structure (m_payload)",  f"{m_payload:>8.2f}", "kg")
    _row("Burn duration (t_burn)",           f"{t_burn:>8.2f}", "s")
    _row("Specific impulse (Isp)",           f"{Isp:>8.2f}", "s")
    _row("Accel limit",                      f"{a_limit_g:>8.1f}", "g0")
    print(DIV)
    print("  Results:")
    _row("Propellant mass (m_prop)",         f"{m_prop:>8.2f}", "kg")
    _row("Propulsion system mass (m_ps_0)",  f"{m_ps_0:>8.2f}", "kg")
    _row("Mass ratio -- vehicle (MR)",        f"{MR_vehicle:>8.3f}", "")
    _row("Mass ratio -- propulsion (MR)",    f"{MR_prop:>8.3f}", "")
    _row("Propellant mass fraction (zeta)",  f"{zeta:>8.3f}", "")
    _row("Effective exhaust velocity (c)",   f"{c:>8.1f}", "m/s")
    _row("Mass flow rate (m_dot)",           f"{m_dot:>8.3f}", "kg/s")
    _row("Thrust (F)",                       f"{F:>8.1f}", "N")
    _row("Total impulse (I_t)",              f"{I_t:>8.0f}", "N-s")
    _row("Impulse-to-weight ratio (It/W0)", f"{It_W0_ratio:>8.1f}", "s")
    _row("Max acceleration",                f"{a_max:>8.2f}", f"m/s^2  ({a_max_g:.2f} g0)")
    _row(f"{a_limit_g:.0f} g0 limit exceeded?",
                                             f"{'NO' if limit_ok else 'YES':>8}", "")
    print(SEP)


def example_2_2(
    t_burn=40.0,       # Burn duration (s)
    m0=1210.0,         # Initial propulsion system mass (kg)
    mf=215.0,          # Rocket motor mass after test (kg)
    F_sl=62_250.0,     # Measured sea-level thrust (N)
    p1=7.00e6,         # Chamber pressure (Pa)
    p2=70_000.0,       # Nozzle exit pressure (Pa)
    d_t=0.0855,        # Nozzle throat diameter (m)
    d_2=0.2703,        # Nozzle exit diameter (m)
    altitudes=None,    # Altitudes (m) to evaluate; must exist in STD_ATMOSPHERE
):
    """
    Example 2-2 — Solid propellant rocket motor sea-level test (Sutton & Biblarz).

    Solves for m_dot, c*, c, and nozzle exit velocity v2, then evaluates
    pressure thrust, total thrust, and specific impulse at each altitude.
    Thrust equation (Eq. 2-13): F = m_dot*v2 + (p2 - p3)*A2
    Momentum thrust is invariant with altitude; only pressure thrust changes.
    """
    if altitudes is None:
        altitudes = [0, 1_000, 25_000]

    # --- Calculations ---
    m_dot  = (m0 - mf) / t_burn
    A_t    = math.pi / 4 * d_t**2
    A_2    = math.pi / 4 * d_2**2
    c_star = p1 * A_t / m_dot                       # characteristic velocity (all altitudes)
    c      = F_sl / m_dot                            # effective exhaust velocity at sea level

    # Solve Eq. 2-13 at sea level for v2 (invariant)
    p3_sl      = STD_ATMOSPHERE_SI[0].P
    v2         = (F_sl - (p2 - p3_sl) * A_2) / m_dot
    F_momentum = m_dot * v2                          # momentum thrust (constant)

    # --- Scalar output ---
    print(f"\n{SEP}")
    print(f"  Example 2-2: Solid Propellant Rocket Motor -- Sea-Level Test")
    print(SEP)
    print("  Inputs:")
    _row("Burn duration (t_burn)",            f"{t_burn:>8.1f}", "s")
    _row("Initial prop. system mass (m0)",    f"{m0:>8.1f}", "kg")
    _row("Motor mass after test (mf)",        f"{mf:>8.1f}", "kg")
    _row("Sea-level thrust (F_sl)",           f"{F_sl:>8.1f}", "N")
    _row("Chamber pressure (p1)",             f"{p1/1e6:>8.3f}", "MPa")
    _row("Nozzle exit pressure (p2)",         f"{p2/1e3:>8.2f}", "kPa")
    _row("Nozzle throat diameter (d_t)",      f"{d_t*100:>8.2f}", "cm")
    _row("Nozzle exit diameter (d_2)",        f"{d_2*100:>8.2f}", "cm")
    print(DIV)
    print("  Results (altitude-independent):")
    _row("Mass flow rate (m_dot)",            f"{m_dot:>8.3f}", "kg/s")
    _row("Throat area (A_t)",                 f"{A_t:>8.5f}", "m^2")
    _row("Exit area (A_2)",                   f"{A_2:>8.5f}", "m^2")
    _row("Characteristic velocity (c*)",      f"{c_star:>8.2f}", "m/s")
    _row("Effective exhaust velocity (c)",    f"{c:>8.2f}", "m/s")
    _row("Nozzle exit velocity (v2)",         f"{v2:>8.2f}", "m/s")
    _row("Momentum thrust",                   f"{F_momentum:>8.1f}", "N")

    # --- Altitude table ---
    print(DIV)
    print("  Altitude Performance (Eq. 2-13: F = m_dot*v2 + (p2-p3)*A2):\n")
    C = [12, 10, 18, 16, 12, 8]  # column widths
    header = (f"  {'Altitude (m)':>{C[0]}}  {'P3 (kPa)':>{C[1]}}"
              f"  {'Press. Thrust (N)':>{C[2]}}  {'Mom. Thrust (N)':>{C[3]}}"
              f"  {'Total F (N)':>{C[4]}}  {'Is (s)':>{C[5]}}")
    print(header)
    print("  " + "-" * (sum(C) + 2 * len(C)))

    for alt in altitudes:
        p3      = STD_ATMOSPHERE_SI[alt].P
        F_press = (p2 - p3) * A_2
        F_total = F_momentum + F_press
        Is      = F_total / (m_dot * g0)
        print(f"  {alt:>{C[0]},}"
              f"  {p3/1e3:>{C[1]}.2f}"
              f"  {F_press:>{C[2]}.0f}"
              f"  {F_momentum:>{C[3]}.0f}"
              f"  {F_total:>{C[4]}.0f}"
              f"  {Is:>{C[5]}.1f}")

    print(f"\n{SEP}")


if __name__ == "__main__":
    import sys
    _EXAMPLES = {"2-1": example_2_1, "2-2": example_2_2}
    keys = sys.argv[1:] or list(_EXAMPLES)
    for k in keys:
        if k in _EXAMPLES:
            _EXAMPLES[k]()
        else:
            print(f"Unknown example '{k}'.  Choices: {list(_EXAMPLES)}")
