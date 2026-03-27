import plot_style  # noqa: F401
import numpy as np
from constants import R_UNIV

SEP = "=" * 60
DIV = "-" * 60
W   = 40  # label column width


def _row(label, value, unit=""):
    """Print a single aligned output row."""
    print(f"    {label:<{W}}: {value}  {unit}")


def hw10_acoustic_modes(
    p1=68.0,         # MPa    — chamber pressure
    D=0.270,         # m      — internal chamber diameter
    L_cyl=0.500,     # m      — cylindrical section length
    half_angle=45.0, # deg    — nozzle convergent half-angle
    Dt=0.050,        # m      — throat diameter (and wall-curvature radius)
    T=2800.0,        # K      — average chamber gas temperature
    M=20.0,          # kg/kmol — molecular weight
    k=1.20,          # —      — specific heat ratio
):
    """
    HW10 — Liquid-propellant chamber acoustic resonance frequencies.

    Computes the first longitudinal (L1), first tangential (T1), and first
    radial (R1) resonant frequencies for a cylindrical combustion chamber
    using the small-perturbation acoustic (standing-wave) model.

    Assumptions:
      1. Uniform gas composition and temperature throughout the cylindrical
         section (as stated in the problem).
      2. Effective acoustic length = cylindrical section length L_cyl only.
         The convergent section is short (110 mm at 45 deg) relative to the
         cylinder and is reported for reference.
      3. Ideal gas: a = sqrt(k * R * T), where R = R_univ / M.
      4. Chamber modeled as closed-closed resonator for longitudinal modes
         (flat injector face = pressure antinode; nozzle throat ~= pressure
         antinode for low-frequency longitudinal modes).
      5. Transverse (tangential / radial) modes governed by cylindrical
         standing-wave solution; Bessel-function zeros from standard tables.

    Equations used:
      Speed of sound:     a      = sqrt(k * R_univ / M * T)
      Specific gas const: R      = R_univ / M
      Longitudinal (L1):  f_L1   = a / (2 * L_cyl)
      Tangential  (T1):   f_T1   = lambda_T1 * a / (pi * D),  lambda_T1 = 1.8412
      Radial      (R1):   f_R1   = lambda_R1 * a / (pi * D),  lambda_R1 = 3.8317
      Convergent length (ref): L_conv = (D - Dt) / 2 / tan(half_angle)

    Bessel-function derivative zeros (rigid-wall BC on cylindrical wave eqn;
    tabulated in Abramowitz & Stegun Table 9.5 and Sutton Ch. 9):
      J1'(x) = 0  -> x = 1.8412  (lambda_T1, 1st tangential mode)
      J0'(x) = -J1(x) = 0  -> x = 3.8317  (lambda_R1, 1st radial mode)
    """
    # Specific gas constant
    R = R_UNIV / M  # J/(kg·K)

    # Speed of sound in chamber gas
    a = np.sqrt(k * R * T)  # m/s

    # Convergent section length from geometry (for reference)
    L_conv = (D - Dt) / 2.0 / np.tan(np.radians(half_angle))

    # Bessel-function derivative zeros for transverse acoustic modes.
    # Derived from the rigid-wall (zero radial velocity) boundary condition
    # applied to the cylindrical acoustic wave equation.
    # Source: standard math tables (e.g. Abramowitz & Stegun, Table 9.5);
    #         also tabulated in Sutton Ch. 9 (verify exact table/eq. number).
    #   lambda_T1 = 1.8412 : first nonzero root of J1'(x) = 0
    #   lambda_R1 = 3.8317 : first root of J0'(x) = -J1(x) = 0
    lambda_T1 = 1.8412
    lambda_R1 = 3.8317

    # Resonance frequencies
    f_L1 = a / (2.0 * L_cyl)
    f_T1 = lambda_T1 * a / (np.pi * D)
    f_R1 = lambda_R1 * a / (np.pi * D)

    print(f"\n{SEP}")
    print("  HW10: Thrust Chamber Acoustic Resonance Frequencies")
    print(SEP)
    print("  Inputs:")
    _row("Chamber pressure (p1)",               f"{p1:>10.1f}", "MPa")
    _row("Internal chamber diameter (D)",        f"{D:>10.3f}", "m")
    _row("Cylindrical section length (L_cyl)",  f"{L_cyl:>10.3f}", "m")
    _row("Convergent half-angle",               f"{half_angle:>10.1f}", "deg")
    _row("Throat diameter (Dt)",                f"{Dt:>10.3f}", "m")
    _row("Chamber gas temperature (T)",         f"{T:>10.1f}", "K")
    _row("Molecular weight (M)",                f"{M:>10.1f}", "kg/kmol")
    _row("Specific heat ratio (k)",             f"{k:>10.2f}")
    print(DIV)
    print("  Intermediate:")
    _row("Spec. gas constant  R = R_univ / M",  f"{R:>10.2f}", "J/(kg-K)")
    _row("Convergent length (ref)",             f"{L_conv:>10.4f}", "m")
    _row("Speed of sound (a)",                  f"{a:>10.2f}", "m/s")
    _row("Bessel root  lambda_T1",              f"{lambda_T1:>10.4f}")
    _row("Bessel root  lambda_R1",              f"{lambda_R1:>10.4f}")
    print(DIV)
    print("  Results:")
    _row("1st Longitudinal mode (L1)",        f"{f_L1:>10.1f}", "Hz")
    _row("1st Tangential mode   (T1)",        f"{f_T1:>10.1f}", "Hz")
    _row("1st Radial mode       (R1)",        f"{f_R1:>10.1f}", "Hz")
    print(f"{SEP}\n")

    return a, f_L1, f_T1, f_R1


if __name__ == "__main__":
    hw10_acoustic_modes()
