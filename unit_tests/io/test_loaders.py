import pathlib

from pyrsistent import pmap, pset

from rogue.ecs import (
    EntityComponentSystem,
    Entity,
)
from rogue.components import (
    create_position_component,
    create_velocity_component,
    create_apperance_component,
    create_size_component,
    create_health_component,
    create_money_component,
)
from rogue.io.loaders import load_rogue_entities_and_components_from_input_yaml


def test_load_rogue_entities_and_components_from_input_yaml(
    input_file_name=pathlib.Path("configs") / "sample_room_config.yaml",
):
    expected_ecs = EntityComponentSystem(
        _last_unique_id=8,
        _entities=pmap(
            {
                Entity(unique_id=4): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="!", color="blue"),
                        "PositionComponent": create_position_component(y_axis=21, x_axis=24),
                    }
                ),
                Entity(unique_id=5): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="*", color="gold"),
                        "PositionComponent": create_position_component(y_axis=20, x_axis=23),
                    }
                ),
                Entity(unique_id=0): pmap(
                    {
                        "PositionComponent": create_position_component(y_axis=15, x_axis=20),
                        "SizeComponent": create_size_component(height=10, width=20),
                    }
                ),
                Entity(unique_id=6): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="+", color="grey"),
                        "PositionComponent": create_position_component(y_axis=15, x_axis=28),
                    }
                ),
                Entity(unique_id=7): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="+", color="grey"),
                        "PositionComponent": create_position_component(y_axis=25, x_axis=39),
                    }
                ),
                Entity(unique_id=1): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="(", color="green"),
                        "PositionComponent": create_position_component(y_axis=16, x_axis=23),
                    }
                ),
                Entity(unique_id=2): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="H", color="red"),
                        "PositionComponent": create_position_component(y_axis=18, x_axis=25),
                        "VelocityComponent": create_velocity_component(y_axis=0, x_axis=0),
                        "HealthComponent": create_health_component(amount=100),
                    }
                ),
                Entity(unique_id=3): pmap(
                    {
                        "AppearanceComponent": create_apperance_component(symbol="#", color="purple"),
                        "PositionComponent": create_position_component(y_axis=22, x_axis=28),
                        "VelocityComponent": create_velocity_component(y_axis=0, x_axis=0),
                        "HealthComponent": create_health_component(amount=100),
                        "MoneyComponent": create_money_component(amount=0),
                    }
                ),
            }
        ),
        _components=pmap(
            {
                "AppearanceComponent": pset(
                    [
                        Entity(unique_id=5),
                        Entity(unique_id=1),
                        Entity(unique_id=4),
                        Entity(unique_id=7),
                        Entity(unique_id=3),
                        Entity(unique_id=6),
                        Entity(unique_id=2),
                    ]
                ),
                "PositionComponent": pset(
                    [
                        Entity(unique_id=5),
                        Entity(unique_id=1),
                        Entity(unique_id=4),
                        Entity(unique_id=7),
                        Entity(unique_id=3),
                        Entity(unique_id=0),
                        Entity(unique_id=6),
                        Entity(unique_id=2),
                    ]
                ),
                "VelocityComponent": pset([Entity(unique_id=2), Entity(unique_id=3)]),
                "SizeComponent": pset([Entity(unique_id=0)]),
                "HealthComponent": pset([Entity(unique_id=2), Entity(unique_id=3)]),
                "MoneyComponent": pset([Entity(unique_id=3)]),
            }
        ),
    )

    ecs = load_rogue_entities_and_components_from_input_yaml(input_file_name)

    assert ecs == expected_ecs
