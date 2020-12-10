from collections import deque, Counter as counter
from typing import (
    cast,
    Optional,
    Tuple,
    Generator,
    List,
    Type,
    Deque,
    Dict,
    Counter,
    Set,
)

import attr

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
    AddComponentAction,
    RemoveComponentAction,
)
from rogue.systems.common.traits import YieldChangesSystemTrait
from rogue.systems.common.constants import ZERO_VELOCITY_COMPONENT


Grid = Counter[Tuple[int, int]]
CoordinatesToEntities = Dict[Tuple[int, int], Set[Tuple[Entity, str]]]


def _analyze_entity(
    *,
    grid: Grid,
    coordinates_to_entities: CoordinatesToEntities,
    entity: Entity,
    position_component: PositionComponent,
    velocity_component: Optional[VelocityComponent],
    size_component: Optional[SizeComponent],
    type_component: TypeComponent,
) -> Tuple[Grid, CoordinatesToEntities]:
    if size_component is not None:

        for y_coordinate in range(position_component.y_axis, position_component.y_axis + size_component.height + 1):
            for x_coordinate in [position_component.x_axis, position_component.x_axis + size_component.width]:
                grid_position = (y_coordinate, x_coordinate)
                grid[grid_position] += 1

        for x_coordinate in range(position_component.x_axis, position_component.x_axis + size_component.width + 1):
            for y_coordinate in [position_component.y_axis, position_component.y_axis + size_component.height]:
                grid_position = (y_coordinate, x_coordinate)
                grid[grid_position] += 1

    elif velocity_component is not None:
        y_axis = position_component.y_axis + velocity_component.y_axis
        x_axis = position_component.x_axis + velocity_component.x_axis
        grid_position = (y_axis, x_axis)

        set_of_entities = coordinates_to_entities.get(grid_position, set())
        set_of_entities.add((entity, type_component.entity_type))
        coordinates_to_entities[grid_position] = set_of_entities

        grid[grid_position] += 1

    else:
        grid_position = (position_component.y_axis, position_component.x_axis)

        set_of_entities = coordinates_to_entities.get(grid_position, set())
        set_of_entities.add((entity, type_component.entity_type))
        coordinates_to_entities[grid_position] = set_of_entities

        grid[grid_position] += 1

    return grid, coordinates_to_entities


def _analyze(*, ecdb: EntityComponentDatabase[ComponentUnion]) -> Tuple[Grid, CoordinatesToEntities]:
    grid: Grid = counter()
    coordinates_to_entities: CoordinatesToEntities = {}

    component_types: List[Type[ComponentUnion]] = [
        PositionComponent,
        VelocityComponent,
        SizeComponent,
        TypeComponent,
    ]
    for entity, components in query_entities(ecdb=ecdb, component_types=component_types):
        position_component = cast(Optional[PositionComponent], components[PositionComponent])
        velocity_component = cast(Optional[VelocityComponent], components[VelocityComponent])
        size_component = cast(Optional[SizeComponent], components[SizeComponent])
        type_component = cast(Optional[TypeComponent], components[TypeComponent])

        if position_component is None:
            continue

        assert type_component is not None

        grid, coordinates_to_entities = _analyze_entity(
            grid=grid,
            coordinates_to_entities=coordinates_to_entities,
            entity=entity,
            position_component=position_component,
            velocity_component=velocity_component,
            size_component=size_component,
            type_component=type_component,
        )

    return grid, coordinates_to_entities


def _pick_up_gold(
    *, ecdb: EntityComponentDatabase[ComponentUnion], hero: Entity, inventory_entity: Entity
) -> Generator[Tuple[Entity, ActionUnion], None, None]:
    if hero is not None:
        gold_money_component = cast(
            MoneyComponent, get_component(ecdb=ecdb, entity=inventory_entity, component_type=MoneyComponent),
        )
        money_component = cast(MoneyComponent, get_component(ecdb=ecdb, entity=hero, component_type=MoneyComponent),)

        new_money_component = evolve(money_component, amount=money_component.amount + gold_money_component.amount)
        yield hero, AddComponentAction(component=new_money_component)


def _pick_up_item(
    *, ecdb: EntityComponentDatabase[ComponentUnion], first_moving_entity: Entity, inventory_entity: Entity
) -> Generator[Tuple[Entity, ActionUnion], None, None]:
    inventory_component = cast(
        InventoryComponent, get_component(ecdb=ecdb, entity=first_moving_entity, component_type=InventoryComponent),
    )

    new_inventory_component = evolve(inventory_component, entities=inventory_component.entities.add(inventory_entity))
    yield first_moving_entity, AddComponentAction(component=new_inventory_component)


def _transform(
    *, ecdb: EntityComponentDatabase[ComponentUnion], grid: Grid, coordinates_to_entities: CoordinatesToEntities,
) -> Generator[Tuple[Entity, ActionUnion], None, None]:
    for coordinates, count in grid.most_common():
        if count <= 1:
            return

        inventory_entity_and_type: Optional[Tuple[Entity, str]] = None
        hero: Optional[Entity] = None
        moving_entities: Deque[Entity] = deque(maxlen=None)  # hero or monsters

        for entity, entity_type in coordinates_to_entities.get(coordinates, []):
            if entity_type == "hero":
                hero = entity
                moving_entities.append(entity)
            if entity_type in {"hobgoblin"}:
                moving_entities.append(entity)
            elif entity_type in {"gold", "potion", "sword"}:
                inventory_entity_and_type = (entity, entity_type)

        # Don't do anything if there is no moving entities at this coordinate
        if len(moving_entities) == 0:
            continue

        # Pick up an inventory item if there is one
        if inventory_entity_and_type is not None:
            inventory_entity, inventory_entity_type = inventory_entity_and_type

            # Remove position component of the item, so that it's not rendered and nobody else can pick it up
            yield inventory_entity, RemoveComponentAction(component_type=PositionComponent)

            if inventory_entity_type == "gold":
                if hero is not None:
                    moving_entities.remove(hero)
                    yield from _pick_up_gold(ecdb=ecdb, hero=hero, inventory_entity=inventory_entity)
            else:
                # Let the first moving entity in the deque pick up the item
                first_moving_entity = moving_entities.popleft()
                yield from _pick_up_item(
                    ecdb=ecdb, first_moving_entity=first_moving_entity, inventory_entity=inventory_entity
                )

        for entity in moving_entities:
            # Do not move the entity
            yield entity, AddComponentAction(component=ZERO_VELOCITY_COMPONENT)


@attr.s(frozen=True, kw_only=True)
class CollisionDetectionSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "CollisionDetectionSystem":
        return cls()

    def __call__(
        self, *, ecdb: EntityComponentDatabase[ComponentUnion]
    ) -> Generator[Tuple[Entity, ActionUnion], None, None]:

        grid, coordinates_to_entities = _analyze(ecdb=ecdb)
        yield from _transform(ecdb=ecdb, grid=grid, coordinates_to_entities=coordinates_to_entities)
