from constants import g0

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


if __name__ == "__main__":
    example_2_1()
