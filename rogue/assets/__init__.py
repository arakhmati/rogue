from pathlib import Path

_ASSETS_DIR = Path(__file__).parent


def get_full_path_to_asset(relative_path_to_asset: Path) -> Path:
    return _ASSETS_DIR / relative_path_to_asset
