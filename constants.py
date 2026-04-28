# Physical constants and reference data for rocket propulsion calculations

from collections import namedtuple

# Standard gravity
g0     = 9.8066   # m/s²   SI
g0_eng = 32.174   # ft/s²  English  (= gc numerically: 32.174 lbm·ft/(lbf·s²))

# Sea-level pressure (Pa)
P_SL = 101325.0

# Universal gas constant
R_UNIV     = 8314.0  # J/(kmol·K)           SI
R_UNIV_ENG = 1545.0  # ft·lbf/(lbmol·°R)   English

# Atmospheric state at a given altitude
#   T   : temperature  (K    for SI table | °R      for English table)
#   P   : pressure     (Pa   for SI table | psia    for English table)
#   rho : density      (kg/m³ for SI table | slug/ft³ for English table)
AtmState = namedtuple('AtmState', ['T', 'P', 'rho'])

# Standard atmosphere — SI units
# Altitude [m], T [K], P [Pa], rho [kg/m³]
# Source: Sutton & Biblarz Appendix 2 (U.S. Standard Atmosphere, NOAA-S/T-1562)
#
#  Alt (m)       T (K)         P (Pa)       rho (kg/m³)
STD_ATMOSPHERE_SI = {
          0: AtmState( 288.150, 101325.000, 1.2250e+00),
      1_000: AtmState( 281.651,  89875.275, 1.1117e+00),
      3_000: AtmState( 268.650,  67805.677, 9.0912e-01),
      5_000: AtmState( 255.650,  54019.397, 7.6312e-01),
     10_000: AtmState( 223.252,  26497.500, 4.1351e-01),
     25_000: AtmState( 221.552,   2549.134, 4.0084e-02),
     50_000: AtmState( 270.650,     79.778, 1.0269e-03),
     75_000: AtmState( 206.650,      2.068, 3.4861e-05),
    100_000: AtmState( 195.080,  3.2012e-2, 5.6040e-07),
    130_000: AtmState( 469.270,  1.2505e-3, 8.1520e-09),
    160_000: AtmState( 696.290,  3.0394e-4, 1.2330e-09),
    200_000: AtmState( 845.560,  8.4741e-5, 2.5410e-10),
    300_000: AtmState( 976.010,  8.7705e-6, 1.9160e-11),
    400_000: AtmState( 995.830,  1.4518e-6, 2.8030e-12),
    600_000: AtmState( 999.850,  8.2130e-8, 2.1370e-13),
  1_000_000: AtmState(1000.000,  7.5138e-9, 3.5610e-15),
}

# =============================================================================
# Table 5-5: Theoretical Chamber Performance of Liquid Rocket Propellant
#            Combinations  (Sutton & Biblarz, 9th ed., Table 5-5, p. 180)
# =============================================================================
# Conditions:
#   - Combustion chamber pressure: 1000 psia (6895 kN/m²)
#   - Nozzle exit pressure: 14.7 psia (1 atm); optimum expansion
#   - Adiabatic combustion; isentropic expansion of ideal gases
#   - Specific gravity at the boiling point is used for oxidizers/fuels that
#     boil below 20°C at 1 atm pressure (see Sutton Eq. 7-1)
#   - Mixture ratios given are for approximate maximum values of I_s
#
# Fields
# ------
#   oxidizer      : oxidizer name (str)
#   fuel          : fuel name (str)
#   mr_mass       : mixture ratio by mass  (oxidizer/fuel) [-]
#   mr_vol        : mixture ratio by volume (oxidizer/fuel) [-]
#   sp_grav       : average specific gravity of the propellant combination [-]
#   T_c           : adiabatic flame / chamber temperature [K]
#   c_star        : characteristic exhaust velocity, c* [m/s];  None if not tabulated
#   M             : mean molecular weight of combustion products [kg/mol]; None if not tabulated
#   Isp_shifting  : specific impulse, shifting equilibrium [s];  None if not tabulated
#   Isp_frozen    : specific impulse, frozen equilibrium   [s];  None if not tabulated
#   k             : ratio of specific heats of combustion products [-]; None if not tabulated
#
# Lookup example:
#   [r for r in TABLE_5_5 if r.oxidizer == 'Oxygen' and r.fuel == 'RP-1']

PropComb = namedtuple('PropComb', [
    'oxidizer', 'fuel',
    'mr_mass', 'mr_vol', 'sp_grav',
    'T_c', 'c_star', 'M',
    'Isp_shifting', 'Isp_frozen', 'k',
])

#                   oxidizer                    fuel               mr_mass mr_vol sp_grav  T_c  c_star    M   Isp_shift Isp_froz    k
TABLE_5_5 = [
    # ── Oxygen ──────────────────────────────────────────────────────────────────────────────────────
    PropComb('Oxygen',                  'Methane',                   3.20,  1.19,  0.81, 3526,  1835, 20.3,   None,  296.0, 1.20),
    PropComb('Oxygen',                  'Methane',                   3.00,  1.11,  0.80, 3526,  1853, None,  311.0,   None, None),
    PropComb('Oxygen',                  'Hydrazine',                 0.74,  0.66,  1.06, 3285,  1871, 18.3,   None,  301.0, 1.25),
    PropComb('Oxygen',                  'Hydrazine',                 0.90,  0.80,  1.07, 3404,  1892, 19.3,  313.0,   None, None),
    PropComb('Oxygen',                  'Hydrogen',                  3.40,  0.21,  0.26, 2959,  2428,  8.9,   None,  386.0, 1.26),
    PropComb('Oxygen',                  'Hydrogen',                  4.02,  0.25,  0.28, 2999,  2432, 10.0,  389.5,   None, None),
    PropComb('Oxygen',                  'RP-1',                      2.24,  1.59,  1.01, 3571,  1774, 21.9,  300.0,  285.4, 1.24),
    PropComb('Oxygen',                  'RP-1',                      2.56,  1.82,  1.02, 3677,  1800, 23.3,   None,   None, None),
    PropComb('Oxygen',                  'UDMH',                      1.39,  0.96,  0.96, 3542,  1835, 19.8,   None,  295.0, 1.25),
    PropComb('Oxygen',                  'UDMH',                      1.65,  1.14,  0.98, 3594,  1864, 21.3,  310.0,   None, None),
    # ── Fluorine ────────────────────────────────────────────────────────────────────────────────────
    PropComb('Fluorine',                'Hydrazine',                 1.83,  1.22,  1.29, 4553,  2128, 18.5,  334.0,   None, 1.33),
    PropComb('Fluorine',                'Hydrazine',                 2.30,  1.54,  1.31, 4713,  2208, 19.4,   None,  365.0, None),
    PropComb('Fluorine',                'Hydrogen',                  4.54,  0.21,  0.33, 3080,  2534,  8.9,   None,  389.0, 1.33),
    PropComb('Fluorine',                'Hydrogen',                  7.60,  0.35,  0.45, 3900,  2549, 11.8,  410.0,   None, None),
    # ── Nitrogen tetroxide ───────────────────────────────────────────────────────────────────────────
    PropComb('Nitrogen tetroxide',      'Hydrazine',                 1.08,  0.75,  1.20, 3258,  1765, 19.5,   None,  283.0, 1.26),
    PropComb('Nitrogen tetroxide',      'Hydrazine',                 1.34,  0.93,  1.22, 3152,  1782, 20.9,  292.0,   None, None),
    PropComb('Nitrogen tetroxide',      '50% UDMH / 50% Hydrazine',  1.62,  1.01,  1.18, 3242,  1652, 21.0,   None,  278.0, 1.24),
    PropComb('Nitrogen tetroxide',      '50% UDMH / 50% Hydrazine',  2.00,  1.24,  1.21, 3372,  1711, 22.6,  289.0,   None, None),
    PropComb('Nitrogen tetroxide',      'RP-1',                      3.40,  1.05,  1.23, 3290,  None, 24.1,   None,  297.0, 1.23),
    PropComb('Nitrogen tetroxide',      'MMH',                       2.15,  1.30,  1.20, 3396,  1747, 22.3,  289.0,   None, None),
    PropComb('Nitrogen tetroxide',      'MMH',                       1.65,  1.00,  1.16, 3200,  1591, 21.7,   None,  278.0, 1.23),
    # ── Red fuming nitric acid ───────────────────────────────────────────────────────────────────────
    PropComb('Red fuming nitric acid',  'RP-1',                      4.10,  2.12,  1.35, 3175,  1594, 24.6,   None,  258.0, 1.22),
    PropComb('Red fuming nitric acid',  'RP-1',                      4.80,  2.48,  1.33, 3230,  1609, 25.8,  269.0,   None, None),
    PropComb('Red fuming nitric acid',  '50% UDMH / 50% Hydrazine',  1.73,  1.00,  1.23, 2997,  1682, 20.6,   None,  272.0, 1.22),
    PropComb('Red fuming nitric acid',  '50% UDMH / 50% Hydrazine',  2.20,  1.26,  1.27, 3172,  1701, 22.4,  279.0,   None, None),
    # ── Hydrogen peroxide (90%) ──────────────────────────────────────────────────────────────────────
    PropComb('Hydrogen peroxide (90%)', 'RP-1',                      7.00,  4.01,  1.29, 2760,  None, 21.7,   None,  297.0, 1.19),
]

# # Conversion factors: SI → English
# _M_TO_FT          = 3.28084        # m     → ft
# _K_TO_R           = 1.8            # K     → °R
# _PA_TO_PSIA       = 1.0 / 6894.757 # Pa    → psia
# _KGPM3_TO_SLUGFT3 = 1.0 / 515.379  # kg/m³ → slug/ft³
#
# # Standard atmosphere — English units
# # Altitude [ft], T [°R], P [psia], rho [slug/ft³]
# # Derived from STD_ATMOSPHERE_SI; altitude keys rounded to the nearest foot.
# STD_ATMOSPHERE_ENG = {
#     round(alt * _M_TO_FT): AtmState(
#         T=atm.T * _K_TO_R, P=atm.P * _PA_TO_PSIA, rho=atm.rho * _KGPM3_TO_SLUGFT3
#     )
#     for alt, atm in STD_ATMOSPHERE_SI.items()
# }
