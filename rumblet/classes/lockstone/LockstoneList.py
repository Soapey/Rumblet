from rumblet.classes.lockstone.Lockstone import Lockstone


class LockstoneList:
    lockstones = {
        "Basic Lockstone": Lockstone(

            name="Basic Lockstone",
            description="The least effective form of lockstone. Used to capture Rumblets as pets.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=0.08
        ),
        "Elemental Lockstone": Lockstone(
            name="Elemental Lockstone",
            description="A lockstone imbued with elemental powers. Can capture stronger Rumblets.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=0.15
        ),
        "Celestial Lockstone": Lockstone(
            name="Celestial Lockstone",
            description="A lockstone with celestial energy. It can capture rare and powerful Rumblets.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=0.22
        ),
        "Esoteric Lockstone": Lockstone(
            name="Esoteric Lockstone",
            description="An enigmatic lockstone. Its capture rate is remarkably high.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=0.35
        ),
        "Arcanum Lockstone": Lockstone(
            name="Arcanum Lockstone",
            description="A lockstone filled with mysterious arcanum. It can capture mythical Rumblets.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=0.4
        ),
        "Divine Lockstone": Lockstone(
            name="Divine Lockstone",
            description="A divine lockstone said to have a perfect capture rate. It can capture any Rumblet with "
                        "certainty.",
            sprite_path=None,
            max_quantity=999,
            base_capture_rate=999.0
        ),
    }
    basic_lockstone = lockstones.get("Basic Lockstone")
    elemental_lockstone = lockstones.get("Elemental Lockstone")
    celestial_lockstone = lockstones.get("Celestial Lockstone")
    esoteric_lockstone = lockstones.get("Esoteric Lockstone")
    arcanum_lockstone = lockstones.get("Arcanum Lockstone")
    divine_lockstone = lockstones.get("Divine Lockstone")
