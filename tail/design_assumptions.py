from dataclasses import dataclass
from enum import Enum
from math import isfinite


class AircraftClass(Enum):
    LARGE_TRANSPORT = "large transport"
    SMALL_TRANSPORT = "small transport"
    LIGHT_AIRPLANE = "light airplane"


PITCH_ROTATION_ACCELERATIONS_DEG_S2: dict[AircraftClass, float] = {
    AircraftClass.LARGE_TRANSPORT: 6.0,
    AircraftClass.SMALL_TRANSPORT: 8.0,
    AircraftClass.LIGHT_AIRPLANE: 10.0,
}


class GroundCondition(Enum):
    CONCRETE = "concrete"
    HARD_TURF = "hard turf"
    SHORT_GRASS = "short grass"
    LONG_GRASS = "long grass"
    SOFT_GROUND = "soft ground"


GROUND_FRICTION_COEFFICIENTS: dict[GroundCondition, float] = {
    GroundCondition.CONCRETE: 0.02,
    GroundCondition.HARD_TURF: 0.04,
    GroundCondition.SHORT_GRASS: 0.05,
    GroundCondition.LONG_GRASS: 0.1,
    GroundCondition.SOFT_GROUND: 0.3,
}


class HorizontalTailLiftMethod(Enum):
    CONTROLLABLE_STABILIZER_ZERO_ELEVATOR = (
        "controllable stabilizer, fixed elevator at zero deflection"
    )
    CONTROLLABLE_STABILIZER_MAX_DOWN_LIFT = (
        "controllable stabilizer, 30% chord elevator at maximum down-lift"
    )
    FIXED_STABILIZER_MAX_DOWN_LIFT = (
        "fixed stabilizer, 30% chord elevator at maximum down-lift"
    )


@dataclass(frozen=True)
class DesignInputs:
    """Selectable ground, rotation, and horizontal-tail sizing inputs.

    Defaults reproduce the project's current concrete and light-airplane
    preliminary values, including the controllable-stabilizer/zero-elevator
    horizontal-tail lift coefficient.
    """

    ground_condition: GroundCondition = GroundCondition.CONCRETE
    manual_ground_friction: float | None = None
    aircraft_class: AircraftClass = AircraftClass.LIGHT_AIRPLANE
    manual_pitch_acceleration_deg_s2: float | None = None
    horizontal_tail_lift_method: HorizontalTailLiftMethod | None = (
        HorizontalTailLiftMethod.CONTROLLABLE_STABILIZER_ZERO_ELEVATOR
    )
    horizontal_tail_aspect_ratio: float | None = None
    manual_C_L_h_max: float | None = None

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.manual_ground_friction is not None:
            value = self.manual_ground_friction
            if not isfinite(value) or value < 0:
                raise ValueError(
                    "manual_ground_friction must be finite and non-negative."
                )

        if self.manual_pitch_acceleration_deg_s2 is not None and not isfinite(
            self.manual_pitch_acceleration_deg_s2
        ):
            raise ValueError("Manual pitch acceleration must be finite.")

        if self.manual_C_L_h_max is not None and not isfinite(self.manual_C_L_h_max):
            raise ValueError("manual_C_L_h_max must be finite.")

        if self.horizontal_tail_lift_method is (
            HorizontalTailLiftMethod.FIXED_STABILIZER_MAX_DOWN_LIFT
        ):
            aspect_ratio = self.horizontal_tail_aspect_ratio
            if aspect_ratio is None or not isfinite(aspect_ratio) or aspect_ratio <= 0:
                raise ValueError(
                    "A positive horizontal_tail_aspect_ratio is required for "
                    "the fixed-stabilizer coefficient method."
                )


def ground_friction_value(inputs: DesignInputs) -> float:
    """Return the selected ground-friction coefficient."""
    if inputs.manual_ground_friction is not None:
        return inputs.manual_ground_friction
    return GROUND_FRICTION_COEFFICIENTS[inputs.ground_condition]


def pitch_rotation_acceleration(inputs: DesignInputs) -> float:
    """Return pitch angular acceleration in deg/s^2, as stated by Roskam.

    Source: Jan Roskam, *Airplane Design, Part VII*, page 44. The value is
    returned in the textbook's stated units without conversion.
    """
    acceleration_deg_s2 = inputs.manual_pitch_acceleration_deg_s2
    if acceleration_deg_s2 is None:
        acceleration_deg_s2 = PITCH_ROTATION_ACCELERATIONS_DEG_S2[
            inputs.aircraft_class
        ]
    return acceleration_deg_s2


def horizontal_tail_lift_coefficient(inputs: DesignInputs) -> float | None:
    """Return a selected preliminary coefficient, or None if not specified.

    The actual maximum depends on tail design and the tail's ground-effect
    behavior throughout rotation; its full determination is covered in Roskam,
    Part VI. These selectable values and the aspect-ratio relationship are
    preliminary project assumptions, not a substitute for that analysis.
    """
    if inputs.manual_C_L_h_max is not None:
        return inputs.manual_C_L_h_max

    method = inputs.horizontal_tail_lift_method
    if method is None:
        return None
    if method is HorizontalTailLiftMethod.CONTROLLABLE_STABILIZER_ZERO_ELEVATOR:
        return -0.8
    if method is HorizontalTailLiftMethod.CONTROLLABLE_STABILIZER_MAX_DOWN_LIFT:
        return -1.2
    if method is HorizontalTailLiftMethod.FIXED_STABILIZER_MAX_DOWN_LIFT:
        assert inputs.horizontal_tail_aspect_ratio is not None
        return -0.35 * inputs.horizontal_tail_aspect_ratio ** (1 / 3)
    raise ValueError(f"Unsupported horizontal-tail lift method: {method!r}")
