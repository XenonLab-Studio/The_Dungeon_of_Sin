#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Copyright (C) 2018 Stefano Peris <xenonlab.develop@gmail.com>

Github repository: <https://github.com/XenonLab-Studio/The_Dungeon_of_Sin.git>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import libtcodpy as libtcod
from src.input_handlers import handle_keys
from src.entity import Entity, get_blocking_entities_at_location
from src.render_functions import clear_all, render_all
from src.game_map import GameMap
from src.render_functions import clear_all, render_all
from src.fov_functions import initialize_fov, recompute_fov
from src.game_states import GameStates


def main():
    # variables for the size of the terminal
    screen_width = 80
    screen_height = 50

    # map size
    map_width = 80
    map_height = 45
    
    # number of rooms and size
    room_max_size = 12
    room_min_size = 6
    max_rooms = 30

    # FOV (Field of View)
    fov_algorithm = 0          # is just the default libtcod algorithm.
    fov_light_walls = True     # says whether or not to "light up" walls.
    fov_radius = 10            # is the radius of the player's view.

    # monsters
    max_monsters_per_room = 3

    # These colors serve as walls and ground outside the field of view when I arrive there
    # (hence the "darkness" in the names).
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks = True)
    entities = [player]

    # libtcod font to use. The bit 'arial10x10.png'
    # is the file from which it reads characters and symbols.
    libtcod.console_set_custom_font('img/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # This line creates the screen.
    # I assign the values screen_width and screen_height (80 and 50, respectively),
    # along with a title for the window, and a Boolean value that tells libtcod whether
    # to go in fullscreen mode or not.
    libtcod.console_init_root(screen_width, screen_height, 'The Dungeon of Sin', False)

    con = libtcod.console_new(screen_width, screen_height)

    # initialize the game map.
    # This can go anywhere before the main cycle;
    # I put my own under the initialization of the console.
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    # It's true by default,
    # because we have to calculate it correctly at the start of the game.
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # functions to assist drawing the entities
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)

                    # edit the section where we move the player to set fov_recompute to True.
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
     main()
