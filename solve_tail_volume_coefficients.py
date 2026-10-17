"""Illustrative horizontal- and vertical-tail volume-coefficient sizing.

Run from the project root with:
    python solve_tail_volume_coefficients.py

The example values come from the cited Computational Design Laboratory
tail-sizing page and are illustrative, not design recommendations.
"""

import sympy as sp

from tail.volume_coefficients import (
    A_h,
    A_v,
    L_h,
    L_v,
    S,
    S_h,
    S_v,
    V_h,
    V_v,
    b,
    b_h,
    b_v,
    c_root_h,
    c_root_v,
    c_tip_h,
    c_tip_v,
    cBar,
    horizontal_tail_area_from_volume_coefficient_equation,
    horizontal_tail_trapezoidal_planform_equations,
    mac_h,
    mac_v,
    taper_ratio_h,
    taper_ratio_v,
    vertical_tail_area_from_volume_coefficient_equation,
    vertical_tail_trapezoidal_planform_equations,
    y_mac_h,
    y_mac_v,
)


def evaluate_planform(
    equations: tuple[sp.Equality, ...],
    substitutions: dict[sp.Symbol, float],
) -> dict[sp.Symbol, float]:
    values = dict(substitutions)
    for equation in equations:
        values[equation.lhs] = float(
            sp.solve(equation, equation.lhs)[0].subs(values)
        )
    return values


def main() -> None:
    # Example values from the cited page; choose aircraft-specific values
    # and sizing methods for actual design work.
    wing_area = 134.0  # ft^2
    wing_mac = 4.3  # ft
    wing_span = 33.0  # ft

    horizontal_area = float(
        horizontal_tail_area_from_volume_coefficient_equation()
        .rhs.subs({V_h: 0.8, S: wing_area, cBar: wing_mac, L_h: 15.0})
    )
    horizontal_values = evaluate_planform(
        horizontal_tail_trapezoidal_planform_equations(),
        {
            S_h: horizontal_area,
            A_h: 5.5,
            taper_ratio_h: 0.75,
        },
    )
    print("Illustrative horizontal-tail volume-coefficient estimate:")
    print(f"  area: {horizontal_area:.1f} ft^2")
    print(f"  span: {horizontal_values[b_h]:.1f} ft")
    print(f"  root chord: {horizontal_values[c_root_h]:.1f} ft")
    print(f"  tip chord: {horizontal_values[c_tip_h]:.1f} ft")
    print(f"  mean aerodynamic chord: {horizontal_values[mac_h]:.1f} ft")
    print(f"  y_MAC from centerline: {horizontal_values[y_mac_h]:.1f} ft")

    vertical_area = float(
        vertical_tail_area_from_volume_coefficient_equation()
        .rhs.subs({V_v: 0.065, S: wing_area, b: wing_span, L_v: 17.0})
    )
    vertical_values = evaluate_planform(
        vertical_tail_trapezoidal_planform_equations(),
        {
            S_v: vertical_area,
            A_v: 1.3,
            taper_ratio_v: 0.55,
        },
    )
    print("\nIllustrative vertical-tail volume-coefficient estimate:")
    print(f"  area: {vertical_area:.1f} ft^2")
    print(f"  height: {vertical_values[b_v]:.1f} ft")
    print(f"  root chord: {vertical_values[c_root_v]:.1f} ft")
    print(f"  tip chord: {vertical_values[c_tip_v]:.1f} ft")
    print(f"  mean aerodynamic chord: {vertical_values[mac_v]:.1f} ft")
    print(f"  y_MAC from root: {vertical_values[y_mac_v]:.1f} ft")


if __name__ == "__main__":
    main()
