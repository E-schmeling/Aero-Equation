"""Symbolic tail-volume-coefficient sizing and trapezoidal planform relations."""

import sympy as sp


S_h, V_h, L_h, S, cBar = sp.symbols(
    "S_h V_h L_h S cBar",
    real=True,
)
S_v, V_v, L_v, b = sp.symbols(
    "S_v V_v L_v b",
    real=True,
)

A_h, b_h, taper_ratio_h, c_root_h, c_tip_h, mac_h, y_mac_h = sp.symbols(
    "A_h b_h taper_ratio_h c_root_h c_tip_h mac_h y_mac_h",
    real=True,
)
A_v, b_v, taper_ratio_v, c_root_v, c_tip_v, mac_v, y_mac_v = sp.symbols(
    "A_v b_v taper_ratio_v c_root_v c_tip_v mac_v y_mac_v",
    real=True,
)


def horizontal_tail_volume_coefficient_equation() -> sp.Equality:
    """Return V_h = S_h * L_h / (S * cBar)."""
    return sp.Eq(V_h, S_h * L_h / (S * cBar))


def horizontal_tail_area_from_volume_coefficient_equation() -> sp.Equality:
    """Return the horizontal-tail area sizing relation from V_h."""
    return sp.Eq(S_h, V_h * S * cBar / L_h)


def vertical_tail_volume_coefficient_equation() -> sp.Equality:
    """Return V_v = S_v * L_v / (S * b)."""
    return sp.Eq(V_v, S_v * L_v / (S * b))


def vertical_tail_area_from_volume_coefficient_equation() -> sp.Equality:
    """Return the vertical-tail area sizing relation from V_v."""
    return sp.Eq(S_v, V_v * S * b / L_v)


def horizontal_tail_trapezoidal_planform_equations() -> tuple[sp.Equality, ...]:
    """Return trapezoidal horizontal-tail span, chord, and MAC relations.

    b_h is the full span of the symmetric horizontal tail. y_mac_h is measured
    outward from the aircraft centerline to the MAC location.
    """
    return (
        sp.Eq(b_h, sp.sqrt(A_h * S_h)),
        sp.Eq(c_root_h, 2 * S_h / (b_h * (1 + taper_ratio_h))),
        sp.Eq(c_tip_h, taper_ratio_h * c_root_h),
        sp.Eq(
            mac_h,
            2
            * c_root_h
            * (1 + taper_ratio_h + taper_ratio_h**2)
            / (3 * (1 + taper_ratio_h)),
        ),
        sp.Eq(
            y_mac_h,
            b_h * (1 + 2 * taper_ratio_h) / (6 * (1 + taper_ratio_h)),
        ),
    )


def vertical_tail_trapezoidal_planform_equations() -> tuple[sp.Equality, ...]:
    """Return trapezoidal vertical-tail height, chord, and MAC relations.

    b_v is the full vertical-tail height. y_mac_v is measured upward from the
    vertical-tail root; unlike the horizontal-tail expression, it uses the
    one-sided vertical height rather than a symmetric full span.
    """
    return (
        sp.Eq(b_v, sp.sqrt(A_v * S_v)),
        sp.Eq(c_root_v, 2 * S_v / (b_v * (1 + taper_ratio_v))),
        sp.Eq(c_tip_v, taper_ratio_v * c_root_v),
        sp.Eq(
            mac_v,
            2
            * c_root_v
            * (1 + taper_ratio_v + taper_ratio_v**2)
            / (3 * (1 + taper_ratio_v)),
        ),
        sp.Eq(
            y_mac_v,
            b_v * (1 + 2 * taper_ratio_v) / (3 * (1 + taper_ratio_v)),
        ),
    )
