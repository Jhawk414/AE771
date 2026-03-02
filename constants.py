# Physical constants and reference data for rocket propulsion calculations

from collections import namedtuple

# Standard gravity (m/s²)
g0 = 9.8066

# Sea-level pressure (Pa)
P_SL = 101325.0

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
