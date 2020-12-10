import pathlib

from pyrsistent import pmap

from rogue.generic.ecs import (
    EntityComponentDatabase,
    Entity,
)
from rogue.components import (
    PositionComponent,
    VelocityComponent,
    TypeComponent,
    SizeComponent,
    HealthComponent,
    MoneyComponent,
    InventoryComponent,
    EquipmentComponent,
)
from rogue.io.loaders import load_rogue_ecdb_from_input_yaml


def test_load_rogue_ecdb_from_input_yaml(input_file_name=pathlib.Path("configs") / "sample_room_config.yaml",):
    expected_ecdb = EntityComponentDatabase(
        _last_unique_id=8,
        _entities=pmap(
            {
                Entity(unique_id=4): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="potion"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=21, x_axis=24),
                    }
                ),
                Entity(unique_id=5): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="gold"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=20, x_axis=23),
                        MoneyComponent: MoneyComponent.create_from_attributes(amount=50),
                    }
                ),
                Entity(unique_id=0): pmap(
                    {
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=15, x_axis=20),
                        SizeComponent: SizeComponent.create_from_attributes(height=10, width=20),
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="room"),
                    }
                ),
                Entity(unique_id=6): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="door"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=15, x_axis=28),
                    }
                ),
                Entity(unique_id=7): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="door"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=25, x_axis=39),
                    }
                ),
                Entity(unique_id=1): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="sword"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=16, x_axis=23),
                    }
                ),
                Entity(unique_id=2): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="hobgoblin"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=18, x_axis=25),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
                Entity(unique_id=3): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type="hero"),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=22, x_axis=28),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        MoneyComponent: MoneyComponent.create_from_attributes(amount=0),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
            }
        ),
    )

    ecdb = load_rogue_ecdb_from_input_yaml(input_file_name)

    assert ecdb == expected_ecdb
