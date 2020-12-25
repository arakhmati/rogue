from typing import Any
import pathlib

import click

from rogue.cli.rogue_pygcurse import rogue_pygcurse
from rogue.cli.rogue_panda3d import rogue_panda3d


@click.group("rogue")
def rogue() -> None:
    ...


@rogue.command()
@click.argument("input_file_name", type=pathlib.Path)
@click.option("--window_height", type=int, default=50)
@click.option("--window_width", type=int, default=80)
def pygcurse(**kwargs: Any) -> None:
    rogue_pygcurse(**kwargs)


@rogue.command()
@click.argument("input_file_name", type=pathlib.Path)
@click.option("--height", type=int, default=50)
@click.option("--width", type=int, default=80)
def panda3d(**kwargs: Any) -> None:
    rogue_panda3d(**kwargs)
