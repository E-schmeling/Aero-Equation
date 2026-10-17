"""Illustrative numerical use of the Roskam horizontal-tail equation.

Run from the project root with:
    python solve_horizontal_tail.py

The numeric values below are placeholders for demonstrating the workflow,
not a valid aircraft design or recommended design inputs.
"""

import sympy as sp

from tail.design_assumptions import (
    DesignInputs,
    GroundCondition,
    HorizontalTailLiftMethod,
    ground_friction_value,
    horizontal_tail_lift_coefficient,
)
from tail.horizontal_tail import (
    C_D_g,
    C_L_wf,
    C_m_ac_wf_g,
    D,
    b,
    b_f,
    c_m_ac_f,
    I_yy,
    I_yy_mg,
    L_wf,
    S,
    S_h,
    T,
    W,
    cBar,
    design_input_substitutions,
    drag_in_ground_effect_equation,
    horizontal_tail_area_equation,
    main_gear_pitch_inertia_equation,
    qBar_rot,
    x_ac_h,
    x_ac_wf,
    x_cg,
    x_mg,
    g,
    z_D,
    z_T,
    z_mg,
    wing_fuselage_lift_in_ground_effect_equation,
    wing_fuselage_pitching_moment_approximation,
)


def calculate_tail_area(
    inputs: dict[sp.Symbol, float],
    design_inputs: DesignInputs,
) -> float:
    area_expression = sp.solve(horizontal_tail_area_equation(), S_h)[0]
    drag_expression = drag_in_ground_effect_equation().rhs
    area_expression = area_expression.subs(D, drag_expression)
    lift_expression = wing_fuselage_lift_in_ground_effect_equation().rhs
    area_expression = area_expression.subs(L_wf, lift_expression)
    moment_expression = wing_fuselage_pitching_moment_approximation().rhs
    area_expression = area_expression.subs(C_m_ac_wf_g, moment_expression)
    inertia_expression = main_gear_pitch_inertia_equation().rhs
    area_expression = area_expression.subs(I_yy_mg, inertia_expression)
    substitutions = design_input_substitutions(design_inputs)
    return float(area_expression.subs(inputs | substitutions))


def main() -> None:
    # Illustrative US customary inputs shared by both cases; replace with
    # aircraft values and verified definitions before using the result.
    aircraft_inputs = {
        z_T: 4.9,  # ft, thrustline to CG vertical distance
        T: 562.0,  # lbf, installed thrust
        z_D: 3.9,  # ft, drag-force line to CG vertical distance
        W: 2698.0,  # lbf
        x_mg: 4.8,  # ft, main gear from wing MGC leading-edge reference
        x_cg: 3.1,  # ft, CG from the same wing MGC leading-edge reference
        z_mg: 3.3,  # ft, CG to main-gear ground contact vertical distance
        C_L_wf: 0.12,  # dimensionless, illustrative ground-roll lift coefficient
        x_ac_wf: 1.2,  # ft from wing MGC leading-edge reference
        b_f: 20.0,  # ft, flap span
        b: 36.0,  # ft, wingspan
        c_m_ac_f: -0.15,  # dimensionless, airfoil moment coefficient, takeoff flaps down
        C_D_g: 0.01,  # dimensionless, placeholder ground-effect drag coefficient
        qBar_rot: 94.0,  # lbf/ft^2 at rotation
        S: 215.0,  # ft^2, wing reference area
        cBar: 4.9,  # ft
        I_yy: 1290.0,  # slug*ft^2, airplane pitch inertia about CG
        g: 32.174,  # ft/s^2
        x_ac_h: 15.0,  # ft from the same longitudinal reference
    }

    drag_value = float(drag_in_ground_effect_equation().rhs.subs(aircraft_inputs))
    lift_value = float(
        wing_fuselage_lift_in_ground_effect_equation()
        .rhs.subs(aircraft_inputs)
    )
    inertia_at_gear = float(
        main_gear_pitch_inertia_equation().rhs.subs(aircraft_inputs)
    )
    base_inputs = DesignInputs()
    base_area = calculate_tail_area(aircraft_inputs, base_inputs)
    print("Base case (all DesignInputs defaults):")
    print(
        f"  ground friction: {ground_friction_value(base_inputs):.2f} (concrete)"
    )
    print(f"  qBar_rot: {aircraft_inputs[qBar_rot]:.1f} lbf/ft^2")
    print(f"  ground-effect drag: {drag_value:.1f} lbf (C_D_g * qBar_rot * S)")
    print(f"  ground-effect wing-fuselage lift: {lift_value:.1f} lbf")
    print(f"  I_yy_mg: {inertia_at_gear:.1f} slug*ft^2 (derived from I_yy)")
    print("  pitch acceleration: 10 deg/s^2")
    print(f"  C_L_h_max: {horizontal_tail_lift_coefficient(base_inputs):.3f}")
    print(f"  horizontal tail area: {base_area:.3f} ft^2")

    # More customized case: fixed stabilizer with a 30%-chord elevator,
    # tail aspect ratio supplied for its preliminary C_L_h_max estimate,
    # soft-ground friction, and a user-selected pitch acceleration.
    detailed_inputs = DesignInputs(
        ground_condition=GroundCondition.SOFT_GROUND,
        manual_pitch_acceleration_deg_s2=12.0,
        horizontal_tail_lift_method=(
            HorizontalTailLiftMethod.FIXED_STABILIZER_MAX_DOWN_LIFT
        ),
        horizontal_tail_aspect_ratio=6.5,
    )
    detailed_area = calculate_tail_area(aircraft_inputs, detailed_inputs)
    print("\nCustomized case:")
    print(
        f"  ground friction: {ground_friction_value(detailed_inputs):.2f} "
        "(soft ground)"
    )
    print(f"  ground-effect wing-fuselage lift: {lift_value:.1f} lbf")
    print(f"  I_yy_mg: {inertia_at_gear:.1f} slug*ft^2 (derived from I_yy)")
    print("  pitch acceleration: 12 deg/s^2 (custom)")
    print(
        "  horizontal-tail aspect ratio: "
        f"{detailed_inputs.horizontal_tail_aspect_ratio:.1f}"
    )
    print(
        "  C_L_h_max: "
        f"{horizontal_tail_lift_coefficient(detailed_inputs):.3f} "
        "(fixed stabilizer relationship)"
    )
    print(f"  horizontal tail area: {detailed_area:.3f} ft^2")

    print(
        "\nAll aircraft numbers above are placeholders, not design values. "
        "Verify Roskam definitions, signs, units, and assumptions before use."
    )


if __name__ == "__main__":
    main()
