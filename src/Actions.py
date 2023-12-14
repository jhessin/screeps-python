from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def find_energy_storage(s: Structure):
    if s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION:
        return s.energy < s.energyCapacity


class Action:
    @staticmethod
    def gather(creep: Creep, use_storage: bool = False):
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            # Get a random new source and save it
            source = creep.pos.findClosestByPath(FIND_SOURCES)
            if source:
                creep.memory.source = source.id

        # If we're near the source, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(source):
            result = creep.harvest(source)
            if result != OK:
                print("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        else:
            creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffaa00'}})

    @staticmethod
    def store(creep: Creep):
        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = creep.pos.findClosestByPath(FIND_STRUCTURES, {
                'filter': find_energy_storage
            })
            if target is None:
                target = creep.room.controller
            creep.memory.target = target.id

        if target.energyCapacity:
            is_close = creep.pos.isNearTo(target)
        else:
            is_close = creep.pos.inRangeTo(target, 3)

        if is_close:
            # if we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
            if target.energyCapacity:
                result = creep.transfer(target, RESOURCE_ENERGY)
                if result == OK or result == ERR_FULL:
                    del creep.memory.target
                else:
                    print(f"[{creep.name}] Unknown result from creep.transfer({target}, {RESOURCE_ENERGY}): {result}")
            else:
                result = creep.upgradeController(target)
                if result != OK:
                    print(f"[{creep.name}] Unknown result from creep.upgradeController({target}): {result}")
                # Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
                if not creep.pos.inRangeTo(target, 2):
                    creep.moveTo(target, {'visualizePathStyle': { 'stroke': '#ffffff'}})
        else:
            creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})

    @staticmethod
    def build(creep: Creep):
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = creep.pos.findClosestByPath(FIND_CONSTRUCTION_SITES)
            if target is None:
                target = creep.room.controller
            creep.memory.target = target.id

        if creep.pos.inRangeTo(target, 3):
            result = creep.build(target)
            if result != OK:
                print(f"[{creep.name}] Unknown result from creep.build({target}): {result}")
        else:
            creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})

