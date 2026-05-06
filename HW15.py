import numpy as np
from scipy.optimize import brentq

from constants import g0

SEP = "=" * 70
DIV = "-" * 70
W   = 50


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


# =========================================================================== #
#  Table 14-2 (Single Stage) -- Payload mass for a single-stage booster
# =========================================================================== #

def hw15_single_stage(
    dV_design = 8000.0,   # m/s   target delta-V
    Isp       = 480.0,    # s     specific impulse
    m_s       = 250.0,    # kg    structural mass
    m_p       = 1500.0,   # kg    propellant mass
):
    """
    HW15 / Table 14-2 (Single Stage) -- Compute payload delivered to orbit.

    Given delta-V, Isp, structural mass, and propellant mass, solve for the
    payload mass that a single-stage booster can deliver.

    Assumptions:
      1. Zero gravity                       5. Constant propellant flow
      2. Vacuum (L = D = 0)                 6. Stationary earth
      3. Thrust = flight direction           7. No booster (u_0 = 0)
      4. Constant thrust (F = const)         8. Vertical 1-D trajectory

    Equations (Lecture / Sutton Ch. 4):
      Tsiolkovsky:  dV = Isp * g0 * ln(m_0 / m_f)
                    dV = c * ln(1 / MR)
                    dV = c * ln(1 / (s + l))

      where  c    = Isp * g0             exhaust velocity
             m_0  = m_pl + m_s + m_p     initial mass
             m_f  = m_pl + m_s           burnout mass
             MR   = m_f / m_0            mass ratio
             s    = m_s / m_0            structural fraction
             l    = m_pl / m_0           payload fraction
             zeta = m_p / m_0            propellant mass fraction
             s + l + zeta = 1

      Analytical solution for m_pl:
        R    = exp(dV / c)  =  1 / MR
        m_pl = m_p / (R - 1) - m_s
    """
    c = Isp * g0                        # m/s   exhaust velocity

    # -- Solve for payload mass (analytical) ----------------------------------
    R    = np.exp(dV_design / c)        # 1/MR
    m_pl = m_p / (R - 1) - m_s         # kg

    # -- Derived quantities ---------------------------------------------------
    m_0  = m_pl + m_s + m_p             # kg    total initial mass
    m_f  = m_pl + m_s                   # kg    burnout mass
    MR   = m_f / m_0                    #       mass ratio
    s    = m_s / m_0                    #       structural fraction
    l    = m_pl / m_0                   #       payload fraction
    zeta = m_p / m_0                    #       propellant mass fraction

    # -- Verification ---------------------------------------------------------
    dV_check = c * np.log(1.0 / MR)    # m/s   should match dV_design

    # -- Output ----------------------------------------------------------------
    print(f"\n{SEP}")
    print("  HW15 / Table 14-2: Single-Stage Booster")
    print(SEP)

    print("  Inputs:")
    _row("Target delta-V (dV_design)",        f"{dV_design:>10.1f}",  "m/s")
    _row("Specific impulse (Isp)",            f"{Isp:>10.1f}",       "s")
    _row("Structural mass (m_s)",             f"{m_s:>10.1f}",       "kg")
    _row("Propellant mass (m_p)",             f"{m_p:>10.1f}",       "kg")

    print(DIV)
    print("  Intermediate:")
    _row("Exhaust velocity (c = Isp*g0)",     f"{c:>10.2f}",         "m/s")
    _row("1/MR = exp(dV/c)",                  f"{R:>10.4f}")
    _row("Total initial mass (m_0)",          f"{m_0:>10.2f}",       "kg")
    _row("Burnout mass (m_f = m_pl + m_s)",   f"{m_f:>10.2f}",       "kg")
    _row("Mass ratio (MR = m_f / m_0)",       f"{MR:>10.6f}")
    _row("Structural fraction (s = m_s/m_0)", f"{s:>10.6f}")
    _row("Payload fraction (l = m_pl/m_0)",   f"{l:>10.6f}")
    _row("Propellant mass frac (zeta)",       f"{zeta:>10.6f}")
    _row("s + l + zeta (check = 1)",          f"{s + l + zeta:>10.6f}")

    print(DIV)
    print("  Results:")
    _row("Payload to orbit (m_pl)  [Tsiolkovsky]", f"{m_pl:>10.2f}", "kg")
    _row("Payload (rounded)",                 f"{m_pl:>10.0f}",      "kg")
    print(DIV)
    print("  Verification:")
    _row("Computed dV               [Tsiolkovsky]", f"{dV_check:>10.2f}", "m/s")
    print(f"{SEP}\n")

    return m_pl


# =========================================================================== #
#  Table 14-2 (Two Stage) -- Payload mass for a two-stage booster
# =========================================================================== #

def hw15_two_stage(
    dV_design = 8000.0,   # m/s   target delta-V
    Isp       = 480.0,    # s     specific impulse (same for both stages)
    m_s1      = 140.0,    # kg    stage 1 structural mass
    m_p1      = 750.0,    # kg    stage 1 propellant mass
    m_s2      = 140.0,    # kg    stage 2 structural mass
    m_p2      = 750.0,    # kg    stage 2 propellant mass
):
    """
    HW15 / Table 14-2 (Two Stage) -- Compute payload delivered to orbit.

    Given delta-V, Isp, and per-stage structural/propellant masses, solve
    for the payload mass a two-stage (tandem) booster can deliver.

    Staging sequence:
      1. Stage 1 fires:      m_01 = m_pl + m_s2 + m_p2 + m_s1 + m_p1
                              m_f1 = m_01 - m_p1
      2. Stage 1 jettisoned:  m_02 = m_f1 - m_s1  (= m_pl + m_s2 + m_p2)
      3. Stage 2 fires:      m_f2 = m_02 - m_p2  (= m_pl + m_s2)

    Equations (Lecture / Sutton Ch. 4):
      dV_1     = c * ln(m_01 / m_f1)  =  c * ln(1 / (s_1 + l_1))
      dV_2     = c * ln(m_02 / m_f2)  =  c * ln(1 / (s_2 + l_2))
      dV_total = dV_1 + dV_2

    Per-stage fractions (each relative to that stage's initial mass):
      s_i    = m_si / m_0i              structural fraction
      l_i    = (payload of stage i) / m_0i   payload fraction
      zeta_i = m_pi / m_0i              propellant mass fraction

    m_pl is found numerically via root-finding (scipy.optimize.brentq).
    """
    c = Isp * g0                        # m/s   exhaust velocity

    def _eval(m_pl):
        """Return per-stage and total delta-V for a given payload mass."""
        m_01 = m_pl + m_s2 + m_p2 + m_s1 + m_p1
        m_f1 = m_01 - m_p1
        m_02 = m_f1 - m_s1             # stage 1 structure jettisoned
        m_f2 = m_02 - m_p2
        dV1  = c * np.log(m_01 / m_f1)
        dV2  = c * np.log(m_02 / m_f2)
        return dV1, dV2, dV1 + dV2

    # -- Solve for payload mass (numerical) -----------------------------------
    residual = lambda m_pl: _eval(m_pl)[2] - dV_design
    m_pl = brentq(residual, 0.01, 50000.0)

    # -- Per-stage masses ------------------------------------------------------
    m_01 = m_pl + m_s2 + m_p2 + m_s1 + m_p1
    m_f1 = m_01 - m_p1
    m_02 = m_f1 - m_s1
    m_f2 = m_02 - m_p2

    dV1, dV2, dV_total = _eval(m_pl)

    # -- Per-stage fractions ---------------------------------------------------
    MR1   = m_f1 / m_01
    s1    = m_s1 / m_01
    l1    = m_02 / m_01                 # stage 1 "payload" = everything above
    zeta1 = m_p1 / m_01

    MR2   = m_f2 / m_02
    s2    = m_s2 / m_02
    l2    = m_pl / m_02                 # stage 2 payload = actual payload
    zeta2 = m_p2 / m_02

    l_overall = m_pl / m_01             # overall payload fraction

    # -- Output ----------------------------------------------------------------
    print(f"\n{SEP}")
    print("  HW15 / Table 14-2: Two-Stage Booster")
    print(SEP)

    print("  Inputs:")
    _row("Target delta-V (dV_design)",          f"{dV_design:>10.1f}", "m/s")
    _row("Specific impulse (Isp, both stages)", f"{Isp:>10.1f}",      "s")
    _row("Stage 1: structural mass (m_s1)",     f"{m_s1:>10.1f}",     "kg")
    _row("Stage 1: propellant mass (m_p1)",     f"{m_p1:>10.1f}",     "kg")
    _row("Stage 2: structural mass (m_s2)",     f"{m_s2:>10.1f}",     "kg")
    _row("Stage 2: propellant mass (m_p2)",     f"{m_p2:>10.1f}",     "kg")

    print(DIV)
    print("  Intermediate:")
    _row("Exhaust velocity (c = Isp*g0)",       f"{c:>10.2f}",        "m/s")

    print(DIV)
    print("  Stage 1:")
    _row("Initial mass (m_01)",                 f"{m_01:>10.2f}",     "kg")
    _row("Burnout mass (m_f1)",                 f"{m_f1:>10.2f}",     "kg")
    _row("Mass ratio (MR1 = m_f1/m_01)",        f"{MR1:>10.6f}")
    _row("Structural fraction (s1)",            f"{s1:>10.6f}")
    _row("Payload fraction (l1)",               f"{l1:>10.6f}")
    _row("Propellant mass frac (zeta1)",        f"{zeta1:>10.6f}")
    _row("s1 + l1 + zeta1 (check = 1)",         f"{s1+l1+zeta1:>10.6f}")
    _row("Delta-V contribution (dV1)",          f"{dV1:>10.2f}",      "m/s")

    print(DIV)
    print("  Stage 2:")
    _row("Initial mass (m_02)",                 f"{m_02:>10.2f}",     "kg")
    _row("Burnout mass (m_f2)",                 f"{m_f2:>10.2f}",     "kg")
    _row("Mass ratio (MR2 = m_f2/m_02)",        f"{MR2:>10.6f}")
    _row("Structural fraction (s2)",            f"{s2:>10.6f}")
    _row("Payload fraction (l2)",               f"{l2:>10.6f}")
    _row("Propellant mass frac (zeta2)",        f"{zeta2:>10.6f}")
    _row("s2 + l2 + zeta2 (check = 1)",         f"{s2+l2+zeta2:>10.6f}")
    _row("Delta-V contribution (dV2)",          f"{dV2:>10.2f}",      "m/s")

    print(DIV)
    print("  Results:")
    _row("Payload to orbit (m_pl)  [Tsiolkovsky]", f"{m_pl:>10.2f}",  "kg")
    _row("Payload (rounded)",                   f"{m_pl:>10.0f}",     "kg")
    _row("Overall payload fraction (l_overall)", f"{l_overall:>10.6f}")
    print(DIV)
    print("  Verification:")
    _row("Total dV (dV1 + dV2)     [Tsiolkovsky]", f"{dV_total:>10.2f}", "m/s")
    print(f"{SEP}\n")

    return m_pl


if __name__ == "__main__":
    hw15_single_stage()
    hw15_two_stage()
