# pylint: disable=unused-import

import os

ROGUE_ECS_BACKEND = os.environ.get("ROGUE_ECS", "immutable")
if ROGUE_ECS_BACKEND == "immutable":
    from ecs import (
        Entity,
        ComponentTemplate,
        MapFromComponentTypeToComponent,
        EntityComponentDatabase,
        create_ecdb,
        add_entity,
        remove_entity,
        add_component,
        get_component,
        remove_component,
        query,
        Systems,
        create_systems,
        add_system,
        process_systems,
    )
elif ROGUE_ECS_BACKEND == "mutable":
    from ecs.mutable_ecs import (
        Entity,
        ComponentTemplate,
        MapFromComponentTypeToComponent,
        EntityComponentDatabase,
        create_ecdb,
        add_entity,
        remove_entity,
        add_component,
        get_component,
        remove_component,
        query,
        Systems,
        create_systems,
        add_system,
        process_systems,
    )
else:
    raise ImportError("Couldn't import ECS")
