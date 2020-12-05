import abc
import random
from collections import deque, Counter as counter
from typing import (
    cast,
    Optional,
    Union,
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
import pygame
import pygcurse
from toolz import first

from rogue.generic.functions import evolve
from rogue.filter_functions import is_hero, is_enemy
from rogue.generic.ecs import (
    EntityComponentDatabase,
    Systems,
    add_component,
    query_entities,
    get_systems,
    Entity,
)
from rogue.components import (
    RogueComponentUnion,
    PositionComponent,
    VelocityComponent,
    AppearanceComponent,
    SizeComponent,
)

from rogue.exceptions import QuitGameException, IgnoreTimeStepException


ZERO_VELOCITY_COMPONENT = VelocityComponent.create_from_attributes(x_axis=0, y_axis=0)


@attr.s(frozen=True, kw_only=True)
class NoReturnSystemTrait(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]) -> None:
        ...


@attr.s(frozen=True, kw_only=True)
class YieldChangesSystemTrait:
    @abc.abstractmethod
    def __call__(
        self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:
        ...


@attr.s(frozen=True, kw_only=True)
class PygcurseRenderSystem(NoReturnSystemTrait):
    window: pygcurse.PygcurseWindow = attr.ib()

    @classmethod
    def create_from_height_and_width(cls, *, height: int, width: int) -> "PygcurseRenderSystem":
        window = pygcurse.PygcurseWindow(width=width, height=height)
        return PygcurseRenderSystem(window=window)

    def __call__(self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]) -> None:

        dynamic_entities: Deque[Tuple[PositionComponent, AppearanceComponent]] = deque(maxlen=None)

        component_types: List[Type[RogueComponentUnion]] = [PositionComponent, SizeComponent, AppearanceComponent]
        for _, components in query_entities(ecdb=ecdb, component_types=component_types):
            position_component = cast(Optional[PositionComponent], components[0])
            size_component = cast(Optional[SizeComponent], components[1])
            appearance_component = cast(Optional[AppearanceComponent], components[2])

            assert position_component is not None

            # Visualize rooms
            if size_component is not None:
                height, width = size_component.height, size_component.width

                # Left Wall
                start_pos = position_component.x_axis, position_component.y_axis + 1
                end_pos = position_component.x_axis, position_component.y_axis + height - 1
                self.window.drawline(char="|", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

                # Right Wall
                start_pos = position_component.x_axis + width, position_component.y_axis + 1
                end_pos = position_component.x_axis + width, position_component.y_axis + height - 1
                self.window.drawline(char="|", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

                # Top Wall
                start_pos = position_component.x_axis, position_component.y_axis
                end_pos = position_component.x_axis + width, position_component.y_axis
                self.window.drawline(char="_", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

                # Bottom Wall
                start_pos = position_component.x_axis, position_component.y_axis + height
                end_pos = position_component.x_axis + width, position_component.y_axis + height
                self.window.drawline(char="_", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

                # Inside of the Room
                y_axis = position_component.y_axis + 1
                x_axis = position_component.x_axis + 1
                self.window.fill(char=".", region=(x_axis, y_axis, width - 1, height - 1), fgcolor="grey")

            # Defer dynamic entities to make sure all static ones already rendered
            if appearance_component is not None:
                dynamic_entities.append((position_component, appearance_component))

        # Visualize dynamic entities
        while len(dynamic_entities) > 0:
            position_component, appearance_component = dynamic_entities.popleft()
            self.window.putchar(
                appearance_component.symbol,
                x=position_component.x_axis,
                y=position_component.y_axis,
                fgcolor=appearance_component.color,
            )


@attr.s(frozen=True, kw_only=True)
class MovementSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "MovementSystem":
        return cls()

    def __call__(
        self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:

        component_types: List[Type[RogueComponentUnion]] = [PositionComponent, VelocityComponent]
        for entity, components in query_entities(ecdb=ecdb, component_types=component_types):
            position_component = cast(Optional[PositionComponent], components[0])
            velocity_component = cast(Optional[VelocityComponent], components[1])

            if position_component is None:
                continue

            if velocity_component is None:
                continue

            y_axis = position_component.y_axis + velocity_component.y_axis
            x_axis = position_component.x_axis + velocity_component.x_axis

            new_position_component: PositionComponent = evolve(position_component, y_axis=y_axis, x_axis=x_axis)
            yield entity, new_position_component
            yield entity, ZERO_VELOCITY_COMPONENT


@attr.s(frozen=True, kw_only=True)
class EnemyAISystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "EnemyAISystem":
        return cls()

    RANDOM_VALUE_TO_YX = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0),
    }

    def __call__(
        self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:
        for entity, _ in query_entities(ecdb=ecdb, filter_function=is_enemy):
            random_value = random.randint(0, len(EnemyAISystem.RANDOM_VALUE_TO_YX) - 1)
            y_axis, x_axis = EnemyAISystem.RANDOM_VALUE_TO_YX[random_value]

            velocity_component = VelocityComponent.create_from_attributes(y_axis=y_axis, x_axis=x_axis)
            yield entity, velocity_component


@attr.s(frozen=True, kw_only=True)
class PygameHeroControlSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "PygameHeroControlSystem":
        return cls()

    def __call__(
        self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:

        # Query the hero once
        hero = first(first(query_entities(ecdb=ecdb, filter_function=is_hero)))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise QuitGameException

            if event.type != pygame.KEYDOWN:
                raise IgnoreTimeStepException

            hero_velocity_y, hero_velocity_x = 0, 0

            if event.key == pygame.K_LEFT:
                hero_velocity_x = -1
            elif event.key == pygame.K_RIGHT:
                hero_velocity_x = 1
            elif event.key == pygame.K_UP:
                hero_velocity_y = -1
            elif event.key == pygame.K_DOWN:
                hero_velocity_y = 1
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise QuitGameException
            else:
                raise IgnoreTimeStepException

            yield hero, VelocityComponent.create_from_attributes(y_axis=hero_velocity_y, x_axis=hero_velocity_x)
            return

        raise IgnoreTimeStepException


@attr.s(frozen=True, kw_only=True)
class CollisionDetectionSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "CollisionDetectionSystem":
        return cls()

    @staticmethod
    def _analyze(
        *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Tuple[Counter[Tuple[int, int]], Dict[Tuple[int, int], Set[Tuple[Entity, bool]]]]:
        grid: Counter[Tuple[int, int]] = counter()
        coordinates_to_entities: Dict[Tuple[int, int], Set[Tuple[Entity, bool]]] = {}

        component_types: List[Type[RogueComponentUnion]] = [PositionComponent, VelocityComponent, SizeComponent]
        for entity, components in query_entities(ecdb=ecdb, component_types=component_types):
            position_component = cast(Optional[PositionComponent], components[0])
            velocity_component = cast(Optional[VelocityComponent], components[1])
            size_component = cast(Optional[SizeComponent], components[2])

            assert position_component is not None
            if size_component is not None:

                for y_coordinate in range(
                    position_component.y_axis, position_component.y_axis + size_component.height + 1
                ):
                    for x_coordinate in [position_component.x_axis, position_component.x_axis + size_component.width]:
                        grid_position = (y_coordinate, x_coordinate)
                        grid[grid_position] += 1

                for x_coordinate in range(
                    position_component.x_axis, position_component.x_axis + size_component.width + 1
                ):
                    for y_coordinate in [position_component.y_axis, position_component.y_axis + size_component.height]:
                        grid_position = (y_coordinate, x_coordinate)
                        grid[grid_position] += 1

            elif velocity_component is not None:
                y_axis = position_component.y_axis + velocity_component.y_axis
                x_axis = position_component.x_axis + velocity_component.x_axis
                grid_position = (y_axis, x_axis)

                set_of_entities = coordinates_to_entities.get(grid_position, set())
                set_of_entities.add((entity, True))
                coordinates_to_entities[grid_position] = set_of_entities

                grid[grid_position] += 1

            else:
                grid_position = (position_component.y_axis, position_component.x_axis)

                set_of_entities = coordinates_to_entities.get(grid_position, set())
                set_of_entities.add((entity, False))
                coordinates_to_entities[grid_position] = set_of_entities

                grid[grid_position] += 1

        return grid, coordinates_to_entities

    @staticmethod
    def _transform(
        *, grid: Counter[Tuple[int, int]], coordinates_to_entities: Dict[Tuple[int, int], Set[Tuple[Entity, bool]]],
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:
        for coordinates, count in grid.most_common():
            if count <= 1:
                return

            for entity, has_velocity_component in coordinates_to_entities.get(coordinates, []):
                if not has_velocity_component:
                    continue

                # Do not move the entity
                yield entity, ZERO_VELOCITY_COMPONENT

    def __call__(
        self, *, ecdb: EntityComponentDatabase[RogueComponentUnion]
    ) -> Generator[Tuple[Entity, RogueComponentUnion], None, None]:

        grid, coordinates_to_entities = self._analyze(ecdb=ecdb)
        yield from self._transform(grid=grid, coordinates_to_entities=coordinates_to_entities)


SystemUnion = Union[
    PygcurseRenderSystem, MovementSystem, EnemyAISystem, PygameHeroControlSystem, CollisionDetectionSystem
]


def process_system(
    *, system: SystemUnion, ecdb: EntityComponentDatabase[RogueComponentUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    if isinstance(system, NoReturnSystemTrait):
        system(ecdb=ecdb)
    elif isinstance(system, YieldChangesSystemTrait):
        for entity, component in system(ecdb=ecdb):
            ecdb = add_component(ecdb=ecdb, entity=entity, component=component)
    else:
        raise ValueError(f"System of type {type(system)} does not support any of the system traits!")
    return ecdb


def process_systems(
    *, ecdb: EntityComponentDatabase[RogueComponentUnion], systems: Systems[SystemUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    for system in get_systems(systems=systems):
        ecdb = process_system(system=system, ecdb=ecdb)
    return ecdb
