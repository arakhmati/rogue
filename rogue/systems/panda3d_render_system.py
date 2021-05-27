from collections import deque
import itertools
from pathlib import Path
from typing import (
    Dict,
    Optional,
    Tuple,
    List,
    Type,
    Deque,
)

import attr

try:
    from direct.gui.OnscreenText import OnscreenText
    from direct.showbase.ShowBase import ShowBase, Loader
    from panda3d.core import LPoint3, NodePath
except ImportError:

    class ShowBase:  # type: ignore
        ...


from rogue.generic.ecs import (
    EntityComponentDatabase,
    Entity,
    query,
    get_component,
)
from rogue.components import (
    ComponentUnion,
    PositionComponent,
    TypeComponent,
    SizeComponent,
)
from rogue.systems.common.traits import NoReturnSystemTrait
from rogue.types import TypeEnum

from rogue.assets import get_full_path_to_asset

# define types for global variables used by panda3d
try:
    base: ShowBase
    camera: NodePath
    render: NodePath
    loader: Loader
except NameError:
    ...

RgbaColor = Tuple[int, int, int, int]

BLACK = (0, 0, 0, 1)
WHITE = (255, 255, 255, 1)
HIGHLIGHT = (0, 1, 1, 1)

DEFAULT_COLOR = (128, 128, 128, 1)
HERO_COLOR = (128, 0, 128, 1)
ENEMY_COLOR = (255, 0, 0, 1)
WEAPON_COLOR = (0, 255, 0, 1)
GOLD_COLOR = (255, 215, 0, 1)
POTION_COLOR = (0, 191, 255, 1)
HEALTH_COLOR = (0, 255, 0, 1)
INVENTORY_COLOR = (128, 0, 128, 1)
EQUIPMENT_COLOR = (0, 255, 0, 1)


class Model:
    model_file_name: Optional[Path] = None

    def __init__(self, color: RgbaColor, y_axis: int, x_axis: int):
        self.model = loader.loadModel(self.model_file_name)  # noqa: F821
        self.model.reparentTo(render)  # noqa: F821
        self.set_color(color)
        self.set_position(y_axis=y_axis, x_axis=x_axis)

    def set_position(self, y_axis: int, x_axis: int) -> None:
        self.model.setPos(get_square_position(y_axis=y_axis, x_axis=x_axis))

    def set_color(self, color: RgbaColor) -> None:
        self.model.setColor(color)


class HeroModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "hero.egg.pz")


class HobgoblinModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "hobgoblin.egg.pz")


class IceMonsterModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "orc.egg.pz")


class ItemModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "item.egg.pz")


class OrcModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "ice_monster.egg.pz")


class SquareModel(Model):
    model_file_name = get_full_path_to_asset(Path("panda3d") / "square.egg.pz")


def _type_to_appearance(item_type: TypeEnum) -> Tuple[Optional[Type[Model]], RgbaColor]:
    item_type_to_appearance = {
        TypeEnum.Hero: (HeroModel, HERO_COLOR),
        # Enemies
        TypeEnum.Hobgoblin: (HobgoblinModel, ENEMY_COLOR),
        TypeEnum.IceMonster: (IceMonsterModel, ENEMY_COLOR),
        TypeEnum.Orc: (OrcModel, ENEMY_COLOR),
        # Weapons
        TypeEnum.Dagger: (ItemModel, WEAPON_COLOR),
        TypeEnum.Sword: (ItemModel, WEAPON_COLOR),
        TypeEnum.Mace: (ItemModel, WEAPON_COLOR),
        TypeEnum.DoubleSword: (ItemModel, WEAPON_COLOR),
        # Items
        TypeEnum.Gold: (ItemModel, GOLD_COLOR),
        TypeEnum.Potion: (ItemModel, POTION_COLOR),
        # Doors
        TypeEnum.Door: (None, DEFAULT_COLOR),
    }
    symbol, color = item_type_to_appearance[item_type]
    return symbol, color


def _render_room(
    *, squares: List[List[SquareModel]], position_component: PositionComponent, size_component: SizeComponent
) -> None:
    height, width = size_component.height, size_component.width

    # Left Wall
    x_axis = position_component.x_axis
    for y_axis in range(position_component.y_axis, position_component.y_axis + height):
        squares[y_axis][x_axis].set_color(BLACK)

    # Right Wall
    x_axis = position_component.x_axis + width
    for y_axis in range(position_component.y_axis, position_component.y_axis + height):
        squares[y_axis][x_axis].set_color(BLACK)

    # Top Wall
    y_axis = position_component.y_axis
    for x_axis in range(position_component.x_axis, position_component.x_axis + width):
        squares[y_axis][x_axis].set_color(BLACK)

    # Bottom Wall
    y_axis = position_component.y_axis + height
    for x_axis in range(position_component.x_axis, position_component.x_axis + width + 1):
        squares[y_axis][x_axis].set_color(BLACK)

    # Inside of the Room
    y_axis_start = position_component.y_axis + 1
    x_axis_start = position_component.x_axis + 1

    y_axis_end = y_axis_start + height - 1
    x_axis_end = x_axis_start + width - 1
    for y_axis, x_axis in itertools.product(range(y_axis_start, y_axis_end), range(x_axis_start, x_axis_end)):
        squares[y_axis][x_axis].set_color(WHITE)


# Function for getting the proper position for a given square
def get_square_position(*, y_axis: int, x_axis: int) -> "LPoint3":
    return LPoint3(x_axis, y_axis, 0)


class PandaApp(ShowBase):  # type: ignore
    def __init__(self, *, height: int, width: int):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(
            text="Rogue using Panda3D", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1), pos=(0.95, -0.95), scale=0.07,
        )

        self.disableMouse()  # Disble mouse camera control
        camera.setPosHpr(width // 2 - 5, height // 2 - 50, 25, 0, -35, 0)  # noqa: F821

        # Initialize Squares
        self.squares = [
            [SquareModel(color=HIGHLIGHT, y_axis=y_axis, x_axis=x_axis) for x_axis in range(width)]
            for y_axis in range(height)
        ]
        self.models: Dict[Entity, Model] = {}
        self.taskMgr.step()

    def step(self, ecdb: EntityComponentDatabase[ComponentUnion]) -> None:

        dynamic_entities: Deque[Tuple[Entity, PositionComponent, TypeComponent]] = deque(maxlen=None)

        component_types: List[Type[ComponentUnion]] = [PositionComponent, TypeComponent]
        for entity, (position_component, type_component) in query(ecdb=ecdb, component_types=component_types):
            size_component = get_component(ecdb=ecdb, entity=entity, component_types=SizeComponent)

            # Visualize rooms
            if size_component is not None:
                _render_room(squares=self.squares, position_component=position_component, size_component=size_component)
            else:
                # Defer dynamic entities to make sure all static ones already rendered
                dynamic_entities.append((entity, position_component, type_component))

        # Visualize dynamic entities
        while len(dynamic_entities) > 0:
            entity, position_component, type_component = dynamic_entities.popleft()
            entity_type = type_component.entity_type
            model_class, color = _type_to_appearance(entity_type)

            y_axis, x_axis = position_component.y_axis, position_component.x_axis
            if model_class is None:
                self.squares[y_axis][x_axis].set_color(color)
            else:
                if entity in self.models:
                    model = self.models[entity]
                    model.set_position(y_axis=y_axis, x_axis=x_axis)
                else:
                    model = model_class(color=color, y_axis=y_axis, x_axis=x_axis)
                    self.models[entity] = model

        self.taskMgr.step()


@attr.s(frozen=True, kw_only=True)
class Panda3dRenderSystem(NoReturnSystemTrait):
    app: PandaApp = attr.ib()

    @classmethod
    def create_from_height_and_width(cls, *, height: int, width: int) -> "Panda3dRenderSystem":
        app = PandaApp(height=height, width=width)
        return Panda3dRenderSystem(app=app)

    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> None:
        self.app.step(ecdb=ecdb)
