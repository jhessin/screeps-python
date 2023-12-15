from enum import Enum, StrEnum
from typing import Tuple

from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Actions(StrEnum):
    IDLE = 'idle'
    MINE_SOURCE = 'mining'
    GATHER_ENERGY = 'gathering'
    STORE_ENERGY = 'storing'
    UPGRADING = 'upgrading'
    BUILDING = 'building'
    ATTACK = 'attacking'


class CreepRoles(Enum):
    Worker = ('worker', (WORK, CARRY, MOVE, MOVE))
    Hauler = ('hauler', (CARRY, MOVE))
    Ranger = ('ranger', (MOVE, MOVE, RANGED_ATTACK, MOVE, ATTACK))
    Attacker = ('attacker', (TOUGH, MOVE, MOVE, ATTACK))
    Healer = ('healer', (MOVE, ATTACK, MOVE, HEAL))

    def __init__(self, name: str, parts: Tuple[str]):
        self.name = name
        self.parts = parts


class CreepManager:
    creep: Creep

    @property
    def role(self) -> CreepRoles:
        r = self.creep.memory.role
        for c in CreepRoles:
            if c.name == r:
                return c
        # As a failsafe check for proper body parts and set the role accordingly.
        if self.creep.getActiveBodyparts(HEAL) > 0:
            self.creep.memory.role = CreepRoles.Healer.name
            return CreepRoles.Healer
        elif self.creep.getActiveBodyparts(RANGED_ATTACK) > 0:
            self.creep.memory.role = CreepRoles.Ranger.name
            return CreepRoles.Ranger
        elif self.creep.getActiveBodyparts(ATTACK) > 0:
            self.creep.memory.role = CreepRoles.Attacker
            return CreepRoles.Attacker
        elif self.creep.getActiveBodyparts(WORK) > 0:
            self.creep.memory.role = CreepRoles.Worker
            return CreepRoles.Worker
        else:
            self.creep.memory.role = CreepRoles.Hauler
            return CreepRoles.Hauler

    @role.setter
    def role(self, value: CreepRoles):
        self.creep.memory.role = value.name

    @property
    def action(self) -> Actions:
        return self.creep.memory.action

    @action.setter
    def action(self, value: Actions):
        self.creep.memory.action = value.value

    @property
    def energy(self) -> int:
        return self.creep.store.getUsedCapacity(RESOURCE_ENERGY)

    @property
    def max_energy(self) -> int:
        return self.creep.store.getCapacity(RESOURCE_ENERGY)

    @property
    def full(self) -> bool:
        return self.creep.store.getFreeCapacity(RESOURCE_ENERGY) == 0

    @property
    def empty(self) -> bool:
        return self.creep.store.getUsedCapacity(RESOURCE_ENERGY) == 0

    def __init__(self, creep: Creep):
        self.creep = creep

    @staticmethod
    def find_creeps_with_role(role: CreepRoles):
        creeps = _(Game.creeps).filter(
            lambda c: c.memory.role == role.name
        ).toArray()
        return creeps

    @staticmethod
    def find_creeps_with_action(action: Actions):
        creeps = _(Game.creeps).filter(
            lambda c: c.memory.action == action.value
        ).toArray()
        return creeps

    def run(self):
        pass
