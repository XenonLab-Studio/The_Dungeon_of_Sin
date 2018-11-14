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
from input_handlers import handle_keys


def main():
    # variables for the size of the terminal
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # libtcod font to use. The bit 'arial10x10.png'
    # is the file from which it reads characters and symbols.
    libtcod.console_set_custom_font('img/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # This line creates the screen.
    # I assign the values screen_width and screen_height (80 and 50, respectively),
    # along with a title for the window, and a Boolean value that tells libtcod whether
    # to go in fullscreen mode or not.
    libtcod.console_init_root(screen_width, screen_height, 'The Dungeon of Sin', False)
    
    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # sets the color for the '@' symbol. The "0" in this function is the console on which it draws.
        # The first argument is '0' (again, the console on which it draws).
        # The next two are the x and y coordinates, in this case 1 and 1.
        # Next, I print the symbol '@' and set the background to 'none' with libtcod.BKGND_NONE.
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        
        libtcod.console_flush()

        #libtcod.console_put_char(0, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
            return True

if __name__ == '__main__':
     main()
