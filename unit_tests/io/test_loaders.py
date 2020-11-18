import pathlib

from pyrsistent import pmap, pset

from rogue.types import (
    EntityComponentSystem,
    Entity,
    TypeComponent,
    AppearanceComponent,
    PositionComponent,
    SizeComponent,
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
                        "TypeComponent": TypeComponent(entity_type="potion"),
                        "AppearanceComponent": AppearanceComponent(symbol="!", color="blue"),
                        "PositionComponent": PositionComponent(y_axis=21, x_axis=24),
                    }
                ),
                Entity(unique_id=5): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="gold"),
                        "AppearanceComponent": AppearanceComponent(symbol="*", color="gold"),
                        "PositionComponent": PositionComponent(y_axis=20, x_axis=23),
                    }
                ),
                Entity(unique_id=0): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="room"),
                        "PositionComponent": PositionComponent(y_axis=15, x_axis=20),
                        "SizeComponent": SizeComponent(height=10, width=20),
                    }
                ),
                Entity(unique_id=6): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="door"),
                        "AppearanceComponent": AppearanceComponent(symbol="+", color="grey"),
                        "PositionComponent": PositionComponent(y_axis=15, x_axis=28),
                    }
                ),
                Entity(unique_id=7): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="door"),
                        "AppearanceComponent": AppearanceComponent(symbol="+", color="grey"),
                        "PositionComponent": PositionComponent(y_axis=25, x_axis=39),
                    }
                ),
                Entity(unique_id=1): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="sword"),
                        "AppearanceComponent": AppearanceComponent(symbol="(", color="green"),
                        "PositionComponent": PositionComponent(y_axis=16, x_axis=23),
                    }
                ),
                Entity(unique_id=2): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="hobgoblin"),
                        "AppearanceComponent": AppearanceComponent(symbol="H", color="red"),
                        "PositionComponent": PositionComponent(y_axis=18, x_axis=25),
                    }
                ),
                Entity(unique_id=3): pmap(
                    {
                        "TypeComponent": TypeComponent(entity_type="hero"),
                        "AppearanceComponent": AppearanceComponent(symbol="#", color="purple"),
                        "PositionComponent": PositionComponent(y_axis=22, x_axis=28),
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
                "TypeComponent": pset(
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
                "SizeComponent": pset([Entity(unique_id=0)]),
            }
        ),
        _systems=pmap({}),
    )

    ecs = load_rogue_entities_and_components_from_input_yaml(input_file_name)

    assert ecs == expected_ecs
