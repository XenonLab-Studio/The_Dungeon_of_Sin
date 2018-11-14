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
from src.entity import Entity
from src.render_functions import clear_all, render_all
from src.game_map import GameMap


def main():
    # variables for the size of the terminal
    screen_width = 80
    screen_height = 50

    # map size
    map_width = 80
    map_height = 45

    # These colors serve as walls and ground outside the field of view when I arrive there
    # (hence the "darkness" in the names).
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

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

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        # functions to assist drawing the entities
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
        if not game_map.is_blocked(player.x + dx, player.y + dy):
            player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
     main()
