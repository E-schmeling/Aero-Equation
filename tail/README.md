# Horizontal-tail equation symbols

The symbolic relationship is Roskam, *Airplane Design, Part VII*, Eq. 2.39,
p. 44. The main-gear inertia relation is from page 43. The user reports using
the 2018 printing, ISBN 9781884885549; the relevant page excerpts have not been
provided for independent source checking. The names below follow the project's
variable names. Meanings described as user-confirmed reflect the project
definitions supplied so far. Textbook-specific signs, reference points, and
calculation methods still require comparison with the cited Roskam printing.

The equation gives `S_h`; it does not calculate all its other inputs.
Use the cited source or other documented aircraft-design equations to obtain
those inputs. The example uses US customary units consistently: lengths in ft,
forces in lbf, dynamic pressure in lbf/ft^2, areas in ft^2, and pitch-axis mass
moment of inertia in slug*ft^2. Pitch angular acceleration is retained in the
textbook's stated deg/s^2. For distance directions and signs, use the
coordinate/sign convention in Roskam, Part VII, p. 39. Set selected conditions and preliminary values
together in [design_assumptions.py](./design_assumptions.py), then pass them to
`design_input_substitutions`.

| Symbol | Working meaning | How obtained / status |
| --- | --- | --- |
| `S_h` | Horizontal-tail planform area | Output solved by Eq. 2.39; `ft^2` in the example. |
| `z_T` | Vertical distance from the thrust line to the CG | Aircraft geometry; `ft`. Apply the coordinate directions and sign convention in Roskam, Part VII, p. 39. |
| `T` | Installed thrust | Propulsion installation/performance input for the selected condition; `lbf`. Confirm thrust setting and operating condition used for the sizing case. |
| `z_D` | Vertical distance from the drag-force line to the CG | Aircraft geometry/drag application point; `ft`. Apply the coordinate directions and sign convention in Roskam, Part VII, p. 39. |
| `D` | Drag at initiation of rotation in ground effect | Roskam, Part VII, p. 40, gives `D = C_D_g * qBar * S` using generic `qBar`. For Eq. 2.39 sizing at rotation, this implementation assumes that `qBar` is evaluated at rotation and writes it as `qBar_rot`. In US customary units, `C_D_g` is dimensionless, `qBar_rot` is in `lbf/ft^2`, and `S` is in `ft^2`, giving `D` in `lbf`. |
| `W` | Aircraft weight for the sizing condition | Weight-and-balance / loading input; `lbf`. Confirm which loading condition the equation assumes. |
| `x_mg` | Distance from main gear to the leading edge of the wing MGC | Landing-gear/wing geometry; `ft`. Apply the coordinate directions and sign convention in Roskam, Part VII, p. 39. |
| `x_cg` | Longitudinal CG coordinate from the wing MGC leading-edge reference | Weight-and-balance calculation for the sizing condition; `ft`. Use the same datum/direction as `x_mg` and `x_ac_*`, following Roskam, Part VII, p. 39. |
| `MGC` | Mean geometric chord of the wing | The user-defined `x_mg` reference is the leading edge of the wing MGC. Keep all longitudinal coordinates on one datum; the exact Roskam datum and sign should be checked against Part VII, p. 39. |
| `mew_g` (`\mu_g`) | Ground-friction coefficient | `DesignInputs` selects a ground condition or manual coefficient. Presets are user-provided. |
| `z_mg` | Vertical distance from the CG to the main-gear/ground contact point | Landing-gear geometry; `ft`. Apply the coordinate directions and sign convention in Roskam, Part VII, p. 39. |
| `L_wf` | Wing-fuselage lift in ground effect during the ground roll | Roskam, Part VII, p. 41, gives `L_wf = C_L_wf * qBar * S` using generic `qBar`. For Eq. 2.39 sizing at rotation, this implementation assumes that `qBar` is evaluated at rotation and writes it as `qBar_rot`. |
| `x_ac_wf` | Longitudinal coordinate of the wing-fuselage aerodynamic center | This interpretation follows the project definition of `C_m_ac_wf_g` as a moment about that aerodynamic center. Obtain from aerodynamic analysis; `ft`. Confirm its exact reference datum and sign against Roskam, Part VII, p. 39. |
| `C_m_ac_wf_g` | Pitching-moment coefficient about the wing/fuselage aerodynamic center in the gear-down configuration | Dimensionless. Can be calculated in ground effect using the more extensive method in Roskam, Part VI, Chapter 8, or approximated by `1.1 * (b_f / b) * c_m_ac_f` (the approximation described in Part VII). The example uses the approximation; the helper is `wing_fuselage_pitching_moment_approximation()`. |
| `qBar_rot` | Dynamic pressure at rotation | Eq. 2.39 uses pressure at rotation. Roskam's drag relation (p. 40) and wing-fuselage lift relation (p. 41) write generic `qBar`; using `qBar_rot` for both is this implementation's stated assumption when sizing the tail at rotation. Calculate `qBar_rot = 0.5 * rho * V_rot**2`; use density in `slug/ft^3` and speed in `ft/s` to obtain `lbf/ft^2`. |
| `rho` | Air density | Atmospheric condition at the selected rotation state; `slug/ft^3` in the example. Used with airspeed to calculate dynamic pressure. |
| `V_rot` | Aircraft airspeed at initiation of rotation | Selected rotation condition; `ft/s` in the dynamic-pressure calculation. Use airspeed relative to the surrounding air, not groundspeed. |
| `S` | Wing reference area | Aircraft geometry; `ft^2`. Use the same reference area for `C_D_g` and `C_L_wf`. |
| `C_D_g` | Drag coefficient in ground effect | Aerodynamic data or analysis at rotation; dimensionless. The helper equation `D = C_D_g * qBar_rot * S` is available as `drag_in_ground_effect_equation()`. |
| `C_L_wf` | Airplane lift coefficient during the ground roll in ground effect | Aerodynamic data or analysis at rotation; dimensionless. The helper equation `L_wf = C_L_wf * qBar_rot * S` is available as `wing_fuselage_lift_in_ground_effect_equation()`. |
| `b_f` | Flap span | Aircraft high-lift geometry; `ft`. Used with wingspan to form the dimensionless span ratio `b_f / b`. |
| `b` | Wingspan | Aircraft geometry; `ft`. Use the same span convention as `b_f`. |
| `c_m_ac_f` | Airfoil pitching-moment coefficient with flaps down in the takeoff configuration | Dimensionless aerodynamic coefficient for the takeoff flap setting. Flap-effect methods are in Roskam, Part VI, section 8.2.2.1. |
| `cBar` | Mean aerodynamic chord | Wing geometry/aerodynamic geometry calculation; `ft`. |
| `I_yy_mg` | Pitch-axis mass moment of inertia about the main-gear ground-contact point | Derived using Roskam, Part VII, p. 43: `I_yy_mg = I_yy + (W/g) * (z_mg^2 + (x_mg - x_cg)^2)`. In US customary units, use `W` in lbf, `g` in ft/s^2, offsets in ft, and inertia in slug*ft^2. Signed offsets follow the p. 39 convention; their squares make the parallel-axis distance contribution non-negative. |
| `I_yy` | Airplane pitch-axis mass moment of inertia about the CG | Mass-properties calculation; `slug*ft^2`. |
| `g` | Gravitational acceleration | Use consistent units; the example uses standard gravity `32.174 ft/s^2`. |
| `thetaDotDot` (`\ddot{\theta}`) | Pitch angular acceleration at initiation of rotation | Roskam, Part VII, p. 44, gives preliminary values in deg/s^2: large transport 6, small transport 8, light airplane 10, with a manual option. Defaults to light airplane when unspecified. The code returns values in deg/s^2 without conversion. |
| `x_ac_h` | Longitudinal coordinate of the horizontal-tail aerodynamic center | Tail geometry/aerodynamic analysis; `ft`. Use the same aircraft datum and sign convention as `x_mg`, `x_cg`, and `x_ac_wf`; confirm against Roskam, Part VII, p. 39. |
| `C_L_h_max` | Maximum lift coefficient of the horizontal tail | As clarified by the user, it depends on tail design and the tail's ground-effect behavior throughout rotation; the full determination process is in Roskam, Part VI. The current `-0.8` default, `-1.2` option, and `-0.35 * A_t**(1/3)` option are preliminary project assumptions, not verified Part VI results. Their applicability and coefficient sign remain unconfirmed against the source. A manual value takes precedence; set `horizontal_tail_lift_method=None` to leave the coefficient symbolic. |
| `A_t` | Horizontal-tail aspect ratio used in the fixed-stabilizer lift-coefficient estimate | Aircraft geometry/design input; dimensionless. Supplied to `DesignInputs` as `horizontal_tail_aspect_ratio`. Verify that this is the aspect-ratio definition intended by Roskam's relation. |

## Assumptions needing a source check

- The 2018 printing (ISBN 9781884885549) is identified by the user, but page
  excerpts have not been provided. The equation's moment reference, coordinate
  axes, signs, and source-specific symbol meanings have not been independently
  checked against the book.
- The friction and pitch-acceleration presets were supplied for this project;
  their source tables and applicability have not been independently checked.
- The horizontal-tail lift presets are preliminary project assumptions. The
  actual `C_L_h_max` must be determined for the tail design and rotation
  ground-effect condition using the Part VI method.
- Values of `qBar_rot`, `L_wf`, `D`, and the aerodynamic coefficients depend on
  the chosen aircraft and rotation condition; this area equation alone does not
  produce them.
- The `C_m_ac_wf_g` approximation uses flap span ratio and the flap-down
  airfoil pitching-moment coefficient; for a more detailed estimate, use the
  Part VI Chapter 8 method and calculate it for the gear-down ground-effect
  condition.

See the project-root [solve_horizontal_tail.py](../solve_horizontal_tail.py)
for an illustrative solve. Its sample numbers are placeholders, not design
recommendations.

## Tail-volume-coefficient sizing

The separate module
[volume_coefficients.py](./volume_coefficients.py) provides symbolic
relationships for preliminary horizontal- and vertical-tail sizing:

- Horizontal tail: `V_h = S_h * L_h / (S * cBar)`, so
  `S_h = V_h * S * cBar / L_h`.
- Vertical tail: `V_v = S_v * L_v / (S * b)`, so
  `S_v = V_v * S * b / L_v`.

Here, `L_h` and `L_v` are the distances between the corresponding tail and
wing mean aerodynamic centers. These volume coefficients and moment arms are
typically selected from comparable-aircraft historical data or another
documented design method; they are not derived by the Roskam Part VII rotation
equation above. The method and illustrative values in the accompanying source
are from the Computational Design Laboratory tail-sizing page, which cites
Raymer section 6.5, Roskam Part II chapter 8, and Nicolai & Carichner chapter
11: <https://computationaldesignlab.github.io/aircraft-design/tail_sizing.html>.
Treat the provided values as example inputs, not recommendations.

The module also returns symbolic trapezoidal-planform relations for span,
root/tip chord, mean aerodynamic chord, and its spanwise position. For a
symmetric horizontal tail, span is full span and `y_mac_h` is measured out from
the centerline. For a single vertical tail, `b_v` is the one-sided height and
`y_mac_v` is measured up from its root; this accounts for the factor of two
relative to the horizontal-tail `y_mac` expression. Planform aspect ratio and
taper ratio remain explicit design inputs.

Run `python solve_tail_volume_coefficients.py` for the source page's
illustrative horizontal- and vertical-tail inputs and resulting planform
estimates. Those values are separate from the aircraft-specific rotation
example in `solve_horizontal_tail.py`.
