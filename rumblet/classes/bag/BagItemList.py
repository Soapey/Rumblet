from rumblet.classes.bag.BagItem import BagItem
from rumblet.classes.lockstone.LockstoneList import LockstoneList


class BagItemList:
    items: dict[str, BagItem] = {
        LockstoneList.basic_lockstone.name: LockstoneList.basic_lockstone,
        LockstoneList.elemental_lockstone.name: LockstoneList.elemental_lockstone,
        LockstoneList.celestial_lockstone.name: LockstoneList.celestial_lockstone,
        LockstoneList.esoteric_lockstone.name: LockstoneList.esoteric_lockstone,
        LockstoneList.arcanum_lockstone.name: LockstoneList.arcanum_lockstone,
        LockstoneList.divine_lockstone.name: LockstoneList.divine_lockstone
    }
