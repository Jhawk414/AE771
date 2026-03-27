import plot_style  # noqa: F401
import numpy as np
from scipy.optimize import brentq

SEP = "=" * 60
DIV = "-" * 60
W   = 44  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def test1_q2(
    p1_p2=200.0,  # —  chamber-to-exit pressure ratio (P1/P2)
    k=1.23,       # —  specific heat ratio
):
    """
    Test 1 / Q2 — Ideal nozzle design from chamber/exit pressure ratio.

    A C-D nozzle designed for ideal (optimum) operation means P2 = P3
    (exit pressure equals ambient), so P1/P2 = P1/P3 = 200.

    Subscript convention used in this problem:
      1 = chamber (stagnation)
      t = throat
      2 = nozzle exit (= ambient for ideal operation)
      T3 = exit static temperature (same station as P2)

    Part a — Nozzle area ratio A2/At (Eq. 3-25):
      At/A2 = ((k+1)/2)^(1/(k-1)) * (P2/P1)^(1/k)
              * sqrt((k+1)/(k-1) * [1 - (P2/P1)^((k-1)/k)])

    Part b — Exit Mach number M2 (Eq. 3-13, algebraic inverse):
      P1/P2 = [1 + (k-1)/2 * M2^2]^(k/(k-1))
      => M2  = sqrt( [(P1/P2)^((k-1)/k) - 1] * 2/(k-1) )

    Part c — Ideal temperature ratio T1/T3 (isentropic, Eq. 3-7):
      T1/T3 = (P1/P2)^((k-1)/k)
            = 1 + (k-1)/2 * M2^2        (consistent with part b)
    """
    p2_p1 = 1.0 / p1_p2  # exit-to-chamber pressure ratio

    # ---- Part a: area ratio (Eq. 3-25) ---------------------------------
    At_A2 = (
        ((k + 1) / 2.0) ** (1.0 / (k - 1))
        * p2_p1 ** (1.0 / k)
        * np.sqrt((k + 1) / (k - 1) * (1.0 - p2_p1 ** ((k - 1) / k)))
    )
    A2_At = 1.0 / At_A2

    # ---- Part b: exit Mach number (Eq. 3-13, inverse) ------------------
    temp_ratio = p1_p2 ** ((k - 1) / k)          # = T1/T3  (used in part c too)
    M2 = np.sqrt((temp_ratio - 1.0) * 2.0 / (k - 1))

    # ---- Part c: temperature ratio T1/T3 (isentropic, Eq. 3-7) --------
    T1_T3 = temp_ratio                            # = (P1/P2)^((k-1)/k)
    T1_T3_check = 1.0 + (k - 1) / 2.0 * M2**2   # must match (sanity check)

    # ---- Output --------------------------------------------------------
    print(f"\n{SEP}")
    print("  Test 1 / Q2: Ideal Nozzle Design from Pressure Ratio")
    print(SEP)
    print("  Inputs:")
    _row("Chamber/exit pressure ratio (P1/P2)",  f"{p1_p2:>10.1f}")
    _row("Specific heat ratio (k)",              f"{k:>10.2f}")
    print(DIV)
    print("  Results:")
    _row("a) Area ratio (A2/At)        [Eq. 3-25]", f"{A2_At:>10.4f}")
    _row("b) Exit Mach number (M2)     [Eq. 3-13]", f"{M2:>10.4f}")
    _row("c) Temperature ratio (T1/T3) [Eq. 3-7] ", f"{T1_T3:>10.4f}")
    print(DIV)
    print("  Verification:")
    _row("   T1/T3 from M2: 1+(k-1)/2*M2^2       ", f"{T1_T3_check:>10.4f}")
    _row("   At/A2 (raw)                          ", f"{At_A2:>10.6f}")
    print(f"{SEP}\n")

    return A2_At, M2, T1_T3


def test1_q3(
    eps=45.0,     # —              nozzle area ratio A2/At
    p1=1300.0,    # psia           chamber pressure
    T1=2100.0,    # °R             chamber temperature
    k=1.27,       # —              specific heat ratio
    R=1716.0,     # ft^2/(s^2·°R) specific gas constant [= ft·lbf/(slug·°R)]
    p3=14.696,    # psia           standard sea-level ambient pressure
):
    """
    Test 1 / Q3 — Ideal C-D nozzle: exit conditions, throat/exit velocities,
    and theoretical maximum velocity (English units).

    Given area ratio A2/At = 45, isentropic flow is assumed throughout.
    R = 1716 ft·lbf/(slug·°R) = 1716 ft^2/(s^2·°R) in the slug system,
    so velocity formulas require no g_c correction factor.

    Part a — Exit Mach number M2 (Eq. 3-14, numerical inversion via brentq):
      A2/At = (1/M) * [(1 + (k-1)/2 * M^2) / ((k+1)/2)]^((k+1)/(2*(k-1)))

    Part b — Exit static temperature T2 (isentropic, Eq. 3-7):
      T2 = T1 / (1 + (k-1)/2 * M2^2)

    Part c — Exit static pressure P2 (isentropic, Eq. 3-13):
      P2 = P1 / (1 + (k-1)/2 * M2^2)^(k/(k-1))

    Part d — Throat velocity vt (Eqs. 3-22, 3-23):
      Tt = 2*T1 / (k+1)          [throat temperature, M_t = 1]
      vt = sqrt(k * R * Tt)      [sonic condition at throat]

    Part e — Exit velocity v2 (Eq. 3-16):
      v2 = sqrt((2k/(k-1)) * R * T1 * [1 - (P2/P1)^((k-1)/k)])

    Part f — Theoretical maximum velocity (Eq. 3-16 as P2 -> 0):
      v_max = sqrt((2k/(k-1)) * R * T1)
      Requires infinite area ratio; cannot be physically achieved.
    """
    # ---- Part a: invert Eq. 3-14 on the supersonic branch --------------
    def _eq3_14(M):
        """A/At as a function of Mach number (Eq. 3-14)."""
        return (1.0 / M) * (
            (1.0 + 0.5 * (k - 1) * M**2) / (0.5 * (k + 1))
        ) ** ((k + 1) / (2.0 * (k - 1)))

    # Supersonic branch: M > 1. Upper bound chosen conservatively large.
    M2 = brentq(lambda M: _eq3_14(M) - eps, 1.0 + 1e-9, 50.0)

    # ---- Part b: exit temperature (Eq. 3-7 / 3-13 isentropic form) -----
    stag_factor = 1.0 + 0.5 * (k - 1) * M2**2   # T1/T2 = P1/P2^((k-1)/k)
    T2 = T1 / stag_factor

    # ---- Part c: exit pressure (Eq. 3-13) -------------------------------
    p2 = p1 / stag_factor ** (k / (k - 1))

    # ---- Part d: throat temperature and velocity (Eqs. 3-22, 3-23) ------
    Tt = 2.0 * T1 / (k + 1)                  # Eq. 3-22
    vt = np.sqrt(k * R * Tt)                  # Eq. 3-23: sonic, M_t = 1

    # ---- Part e: exit velocity (Eq. 3-16) --------------------------------
    p2_p1 = p2 / p1
    v2 = np.sqrt(
        (2.0 * k / (k - 1)) * R * T1 * (1.0 - p2_p1 ** ((k - 1) / k))
    )
    v2_check = M2 * np.sqrt(k * R * T2)       # must equal v2 (sanity check)

    # ---- Part f: theoretical maximum velocity (Eq. 3-16, P2 -> 0) -------
    v_max = np.sqrt((2.0 * k / (k - 1)) * R * T1)

    # ---- Output ----------------------------------------------------------
    print(f"\n{SEP}")
    print("  Test 1 / Q3: Ideal C-D Nozzle - Exit Conditions & Velocities")
    print(SEP)
    print("  Inputs:")
    _row("Area ratio (A2/At)",                          f"{eps:>10.1f}")
    _row("Chamber pressure (P1)",                       f"{p1:>10.1f}", "psia")
    _row("Chamber temperature (T1)",                    f"{T1:>10.1f}", "°R")
    _row("Specific heat ratio (k)",                     f"{k:>10.2f}")
    _row("Gas constant (R)",                            f"{R:>10.1f}", "ft^2/(s^2·°R)")
    _row("Sea-level ambient pressure (P3)",             f"{p3:>10.3f}", "psia")
    print(DIV)
    print("  Results:")
    _row("a) Exit Mach number (M2)         [Eq. 3-14]", f"{M2:>10.4f}")
    _row("b) Exit temperature (T2)         [Eq. 3-7] ", f"{T2:>10.2f}", "°R")
    _row("c) Exit pressure (P2)            [Eq. 3-13]", f"{p2:>10.4f}", "psia")
    _row("d) Throat temperature (Tt)       [Eq. 3-22]", f"{Tt:>10.2f}", "°R")
    _row("   Throat velocity (vt)          [Eq. 3-23]", f"{vt:>10.2f}", "ft/s")
    _row("e) Exit velocity (v2)            [Eq. 3-16]", f"{v2:>10.2f}", "ft/s")
    _row("f) Max theoretical velocity      [Eq. 3-16]", f"{v_max:>10.2f}", "ft/s")
    _row("   (P2 -> 0, A2/At -> inf; unreachable)    ", "")
    print(DIV)
    print("  Verification:")
    _row("   A/At check from M2: eq. 3-14            ", f"{_eq3_14(M2):>10.4f}", f"(target {eps:.1f})")
    _row("   v2 from M2*sqrt(k*R*T2)                 ", f"{v2_check:>10.2f}", "ft/s")
    _row("   P2/P3 (over/under expansion)            ", f"{p2/p3:>10.4f}", "(< 1 = over-expanded)")
    print(f"{SEP}\n")

    return M2, T2, p2, Tt, vt, v2, v_max


def test1_q1(
    F=25_000.0,     # N          required thrust
    p1_psia=1000.0, # psia       chamber pressure (converted to Pa internally)
    T1=3526.0,      # K          chamber temperature      [Table 5.5: LOX/CH4, O/F=3.20]
    k=1.20,         # --         specific heat ratio      [Table 5.5: LOX/CH4, O/F=3.20]
    M_w=20.3,       # g/mol      mol. wt of combustion products [Table 5.5: LOX/CH4]
    R_univ=8314.3,  # J/kg-mol-K universal gas constant
    p3=101_325.0,   # Pa         sea-level ambient; = p2 for optimum expansion
    g0=9.80665,     # m/s^2      standard gravity
):
    """
    Test 1 / Q1 — LOX/Methane ideal rocket nozzle design (25,000-N thrust).

    Operating condition: P1 = 1000 psia, sea-level optimum expansion (P2 = P3).
    Propellant data from Table 5.5 (O/F = 3.20 by mass, LOX/CH4).

    Intermediate quantities (specific volume approach from study guide / Ex 3-3):
      V1  = R*T1 / P1                        [ideal gas, chamber]
      pt  = P1 * (2/(k+1))^(k/(k-1))        [critical / throat pressure]
      Tt  = 2*T1 / (k+1)                     [Eq. 3-22: throat temperature]
      vt  = sqrt(k*R*Tt)                     [Eq. 3-23: throat velocity, M=1]
      T2  = T1 * (P2/P1)^((k-1)/k)          [Eq. 3-7:  isentropic exit temp]
      V2  = R*T2 / P2                        [ideal gas, nozzle exit]
      Vth = R*Tt / pt                        [ideal gas, nozzle throat]

    Parts:
      a)  v2      Eq. 3-16: sqrt(2k/(k-1)*R*T1*[1-(P2/P1)^((k-1)/k)])
      b)  vth     sqrt(k*R*Tt)                    [Eq. 3-23: throat velocity]
      c)  A2      m_dot * V2 / v2             [continuity, specific-vol approach]
      d)  Isp     Eq. 2-5: v2 / g0           [optimum expansion => c = v2]
      e)  At      m_dot * Vth / vt            [continuity, specific-vol approach]
      f)  A2/At   from parts c) and e)
      g)  A2      At * (A2/At) via Eq. 3-25  [cross-check on part c)]
      h)  M2      Eq. 3-13 inverse: sqrt([(P1/P2)^((k-1)/k)-1]*2/(k-1))
      i)  T2      from intermediate above
    """
    # ---- Unit conversion & derived constants ----------------------------
    p1    = p1_psia * 6_894.757          # psia -> Pa
    R     = R_univ / M_w                 # specific gas constant  [J/kg-K]
    p2    = p3                           # optimum expansion: P2 = P3
    p2_p1 = p2 / p1

    # ---- Intermediate thermodynamic states ------------------------------
    # Chamber
    V1 = R * T1 / p1                     # specific volume at chamber  [m^3/kg]

    # Throat  (Eqs. 3-22, 3-23)
    pt  = p1 * (2.0 / (k + 1)) ** (k / (k - 1))   # critical pressure  [Pa]
    Tt  = 2.0 * T1 / (k + 1)                        # Eq. 3-22  [K]
    vt  = np.sqrt(k * R * Tt)                        # Eq. 3-23  [m/s]
    Vth = R * Tt / pt                                # specific volume at throat

    # Exit  (isentropic, Eq. 3-7)
    T2  = T1 * p2_p1 ** ((k - 1) / k)              # exit temperature  [K]
    V2  = R * T2 / p2                               # specific volume at exit

    # ---- Part a: exit velocity (Eq. 3-16) --------------------------------
    v2 = np.sqrt((2.0 * k / (k - 1)) * R * T1 * (1.0 - p2_p1 ** ((k - 1) / k)))

    # ---- Mass flow rate (optimum: c = v2, F = m_dot*v2) ------------------
    m_dot = F / v2                                   # Eq. 2-16 rearranged

    # ---- Part b: Vth (already computed above) ----------------------------

    # ---- Part c: A2 via continuity (specific volume approach) ------------
    A2_sv   = m_dot * V2 / v2                        # [m^2]
    A2_sv_cm = A2_sv * 1e4                           # [cm^2]

    # ---- Part d: specific impulse (Eq. 2-5) ------------------------------
    Isp = v2 / g0

    # ---- Part e: At via continuity (specific volume approach) ------------
    At      = m_dot * Vth / vt                       # [m^2]
    At_cm   = At * 1e4                               # [cm^2]

    # ---- Part f: area ratio ----------------------------------------------
    eps_calc = A2_sv / At

    # ---- Part g: A2 cross-check via Eq. 3-25 area ratio ------------------
    At_A2_eq325 = (
        ((k + 1) / 2.0) ** (1.0 / (k - 1))
        * p2_p1 ** (1.0 / k)
        * np.sqrt((k + 1) / (k - 1) * (1.0 - p2_p1 ** ((k - 1) / k)))
    )
    eps_3_25 = 1.0 / At_A2_eq325
    A2_check_cm = At_cm * eps_3_25                   # [cm^2]

    # ---- Part h: exit Mach number (Eq. 3-13 inverse) --------------------
    M2 = np.sqrt(((1.0 / p2_p1) ** ((k - 1) / k) - 1.0) * 2.0 / (k - 1))

    # ---- Part i: T2 (already computed above) ----------------------------

    # ---- Output ----------------------------------------------------------
    print(f"\n{SEP}")
    print("  Test 1 / Q1: LOX/CH4 Ideal Nozzle Design (25,000-N thrust)")
    print(SEP)
    print("  Inputs  (* = from Table 5.5, LOX/CH4 O/F=3.20 by mass):")
    _row("Thrust (F)",                               f"{F:>10.0f}",   "N")
    _row("Chamber pressure (P1)",                    f"{p1_psia:>10.1f}", "psia")
    _row("* Chamber temperature (T1)",               f"{T1:>10.1f}",  "K")
    _row("* Specific heat ratio (k)",                f"{k:>10.2f}")
    _row("* Molecular weight (M_w)",                 f"{M_w:>10.2f}", "g/mol")
    _row("  => Specific gas constant (R = R'/M_w)",  f"{R:>10.3f}",   "J/kg-K")
    _row("Sea-level ambient / exit pressure (P3=P2)",f"{p3:>10.1f}",  "Pa")
    print(DIV)
    print("  Intermediate (thermodynamic states):")
    _row("Chamber specific volume (V1)",             f"{V1:>10.6f}",  "m^3/kg")
    _row("Throat pressure (pt)         [crit. ratio]",f"{pt:>10.1f}", "Pa")
    _row("Throat temperature (Tt)      [Eq. 3-22]",  f"{Tt:>10.2f}", "K")
    _row("Throat velocity (vt)         [Eq. 3-23]",  f"{vt:>10.2f}", "m/s")
    _row("Throat specific volume (Vth)",             f"{Vth:>10.6f}", "m^3/kg")
    _row("Exit temperature (T2)        [Eq. 3-7]",   f"{T2:>10.2f}", "K")
    _row("Exit specific volume (V2)",                f"{V2:>10.5f}",  "m^3/kg")
    _row("Mass flow rate (m_dot = F/v2)",            f"{m_dot:>10.4f}", "kg/s")
    print(DIV)
    print("  Results:")
    _row("a) Exit velocity (v2)         [Eq. 3-16]", f"{v2:>10.2f}",  "m/s")
    _row("b) Throat velocity (vth)      [Eq. 3-23]", f"{vt:>10.2f}",  "m/s")
    _row("c) Nozzle exit area (A2)  [m_dot*V2/v2]", f"{A2_sv_cm:>10.4f}", u"cm\u00b2")
    _row("d) Specific impulse (Isp)    [Eq. 2-5]",  f"{Isp:>10.2f}",  "s")
    _row("e) Nozzle throat area (At) [m_dot*Vth/vt]",f"{At_cm:>10.4f}", u"cm\u00b2")
    _row("f) Nozzle area ratio (A2/At)",             f"{eps_calc:>10.4f}")
    _row("g) Nozzle exit area A2  [At*eps, Eq.3-25]",f"{A2_check_cm:>10.4f}", u"cm\u00b2")
    _row("h) Exit Mach number (M2)     [Eq. 3-13]", f"{M2:>10.4f}")
    _row("i) Exit temperature (T2)     [Eq. 3-7]",  f"{T2:>10.2f}",  "K")
    print(DIV)
    print("  Verification:")
    _row("   A2 parts c) vs g) agreement",           f"{abs(A2_sv_cm-A2_check_cm):>10.4f}", u"cm\u00b2 diff")
    _row("   M2 check: v2 / sqrt(k*R*T2)",           f"{v2/np.sqrt(k*R*T2):>10.4f}", "(= M2)")
    print(f"{SEP}\n")

    return v2, vt, A2_sv_cm, Isp, At_cm, eps_calc, A2_check_cm, M2, T2


if __name__ == "__main__":
    #test1_q1()
    #test1_q2()
    test1_q3()
