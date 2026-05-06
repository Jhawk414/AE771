# AE771 — Rocket Propulsion

Propulsion textbook example problems for AE771 (Rocket Propulsion).

Problems are implemented as parameterized Python functions so that inputs can be
changed and results are printed neatly to the console.

## Textbook

**Rocket Propulsion Elements**, 9th Edition
George P. Sutton & Oscar Biblarz
Wiley, 2017
ISBN: 978-1-118-75388-0

## Structure

| File | Contents                                                                                                                         |
|------|----------------------------------------------------------------------------------------------------------------------------------|
| `constants.py` | Shared physical constants (`g0`, `g0_eng`, `R_UNIV`, `R_UNIV_ENG`) and Appendix 2 standard atmosphere table (SI)                 |
| `plot_style.py` | Registers the bundled Charter font and applies `ae771.mplstyle`                                                                  |
| `ae771.mplstyle` | Shared matplotlib style (Charter font, mathtext config)                                                                          |
| `Charter Regular.ttf` | Bundled font — no system installation required                                                                                   |
| `HW2.py` | Chapter 2 example problems (Ex 2-1, Ex 2-2)                                                                                      |
| `HW3.py` | HW3: Minuteman first-stage rocket — net thrust & Isp vs. altitude                                                                |
| `HW4.py` | HW4: Ex 3-1 ideal nozzle (chamber pressure & area ratio); Fig 3-1 recreation                                                     |
| `HW5.py` | HW5: Ex 3-2 ideal rocket (thrust & Isp, optimum expansion); Fig 3-3 recreation                                                   |
| `HW6.py` | HW6: Fig 3-4 recreation — area & velocity ratios vs. pressure ratio for several k                                                |
| `HW7.py` | HW7: Ex 3-3 ideal nozzle design at altitude; Ex 3-4 thrust coefficient variation & optimum altitude                              |
| `HW9/HW9.py` | HW9: Supersonic nozzle design — Rao (bell) and conical nozzle contours for SSME geometry                                         |
| `HW10.py` | HW10: Acoustic resonance frequencies — first longitudinal, tangential, and radial modes                                          |
| `HW12.py` | HW12: Ex 6-1 LOX/LH2 liquid rocket engine — nozzle areas, propellant weight/volume flow rates, and total propellant requirements |
| `HW13.py` | HW13: Ex 8-1 film coefficient effects on heat transfer rate and wall temperatures in a liquid-cooled thrust chamber              |
| `HW14.py` | HW14: Q1 cooling-passage pressure drop; Q2 film coefficient & wall temperatures in a water-cooled thrust chamber               |
| `HW15.py` | HW15: Table 14-2 recreation — single-stage vs two-stage booster payload comparison (Tsiolkovsky; brentq for two-stage)         |
| `Test1/Test1.py` | Test 1: Take-home exam problems                                                                                                  |
| `Test2/Test2.py` | Test 2: Take-home exam problems                                                                                                   |

## Running

Each file can be run directly.  For `HW2.py`, pass one or more example keys to run only those problems:

```
python HW2.py          # all examples
python HW2.py 2-1      # Example 2-1 only
python HW2.py 2-2      # Example 2-2 only

python HW3.py          # Minuteman thrust/Isp plot
python HW4.py          # Ex 3-1 console output + Fig 3-1 plot
python HW5.py          # Ex 3-2 console output + Fig 3-3 plot
python HW6.py          # Fig 3-4 plot (k = 1.1, 1.25, 1.4, 1.7)
python HW7.py          # Ex 3-3 console output; Ex 3-4 console output
python HW10.py         # Acoustic resonance frequency console output
python HW9/HW9.py      # Rao and conical nozzle contour plots
python HW12.py         # Ex 6-1 console output
python HW13.py         # Ex 8-1 console output
python HW14.py         # Q1 pressure drop; Q2 film coeff & wall temps
python HW15.py         # Table 14-2 single- vs two-stage payload comparison
python Test1/Test1.py  # Test 1 problems
python Test2/Test2.py  # Test 2 problems
```
