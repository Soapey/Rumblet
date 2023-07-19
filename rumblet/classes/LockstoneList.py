from rumblet.classes.Lockstone import Lockstone


class LockstoneList:
    lockstones = {
        "Basic Lockstone": Lockstone(name="Basic Lockstone", sprite_path=None, level_1_capture_rate=0.08),
        "Elemental Lockstone": Lockstone(name="Elemental Lockstone", sprite_path=None, level_1_capture_rate=0.15),
        "Celestial Lockstone": Lockstone(name="Celestial Lockstone", sprite_path=None, level_1_capture_rate=0.22),
        "Esoteric Lockstone": Lockstone(name="Esoteric Lockstone", sprite_path=None, level_1_capture_rate=0.35),
        "Arcanum Lockstone": Lockstone(name="Arcanum Lockstone", sprite_path=None, level_1_capture_rate=0.4),
        "Divine Lockstone": Lockstone(name="Divine Lockstone", sprite_path=None, level_1_capture_rate=999.0),
    }
    basic_lockstone = lockstones.get("Basic Lockstone")
    elemental_lockstone = lockstones.get("Elemental Lockstone")
    celestial_lockstone = lockstones.get("Celestial Lockstone")
    esoteric_lockstone = lockstones.get("Esoteric Lockstone")
    arcanum_lockstone = lockstones.get("Arcanum Lockstone")
    divine_lockstone = lockstones.get("Divine Lockstone")