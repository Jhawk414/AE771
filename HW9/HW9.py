"""
AE 771 - Supersonic Nozzle Design
Rao (bell) nozzle and conical nozzle for SSME geometry.

Coordinate convention: x = axial (positive downstream from throat),
                       y = radial (distance from centerline).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ─────────────────────────── INPUTS ───────────────────────────────────────────
R_t      = 5.15    # throat radius, in
L_n      = 121.0   # nozzle length (throat to exit plane), in
eps      = 77.5    # area ratio (exit/throat)
theta_n  = 36.0    # inflection angle, degrees (half-angle at the inflection point)

THETA_CONE = 15.0  # conical nozzle half-angle, degrees
# ──────────────────────────────────────────────────────────────────────────────

def compute_rao(R_t, L_n, eps, theta_n_deg):
    """Compute Rao nozzle geometry: arc parameters, parabolic coefficients,
    meeting point, exit point, and theta_e."""
    th_n = np.radians(theta_n_deg)

    # Arc radii and centers (centered on nozzle axis x=0)
    r_inner = 1.5  * R_t   # inner (convergent) arc radius
    r_outer = 0.382 * R_t   # outer (divergent) arc radius
    cy_inner = 2.5  * R_t   # inner arc center y-coordinate
    cy_outer = 1.382 * R_t  # outer arc center y-coordinate

    # Meeting point: where the outer arc slope equals tan(theta_n)
    # Lower half of outer arc: y = cy_outer - sqrt(r_outer^2 - x^2)
    # dy/dx = x / sqrt(r_outer^2 - x^2) = tan(theta_n)
    x_m = r_outer * np.sin(th_n)
    y_m = cy_outer - np.sqrt(r_outer**2 - x_m**2)

    # Exit point
    y_e = np.sqrt(eps) * R_t
    x_e = L_n

    # Solve parabola x = a*y^2 + b*y + c using:
    #   (1) slope at meeting point: 1/(2a*y_m + b) = 1/tan(theta_n)  =>  b = 1/tan - 2a*y_m
    #   (2) exit point: x_e = a*y_e^2 + b*y_e + c
    #   (3) meeting point: x_m = a*y_m^2 + b*y_m + c
    tan_n = np.tan(th_n)
    a = (x_m - y_m/tan_n - x_e + y_e/tan_n) / (-y_m**2 - y_e**2 + 2*y_m*y_e)
    b = 1.0/tan_n - 2*a*y_m
    c = x_e - a*y_e**2 - b*y_e

    # Exit angle: tan(theta_e) = dy/dx|_exit = 1 / (2a*y_e + b)
    theta_e = np.degrees(np.arctan(1.0 / (2*a*y_e + b)))

    params = {
        'r_inner': r_inner, 'r_outer': r_outer,
        'cy_inner': cy_inner, 'cy_outer': cy_outer,
        'x_m': x_m, 'y_m': y_m,
        'x_e': x_e, 'y_e': y_e,
        'a': a, 'b': b, 'c': c,
        'theta_e': theta_e,
    }
    return params


def compute_conical(R_t, eps, theta_cone_deg):
    """Compute conical nozzle geometry: meeting point and cone length."""
    th_c = np.radians(theta_cone_deg)

    # Inner arc (same as Rao): lower half, y = cy_inner - sqrt(r_inner^2 - x^2)
    # Slope dy/dx = x / sqrt(r_inner^2 - x^2) = tan(theta_cone)
    r_inner = 1.5  * R_t
    cy_inner = 2.5 * R_t
    x_c = r_inner * np.sin(th_c)
    y_c = cy_inner - np.sqrt(r_inner**2 - x_c**2)

    # Cone length from throat to exit: (y_exit - y_throat) / tan(theta_cone)
    y_e = np.sqrt(eps) * R_t
    L_cone = (y_e - R_t) / np.tan(th_c)

    params = {
        'r_inner': r_inner, 'cy_inner': cy_inner,
        'x_c': x_c, 'y_c': y_c,
        'y_e': y_e, 'L_cone': L_cone,
    }
    return params


def rao_coordinates(R_t, p, n_inner=60, n_outer=40, n_parab=200):
    """Generate (x, y) coordinate arrays for all three Rao nozzle segments."""
    cy_inner = p['cy_inner']
    r_inner  = p['r_inner']
    r_outer  = p['r_outer']
    cy_outer = p['cy_outer']

    # Inner arc: x from -(r_inner - small offset) to 0, using lower half
    # Lower half: y = cy_inner - sqrt(r_inner^2 - x^2)
    # Arc spans x from -sqrt(r_inner^2 - (2*R_t)^2) to 0 (at throat).
    # Start the arc where y = 2*R_t (arbitrary upstream cutoff, matches example plot).
    # More simply: start at x where y = 2*R_t => (2*R_t - cy_inner)^2 + x^2 = r_inner^2
    x_inner_start = -np.sqrt(r_inner**2 - (2*R_t - cy_inner)**2)
    x_inner = np.linspace(x_inner_start, 0.0, n_inner)
    y_inner = cy_inner - np.sqrt(np.clip(r_inner**2 - x_inner**2, 0, None))

    # Outer arc: x from 0 to x_m (meeting point), using lower half
    x_outer = np.linspace(0.0, p['x_m'], n_outer)
    y_outer = cy_outer - np.sqrt(np.clip(r_outer**2 - x_outer**2, 0, None))

    # Parabola: y from y_m to y_e, x = a*y^2 + b*y + c
    a, b, c = p['a'], p['b'], p['c']
    y_parab = np.linspace(p['y_m'], p['y_e'], n_parab)
    x_parab = a*y_parab**2 + b*y_parab + c

    return (x_inner, y_inner), (x_outer, y_outer), (x_parab, y_parab)


def conical_coordinates(R_t, p, n_inner=60, n_cone=200):
    """Generate (x, y) coordinate arrays for both conical nozzle segments."""
    r_inner  = p['r_inner']
    cy_inner = p['cy_inner']

    # Inner arc: same start as Rao inner arc
    x_inner_start = -np.sqrt(r_inner**2 - (2*R_t - cy_inner)**2)
    x_inner = np.linspace(x_inner_start, p['x_c'], n_inner)
    y_inner = cy_inner - np.sqrt(np.clip(r_inner**2 - x_inner**2, 0, None))

    # Straight cone from meeting point to exit
    y_cone = np.linspace(p['y_c'], p['y_e'], n_cone)
    x_cone = p['x_c'] + (y_cone - p['y_c']) / np.tan(np.radians(THETA_CONE))

    return (x_inner, y_inner), (x_cone, y_cone)


def print_summary(rao, conical):
    """Print a formatted summary of nozzle parameters and outputs."""
    sep  = "─" * 54
    sep2 = "=" * 54

    print(f"\n{'':>2}{sep2}")
    print(f"{'':>2}  AE 771 — Supersonic Nozzle Design Summary")
    print(f"{'':>2}{sep2}")

    print(f"{'':>2}  INPUTS")
    print(f"{'':>2}{sep}")
    print(f"{'':>2}  {'Throat Radius R_t':<30} {R_t:>10.4f}  in")
    print(f"{'':>2}  {'Nozzle Length L_n':<30} {L_n:>10.4f}  in")
    print(f"{'':>2}  {'Area Ratio ε':<30} {eps:>10.2f}")
    print(f"{'':>2}  {'Inflection Angle θ_n':<30} {theta_n:>10.2f}  deg")
    print(f"{'':>2}  {'Cone Half-Angle':<30} {THETA_CONE:>10.2f}  deg")

    print(f"\n{'':>2}  RAO NOZZLE")
    print(f"{'':>2}{sep}")
    print(f"{'':>2}  {'r_outer (0.382·R_t)':<30} {rao['r_outer']:>10.4f}  in")
    print(f"{'':>2}  {'cy_outer (1.382·R_t)':<30} {rao['cy_outer']:>10.4f}  in")
    print(f"{'':>2}  {'Meeting Point x_m':<30} {rao['x_m']:>10.4f}  in")
    print(f"{'':>2}  {'Meeting Point y_m':<30} {rao['y_m']:>10.4f}  in")
    print(f"{'':>2}  {'Parabola a':<30} {rao['a']:>10.6f}")
    print(f"{'':>2}  {'Parabola b':<30} {rao['b']:>10.6f}")
    print(f"{'':>2}  {'Parabola c':<30} {rao['c']:>10.6f}  in")
    print(f"{'':>2}  {'Exit Point x_e':<30} {rao['x_e']:>10.4f}  in")
    print(f"{'':>2}  {'Exit Point y_e = √ε·R_t':<30} {rao['y_e']:>10.4f}  in")
    print(f"{'':>2}  {'Exit Angle θ_e':<30} {rao['theta_e']:>10.4f}  deg")

    print(f"\n{'':>2}  CONICAL NOZZLE")
    print(f"{'':>2}{sep}")
    print(f"{'':>2}  {'Meeting Point x_c':<30} {conical['x_c']:>10.4f}  in")
    print(f"{'':>2}  {'Meeting Point y_c':<30} {conical['y_c']:>10.4f}  in")
    print(f"{'':>2}  {'Cone Length L_cone':<30} {conical['L_cone']:>10.4f}  in")
    print(f"{'':>2}  {'Exit Radius y_e = √ε·R_t':<30} {conical['y_e']:>10.4f}  in")

    ratio = conical['L_cone'] / L_n
    print(f"\n{'':>2}  COMPARISON")
    print(f"{'':>2}{sep}")
    print(f"{'':>2}  {'Rao / Conical length ratio':<30} {1/ratio:>10.4f}")
    print(f"{'':>2}  Rao nozzle is {(1-1/ratio)*100:.1f}% shorter than conical.")
    print(f"{'':>2}{sep2}\n")


def plot_nozzles(rao_coords, con_coords, rao, conical):
    """Plot both nozzles side-by-side; save combined PNG + SVG and individual SVGs."""
    (xi, yi), (xo, yo), (xp, yp) = rao_coords
    (xci, yci), (xcc, ycc) = con_coords

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("AE 771 — Supersonic Nozzle Profiles (SSME)", fontsize=13, y=1.01)

    # ── Rao nozzle ──────────────────────────────────────────────
    ax = axes[0]
    ax.set_title(f"Rao (Bell) Nozzle  |  $θ_n$ = {theta_n}°, $θ_e$ = {rao['theta_e']:.2f}°")
    for x_seg, y_seg, lbl in [(xi, yi, "Inner arc"), (xo, yo, "Outer arc"),
                               (xp, yp, "Parabola")]:
        ax.plot(x_seg,  y_seg, lw=1.8, label=lbl)
        ax.plot(x_seg, -y_seg, lw=1.8, color=ax.lines[-1].get_color())
    ax.axhline(0, color='k', lw=0.6, ls='--')
    ax.axvline(0, color='gray', lw=0.6, ls=':')
    ax.set_xlabel("x (in)")
    ax.set_ylabel("y (in)")
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, lw=0.4, alpha=0.5)

    # ── Conical nozzle ───────────────────────────────────────────
    ax = axes[1]
    ax.set_title(f"Conical Nozzle  |  $θ_{{cone}}$ = {THETA_CONE}°,  $L_{{cone}}$ = {conical['L_cone']:.1f} in")
    for x_seg, y_seg, lbl in [(xci, yci, "Inner arc"), (xcc, ycc, "Cone wall")]:
        ax.plot(x_seg,  y_seg, lw=1.8, label=lbl)
        ax.plot(x_seg, -y_seg, lw=1.8, color=ax.lines[-1].get_color())
    ax.axhline(0, color='k', lw=0.6, ls='--')
    ax.axvline(0, color='gray', lw=0.6, ls=':')
    ax.set_xlabel("x (in)")
    ax.set_ylabel("y (in)")
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, lw=0.4, alpha=0.5)

    plt.tight_layout()
    plt.savefig("nozzle_profiles.png", dpi=150, bbox_inches='tight')
    plt.savefig("nozzle_profiles.svg", bbox_inches='tight')
    plt.show()
    print("  Plots saved to nozzle_profiles.png / nozzle_profiles.svg")


def export_coordinates(rao_coords, con_coords, rao, conical, filename="nozzle_coords.txt"):
    """Write coordinate tables for both nozzles to a plain-text file."""
    (xi, yi), (xo, yo), (xp, yp) = rao_coords
    (xci, yci), (xcc, ycc) = con_coords

    x_rao = np.concatenate([xi, xo, xp])
    y_rao = np.concatenate([yi, yo, yp])
    x_con = np.concatenate([xci, xcc])
    y_con = np.concatenate([yci, ycc])

    hdr = f"{'x (in)':>12}  {'y (in)':>12}  {'-y (in)':>12}"
    row = lambda x, y: f"{x:>12.6f}  {y:>12.6f}  {-y:>12.6f}"

    with open(filename, 'w') as f:
        f.write("AE 771 — Nozzle Coordinates\n")
        f.write("=" * 42 + "\n\n")
        f.write("RAO NOZZLE\n")
        f.write("-" * 42 + "\n")
        f.write(hdr + "\n")
        for x, y in zip(x_rao, y_rao):
            f.write(row(x, y) + "\n")
        f.write("\n\nCONICAL NOZZLE\n")
        f.write("-" * 42 + "\n")
        f.write(hdr + "\n")
        for x, y in zip(x_con, y_con):
            f.write(row(x, y) + "\n")

    print(f"  Coordinates exported to {filename}")


# ─────────────────────────── MAIN ─────────────────────────────────────────────
if __name__ == "__main__":
    rao     = compute_rao(R_t, L_n, eps, theta_n)
    conical = compute_conical(R_t, eps, THETA_CONE)

    print_summary(rao, conical)

    rao_coords = rao_coordinates(R_t, rao)
    con_coords = conical_coordinates(R_t, conical)

    export_coordinates(rao_coords, con_coords, rao, conical)
    plot_nozzles(rao_coords, con_coords, rao, conical)
