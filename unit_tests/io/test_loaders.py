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
from rogue.types import TypeEnum


def test_load_rogue_ecdb_from_input_yaml(input_file_name=pathlib.Path("configs") / "sample_room_config.yaml",):
    expected_ecdb = EntityComponentDatabase(
        _last_unique_id=13,
        _entities=pmap(
            {
                Entity(unique_id=0): pmap(
                    {
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=15, x_axis=20),
                        SizeComponent: SizeComponent.create_from_attributes(height=10, width=20),
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Room),
                    }
                ),
                Entity(unique_id=1): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Sword),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=16, x_axis=23),
                    }
                ),
                Entity(unique_id=2): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Hobgoblin),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=18, x_axis=25),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
                Entity(unique_id=3): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Hero),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=22, x_axis=28),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        MoneyComponent: MoneyComponent.create_from_attributes(amount=0),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
                Entity(unique_id=4): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Potion),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=21, x_axis=24),
                    }
                ),
                Entity(unique_id=5): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Gold),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=20, x_axis=23),
                        MoneyComponent: MoneyComponent.create_from_attributes(amount=50),
                    }
                ),
                Entity(unique_id=6): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Door),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=15, x_axis=28),
                    }
                ),
                Entity(unique_id=7): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Door),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=25, x_axis=39),
                    }
                ),
                Entity(unique_id=8): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Dagger),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=24, x_axis=35),
                    }
                ),
                Entity(unique_id=9): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Mace),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=24, x_axis=22),
                    }
                ),
                Entity(unique_id=10): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.DoubleSword),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=24, x_axis=30),
                    }
                ),
                Entity(unique_id=11): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.IceMonster),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=21, x_axis=32),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
                Entity(unique_id=12): pmap(
                    {
                        TypeComponent: TypeComponent.create_from_attributes(entity_type=TypeEnum.Orc),
                        PositionComponent: PositionComponent.create_from_attributes(y_axis=17, x_axis=34),
                        VelocityComponent: VelocityComponent.create_from_attributes(y_axis=0, x_axis=0),
                        HealthComponent: HealthComponent.create_from_attributes(amount=100),
                        InventoryComponent: InventoryComponent.create_from_attributes(entities=[]),
                        EquipmentComponent: EquipmentComponent.create_from_attributes(entities=[]),
                    }
                ),
            }
        ),
    )

    ecdb = load_rogue_ecdb_from_input_yaml(input_file_name)

    assert ecdb == expected_ecdb
