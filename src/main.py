from enum import Enum, auto
import pygame
import os

from . import util
from . import configuration
from . import ecs
from . import graphics
from . import resources
from . import tiles
from . import components
from . import events
from . import inputs
from . import physics
from . import entity_definitions
from . import behaviour
from . import player
from . import gamestep
from . import cleanup
from . import nextdungeon

def main():
    # ECS initialization
    pygame.init()
    game = ecs.TilemapEcs(tiles.Tilemap(configuration.DUNGEON_DIMS))
    clock = pygame.time.Clock()
    
    # Load resources
    res = resources.load_res(configuration.RESOURCES_PATH, tile_scale=configuration.SCALE)

    # System initialization
    graphics_system = graphics.GraphicsSystem(res, tile_scale=configuration.SCALE, window_dimensions=configuration.WINDOW_DIMS)
    user_input_system = inputs.UserInputSystem()
    physics_system = physics.PhysicsSystem()
    behaviour_system = behaviour.BehaviourSystem()
    player_system = player.PlayerSystem()
    gamestep_system = gamestep.GamestepSystem()
    cleanup_system = cleanup.CleanupDeadSystem()
    nextdungeon_system = nextdungeon.NextDungeonSystem()

    game.register_system(graphics_system, events.RenderTickEvent)
    game.register_system(user_input_system, events.UserInputEvent, events.RenderTickEvent)
    game.register_system(physics_system, events.PhysicsTickEvent)
    game.register_system(behaviour_system, events.BehaviourTickEvent)
    game.register_system(player_system, events.UserHoversTileWithMouseEvent, events.UserClicksTileWithMouseEvent, events.UserInputEvent, events.RenderTickEvent, events.AfterPhysicsTickEvent)
    game.register_system(gamestep_system, events.GamestepEvent)
    game.register_system(cleanup_system, events.AfterPhysicsTickEvent)
    game.register_system(nextdungeon_system, events.LoadNextDungeonEvent)

    # Initialise game
    game.emit_event(events.LoadNextDungeonEvent())

    while True:
        pressed_keys = []

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT: 
                return

            if pygame_event.type == pygame.KEYDOWN:
                pressed_keys.append(pygame_event.key)

        if pressed_keys:
            game.emit_event(events.UserInputEvent(pressed_keys))

        pygame.display.flip()
        dt = clock.tick(configuration.TARGET_FPS)
        game.emit_event(events.RenderTickEvent(dt, util.reverse_tuple(pygame.mouse.get_pos()), pygame.mouse.get_pressed()[0]))
 
main() #cmmit this line to run the game with menu
        
# uncommit this line to run the game with menu    
# def run_game():
#     main()  

# if __name__ == "__main__":
#     run_game()  
