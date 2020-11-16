import pyrsistent

ENEMY_ENTITY_TYPES = pyrsistent.s("hobgoblin", "ice_monster", "orc")
WEAPON_ENTITY_TYPES = pyrsistent.s("mace", "sword", "double_sword")

ENTITY_TYPES = (
    pyrsistent.pset(["room", "hero", "door", "potion", "gold"]).union(ENEMY_ENTITY_TYPES).union(WEAPON_ENTITY_TYPES)
)
