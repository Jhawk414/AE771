# Physical constants and reference data for rocket propulsion calculations

# Standard gravity (m/s^2)
g0 = 9.8066

# Sea-level pressure (Pa)
P_SL = 101_325.0

# Standard atmosphere — altitude (m) : pressure (Pa)
# Source: Sutton & Biblarz Appendix 2 (U.S. Standard Atmosphere, NOAA-S/T-1562)
# Pressures computed as: pressure_ratio (from table) * P_SL
#
# Alt (m)   Pressure Ratio      Pressure (Pa)
STD_ATMOSPHERE = {
          0: 1.0000    * P_SL,  # 1.0000
      1_000: 8.8700e-1 * P_SL,  # 8.8700e-1
      3_000: 6.6919e-1 * P_SL,  # 6.6919e-1
      5_000: 5.3313e-1 * P_SL,  # 5.3313e-1
     10_000: 2.6151e-1 * P_SL,  # 2.6151e-1
     25_000: 2.5158e-2 * P_SL,  # 2.5158e-2
     50_000: 7.8735e-4 * P_SL,  # 7.8735e-4
     75_000: 2.0408e-5 * P_SL,  # 2.0408e-5
    100_000: 3.1593e-7 * P_SL,  # 3.1593e-7
    130_000: 1.2341e-8 * P_SL,  # 1.2341e-8
    160_000: 2.9997e-9 * P_SL,  # 2.9997e-9
    200_000: 8.3628e-10 * P_SL, # 8.3628e-10
    300_000: 8.6557e-11 * P_SL, # 8.6557e-11
    400_000: 1.4328e-11 * P_SL, # 1.4328e-11
    600_000: 8.1056e-13 * P_SL, # 8.1056e-13
  1_000_000: 7.4155e-14 * P_SL, # 7.4155e-14
}
