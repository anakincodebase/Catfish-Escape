import os
from typing import *
from enum import Enum, auto
from dataclasses import dataclass, asdict

from . import tiles
from . import ecs
from . import util

@dataclass
class SpriteComponent(ecs.Component):
    img_key: str
    z_index: int = 0

    def __iter__(self):
        return iter(asdict(self).values())

@dataclass
class UITextComponent(ecs.Component):
    text: str
    screen_pos: Tuple[int, int]

@dataclass
class PathfindTargetComponent(ecs.Component):
    graph: util.Graph = None
    plan: List[Tuple[int, int]] = None


class PlayerControlComponent(ecs.Component):
    def __init__(self):
        self.visible: Set[Tuple[int, int]] = set()
        self.discovered: Set[Tuple[int, int]] = set()

        self.do_autowalk: bool = False
        self.autowalk_plan: List[Tuple[int, int]] = None
        self.autowalk_timer: int = 0

@dataclass
class MovementActionComponent(ecs.Component):
    dy: int = 0
    dx: int = 0

    def __iter__(self):
        return iter(asdict(self).values())
    
@dataclass
class DamagableComponent(ecs.Component):
    health: int

@dataclass
class IdleActionComponent(ecs.Component):
    pass

@dataclass
class DumbPeacefulBehaviourComponent(ecs.Component):
    sight_range: int = 2

@dataclass
class SimpleHostileBehaviourComponent(ecs.Component):
    sight_range: int = 4
    last_seen_player_position: Tuple[int, int] = None
        

class HealthComponent(ecs.Component):
    def __init__(self, max_health, health=None):
        self.max_health = max_health

        if health is None:
            self.health = max_health
        else:
            self.health = health

@dataclass
class MeleeAttackComponent(ecs.Component):
    damage: int    

@dataclass
class CollisionComponent(ecs.Component):
    pass

@dataclass
class FleeVulnerabilityComponent(ecs.Component):
    vulnerable_square: Tuple[int, int] = None

@dataclass
class RealtimeLifetimeComponent:
    created: int
    lifetime: int = 500 # in ms

@dataclass
class FloatingTextComponent:
    text: str = "Not set."
    color: Tuple[int, int, int] = (255, 255, 255)
    font: str = os.path.join("res", "fonts", "alagard.ttf")
    destroy_on_tick: bool = True

@dataclass
class PickupComponent:
    player_only: bool = True
    heal_amount: int = 2
    nextlevel_switch: bool =False

@dataclass
class BarTextComponent:
    text: str = "Not set."
    color: Tuple[int, int, int] = (255, 255, 255)
    font: str = os.path.join("res", "fonts", "alagard.ttf")