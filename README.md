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

| File | Contents |
|------|----------|
| `constants.py` | Shared physical constants (`g0`) and Appendix 2 standard atmosphere table |
| `plot_style.py` | Registers the bundled Charter font and applies `ae771.mplstyle` |
| `ae771.mplstyle` | Shared matplotlib style (Charter font, mathtext config) |
| `Charter Regular.ttf` | Bundled font — no system installation required |
| `HW2.py` | Chapter 2 example problems (Ex 2-1, Ex 2-2) |
| `HW3.py` | HW3: Minuteman first-stage rocket — net thrust & Isp vs. altitude |
| `HW4.py` | HW4: Ex 3-1 ideal nozzle (chamber pressure & area ratio); Fig 3-1 recreation |

## Running

Each file can be run directly.  For `HW2.py`, pass one or more example keys to run only those problems:

```
python HW2.py          # all examples
python HW2.py 2-1      # Example 2-1 only
python HW2.py 2-2      # Example 2-2 only

python HW3.py          # Minuteman thrust/Isp plot
python HW4.py          # Ex 3-1 console output + Fig 3-1 plot
```
