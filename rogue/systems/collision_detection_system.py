from typing import (
    cast,
    Optional,
    Tuple,
    Generator,
    List,
    Type,
)

import attr
import pyrsistent
from pyrsistent.typing import PMap

from rogue.generic.functions import evolve
from rogue.generic.ecs import (
    EntityComponentDatabase,
    get_component,
    query_entities,
    Entity,
)
from rogue.components import (
    ComponentUnion,
    PositionComponent,
    VelocityComponent,
    TypeComponent,
    SizeComponent,
    InventoryComponent,
    MoneyComponent,
)
from rogue.systems.common.actions import (
    ActionUnion,
    RemoveEntityAction,
    AddComponentAction,
    RemoveComponentAction,
)
from rogue.systems.common.traits import YieldChangesSystemTrait
from rogue.systems.common.constants import ZERO_VELOCITY_COMPONENT
from rogue.types import TypeEnum, ITEM_TYPES, ENEMY_TYPES

Coordinates = Tuple[int, int]
Grid = PMap[Coordinates, Entity]


def get_entity_type(*, ecdb: EntityComponentDatabase[ComponentUnion], entity: Entity) -> TypeEnum:
    type_component = cast(TypeComponent, get_component(ecdb=ecdb, entity=entity, component_type=TypeComponent))
    return type_component.entity_type


def _populate_grid_entity(
    *, grid: Grid, entity: Entity, position_component: PositionComponent, size_component: Optional[SizeComponent],
) -> Grid:
    if size_component is not None:

        for y_coordinate in range(position_component.y_axis, position_component.y_axis + size_component.height + 1):
            for x_coordinate in [position_component.x_axis, position_component.x_axis + size_component.width]:
                grid_position = (y_coordinate, x_coordinate)
                grid = grid.set(grid_position, entity)

        for x_coordinate in range(position_component.x_axis, position_component.x_axis + size_component.width + 1):
            for y_coordinate in [position_component.y_axis, position_component.y_axis + size_component.height]:
                grid_position = (y_coordinate, x_coordinate)
                grid = grid.set(grid_position, entity)
    else:
        grid_position = (position_component.y_axis, position_component.x_axis)
        grid = grid.set(grid_position, entity)

    return grid


def _populate_grid(*, ecdb: EntityComponentDatabase[ComponentUnion]) -> Grid:
    grid: Grid = pyrsistent.pmap()

    component_types: List[Type[ComponentUnion]] = [
        PositionComponent,
        SizeComponent,
    ]
    for entity, components in query_entities(ecdb=ecdb, component_types=component_types):
        position_component = cast(Optional[PositionComponent], components[PositionComponent])
        size_component = cast(Optional[SizeComponent], components[SizeComponent])

        if position_component is None:
            continue

        grid = _populate_grid_entity(
            grid=grid, entity=entity, position_component=position_component, size_component=size_component,
        )

    return grid


def _move_entity(*, grid: Grid, entity: Entity, coordinates: Coordinates, new_coordinates: Coordinates) -> Grid:
    grid = grid.remove(coordinates)
    grid = grid.set(new_coordinates, entity)
    return grid


def _pick_up_gold(
    *, ecdb: EntityComponentDatabase[ComponentUnion], entity: Entity, gold_entity: Entity
) -> List[Tuple[Entity, ActionUnion]]:
    gold_money_component = cast(
        MoneyComponent, get_component(ecdb=ecdb, entity=gold_entity, component_type=MoneyComponent),
    )
    money_component = cast(MoneyComponent, get_component(ecdb=ecdb, entity=entity, component_type=MoneyComponent))

    new_money_component = evolve(money_component, amount=money_component.amount + gold_money_component.amount)
    return [
        (entity, AddComponentAction(component=new_money_component)),
        (gold_entity, RemoveComponentAction(component_type=PositionComponent)),
    ]


def _pick_up_item(
    *, ecdb: EntityComponentDatabase[ComponentUnion], entity: Entity, item_entity: Entity
) -> List[Tuple[Entity, ActionUnion]]:
    inventory_component = cast(
        InventoryComponent, get_component(ecdb=ecdb, entity=entity, component_type=InventoryComponent),
    )

    new_inventory_component = evolve(inventory_component, entities=inventory_component.entities.add(item_entity))

    return [
        (entity, AddComponentAction(component=new_inventory_component)),
        (item_entity, RemoveComponentAction(component_type=PositionComponent)),
    ]


def _handle_item(
    *,
    ecdb: EntityComponentDatabase[ComponentUnion],
    grid: Grid,
    entity: Entity,
    entity_type: TypeEnum,
    coordinates: Coordinates,
    item_entity: Entity,
    item_entity_type: TypeEnum,
    item_coordinates: Coordinates,
) -> Tuple[Grid, List[Tuple[Entity, ActionUnion]]]:
    actions: List[Tuple[Entity, ActionUnion]] = []
    if item_entity_type == TypeEnum.Gold:
        if entity_type == TypeEnum.Hero:
            actions.extend(_pick_up_gold(ecdb=ecdb, entity=entity, gold_entity=item_entity))
            grid = _move_entity(grid=grid, entity=entity, coordinates=coordinates, new_coordinates=item_coordinates)
        else:
            actions.append((entity, AddComponentAction(component=ZERO_VELOCITY_COMPONENT)))
    else:
        actions.extend(_pick_up_item(ecdb=ecdb, entity=entity, item_entity=item_entity))
        grid = _move_entity(grid=grid, entity=entity, coordinates=coordinates, new_coordinates=item_coordinates)

    return grid, actions


def _handle_enemy(
    *,
    grid: Grid,
    entity: Entity,
    entity_type: TypeEnum,
    coordinates: Coordinates,
    enemy_entity: Entity,
    enemy_coordinates: Coordinates,
) -> Tuple[Grid, List[Tuple[Entity, ActionUnion]]]:
    actions: List[Tuple[Entity, ActionUnion]] = []
    if entity_type == TypeEnum.Hero:
        actions.append((entity, RemoveEntityAction(entity=enemy_entity)))
        grid = _move_entity(grid=grid, entity=entity, coordinates=coordinates, new_coordinates=enemy_coordinates)
    elif entity_type in ENEMY_TYPES:
        actions.append((entity, AddComponentAction(component=ZERO_VELOCITY_COMPONENT)))
    else:
        raise ValueError("Unrecognized case!")
    return grid, actions


def _resolve_collisions(
    *, ecdb: EntityComponentDatabase[ComponentUnion], grid: Grid,
) -> Generator[Tuple[Entity, ActionUnion], None, None]:

    for coordinates in list(grid):
        entity = grid[coordinates]

        velocity_component = cast(
            Optional[VelocityComponent], get_component(ecdb=ecdb, entity=entity, component_type=VelocityComponent)
        )

        if velocity_component is None:
            continue

        y_axis, x_axis = coordinates
        new_coordinates = y_axis + velocity_component.y_axis, x_axis + velocity_component.x_axis

        if new_coordinates in grid:
            other_entity = grid[new_coordinates]

            entity_type = get_entity_type(ecdb=ecdb, entity=entity)
            other_entity_type = get_entity_type(ecdb=ecdb, entity=other_entity)

            if other_entity_type in ITEM_TYPES:
                grid, actions = _handle_item(
                    ecdb=ecdb,
                    grid=grid,
                    entity=entity,
                    entity_type=entity_type,
                    coordinates=coordinates,
                    item_entity=other_entity,
                    item_entity_type=other_entity_type,
                    item_coordinates=new_coordinates,
                )
                yield from actions
            elif other_entity_type in ENEMY_TYPES:
                grid, actions = _handle_enemy(
                    grid=grid,
                    entity=entity,
                    entity_type=entity_type,
                    coordinates=coordinates,
                    enemy_entity=other_entity,
                    enemy_coordinates=new_coordinates,
                )
                yield from actions
            else:
                yield entity, AddComponentAction(component=ZERO_VELOCITY_COMPONENT)
        else:
            grid = _move_entity(grid=grid, entity=entity, coordinates=coordinates, new_coordinates=new_coordinates)


@attr.s(frozen=True, kw_only=True)
class CollisionDetectionSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "CollisionDetectionSystem":
        return cls()

    def __call__(
        self, *, ecdb: EntityComponentDatabase[ComponentUnion]
    ) -> Generator[Tuple[Entity, ActionUnion], None, None]:

        grid = _populate_grid(ecdb=ecdb)

        yield from _resolve_collisions(
            ecdb=ecdb, grid=grid,
        )
