"""Symbolic horizontal-tail sizing equation.

The equation is kept symbolic so it can be solved for different variables or
combined with other relations. Configure selected values together in
``DesignInputs`` and use ``design_input_substitutions`` to apply them.
"""

import sympy as sp

from tail.design_assumptions import (
    DesignInputs,
    ground_friction_value,
    horizontal_tail_lift_coefficient,
    pitch_rotation_acceleration,
)


(
    z_T,
    T,
    z_D,
    D,
    W,
    x_mg,
    x_cg,
    mew_g,
    z_mg,
    L_wf,
    x_ac_wf,
    C_m_ac_wf_g,
    b_f,
    b,
    c_m_ac_f,
    C_D_g,
    C_L_wf,
    qBar_rot,
    S,
    cBar,
    I_yy,
    I_yy_mg,
    g,
    thetaDotDot,
    x_ac_h,
    C_L_h_max,
    S_h,
) = sp.symbols(
    "z_T T z_D D W x_mg x_cg mew_g z_mg L_wf x_ac_wf "
    "C_m_ac_wf_g b_f b c_m_ac_f C_D_g C_L_wf qBar_rot S cBar "
    "I_yy I_yy_mg g thetaDotDot "
    "x_ac_h C_L_h_max S_h",
    real=True,
)


def horizontal_tail_area_equation() -> sp.Equality:
    """Return Roskam's horizontal-tail area relationship in symbolic form.

    Source: Jan Roskam, *Airplane Design, Part VII*, equation 2.39, page 44.
    The project uses the 2018 printing (ISBN 9781884885549). Keep all
    quantities in a consistent unit system.
    """
    # All dimensional values must use a consistent unit system. In the
    # project's US-customary example, forces are lbf, lengths ft, pressure
    # psf, area ft^2, and mass moment of inertia slug*ft^2.
    numerator = (
        -z_T * T
        + z_D * D
        + W * (x_mg - x_cg + mew_g * z_mg)
        - L_wf * (x_mg - x_ac_wf + mew_g * z_mg)
        - C_m_ac_wf_g * qBar_rot * S * cBar
        + I_yy_mg * thetaDotDot
    )
    denominator = (
        qBar_rot * (x_mg - x_ac_h + mew_g * z_mg) * C_L_h_max
    )
    return sp.Eq(S_h, numerator / denominator)


def drag_in_ground_effect_equation() -> sp.Equality:
    """Return drag in ground effect from the drag coefficient.

    Roskam, *Airplane Design, Part VII*, p. 40, writes this relation using
    generic qBar. For Eq. 2.39 sizing at rotation, this implementation assumes
    that qBar is evaluated at rotation and uses qBar_rot. Keep units compatible.
    """
    return sp.Eq(D, C_D_g * qBar_rot * S)


def wing_fuselage_lift_in_ground_effect_equation() -> sp.Equality:
    """Return wing-fuselage lift during the ground roll in ground effect.

    Roskam, *Airplane Design, Part VII*, p. 41, writes this relation using
    generic qBar. For Eq. 2.39 sizing at rotation, this implementation assumes
    that qBar is evaluated at rotation and uses qBar_rot.
    """
    return sp.Eq(L_wf, C_L_wf * qBar_rot * S)


def wing_fuselage_pitching_moment_approximation() -> sp.Equality:
    """Return the flap-span approximation for gear-down pitching moment.

    Roskam, *Airplane Design, Part VII*, p. 44 gives the approximation
    C_m_ac_wf_g = 1.1 * (b_f / b) * c_m_ac_f, where c_m_ac_f is the
    airfoil pitching-moment coefficient with flaps down in the takeoff
    configuration. The detailed method is covered in Part VI, Chapter 8;
    flap effects are addressed in section 8.2.2.1.
    """
    return sp.Eq(C_m_ac_wf_g, 1.1 * (b_f / b) * c_m_ac_f)


def main_gear_pitch_inertia_equation() -> sp.Equality:
    """Return Roskam's parallel-axis relation for inertia about gear contact.

    Source: Jan Roskam, *Airplane Design, Part VII*, page 43. This equation
    uses weight divided by gravitational acceleration to obtain mass.
    """
    return sp.Eq(
        I_yy_mg,
        I_yy + (W / g) * (z_mg**2 + (x_mg - x_cg) ** 2),
    )


def design_input_substitutions(inputs: DesignInputs) -> dict[sp.Symbol, float]:
    """Return only the symbolic substitutions selected by these design inputs."""
    substitutions = {
        mew_g: ground_friction_value(inputs),
        thetaDotDot: pitch_rotation_acceleration(inputs),
    }
    tail_lift_coefficient = horizontal_tail_lift_coefficient(inputs)
    if tail_lift_coefficient is not None:
        substitutions[C_L_h_max] = tail_lift_coefficient
    return substitutions
