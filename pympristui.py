#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2021 CJ Kucera (cj@apocalyptech.com)
# 
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the authors be held liable for any damages arising from
# the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software in a
#    product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
# 3. This notice may not be removed or altered from any source distribution.

import urwid
import mpris2
import argparse

app_desc = 'TUI MPRIS2 Control'
__version__ = '1.0.1'

def decimal_to_time(secs):
    m, s = divmod(secs, 60)
    return '{:d}:{:02d}'.format(int(m), int(s))

class TUIPlayer(object):

    KEY_PAUSE = ' '
    KEY_NEXT = 'n'
    KEY_PREV = 'p'
    KEY_STOP = 's'
    KEY_QUIT = 'q'

    def __init__(self, player_str):

        global app_desc
        global __version__

        player_uri = None
        player_uris = list(mpris2.get_players_uri())
        for uri in player_uris:
            if player_str in uri:
                player_uri = uri
                break
        if not player_uri:
            print('Available Player URIs:')
            for uri in player_uris:
                print(' - {}'.format(uri))
            raise RuntimeError('No dbus players matched "{}"'.format(player_str))

        self.player = mpris2.Player(dbus_interface_info={'dbus_uri': player_uri})
        self.status = '(unknown)'
        self.trackid = None
        self.cur_pos = 0
        self.length = 0
        self.title = 'n/a'
        self.artist = 'n/a'
        self.album = 'n/a'

        main_header = urwid.Text('{} v{}'.format(app_desc, __version__), wrap='clip')
        header_widget = urwid.Padding(urwid.AttrMap(main_header, 'main_header'))

        labels = urwid.Pile([])
        values = urwid.Pile([])

        max_len = 0
        self.status_text = urwid.Text('', wrap='clip')
        self.status_attr = None
        self.artist_text = urwid.Text('', wrap='clip')
        self.album_text = urwid.Text('', wrap='clip')
        self.song_text = urwid.Text('', wrap='clip')
        self.position_text = urwid.Text('', wrap='clip')
        for label, val, is_status in [
                ('Connected to:', urwid.Text(player_uri, wrap='clip'), False),
                ('Status:', self.status_text, True),
                ('', urwid.Text(''), False),
                ('Album:', self.album_text, False),
                ('Artist:', self.artist_text, False),
                ('Song:', self.song_text, False),
                ('Position:', self.position_text, False),
                ]:
            if len(label) > max_len:
                max_len = len(label)
            attr_map = urwid.AttrMap(val, 'value')
            if is_status:
                self.status_attr = attr_map
            labels.contents.append((urwid.AttrMap(urwid.Text(label, align='right'), 'label'), ('pack', None)))
            values.contents.append((attr_map, ('pack', None)))

        cols = urwid.Columns([(max_len, labels), values], dividechars=1)
        main_padding = urwid.Padding(cols, left=3, right=3)
        main_filler = urwid.Filler(main_padding, top=1, bottom=1)
        main_pile = urwid.Pile([])
        main_pile.contents.append((main_filler, ('weight', 1)))
        keys = []
        for key, label in [
                (TUIPlayer.KEY_PAUSE, 'play/pause'),
                (TUIPlayer.KEY_NEXT, 'next'),
                (TUIPlayer.KEY_PREV, 'previous'),
                (TUIPlayer.KEY_STOP, 'stop'),
                (TUIPlayer.KEY_QUIT, 'quit'),
                ]:
            keys.append('[{}] {}'.format(key, label))
        main_pile.contents.append((
            urwid.AttrMap(urwid.Text(', '.join(keys), wrap='clip'), 'keys'),
            ('pack', None)))
        main_box = urwid.LineBox(main_pile)
        main_frame = urwid.Frame(main_box, header_widget)

        palette = [
                ('main_header', 'white', 'dark blue'),
                ('label', 'yellow', 'black'),
                ('value', 'white', 'black'),
                ('keys', 'light green', 'black'),
                ('stopped', 'light red', 'black'),
                ('paused', 'light blue', 'black'),
                ('playing', 'light green', 'black'),
                (None, 'white', 'black')
                ]

        self.loop = urwid.MainLoop(main_frame,
                palette=palette,
                input_filter=self.input_filter,
                )

    def start(self):
        self.update_status()
        self.loop.run()

    def exit_main_loop(self):
        raise urwid.ExitMainLoop()

    def input_filter(self, keys, raw):
        for key in keys:
            if type(key) != str:
                # This guards against mouse clicks
                continue
            key = key.lower()
            if key == TUIPlayer.KEY_QUIT:
                self.exit_main_loop()
            elif key == TUIPlayer.KEY_PAUSE:
                self.player.PlayPause()
            elif key == TUIPlayer.KEY_STOP:
                self.player.Stop()
            elif key == TUIPlayer.KEY_NEXT:
                self.player.Next()
            elif key == TUIPlayer.KEY_PREV:
                self.player.Previous()
        return []

    def update_status(self):

        self.status = self.player.PlaybackStatus
        data = self.player.Metadata
        self.trackid = data['mpris:trackid']
        if self.status == 'Stopped':
            self.cur_pos = 0
            self.title = 'n/a'
            self.artist = 'n/a'
            self.album = 'n/a'
            self.length = 0
        else:
            self.cur_pos = self.player.Position/1000000
            self.title = data['xesam:title']
            self.artist = data['xesam:artist'][0]
            self.album = data['xesam:album']
            self.url = data['xesam:url']
            self.length = data['mpris:length']/1000000

        self.status_text.set_text(self.status)
        self.artist_text.set_text(self.artist)
        self.album_text.set_text(self.album)
        self.song_text.set_text(self.title)
        self.position_text.set_text('{} / {}'.format(
            decimal_to_time(self.cur_pos),
            decimal_to_time(self.length),
            ))

        if self.status == 'Stopped':
            self.status_attr.set_attr_map({None: 'stopped'})
        elif self.status == 'Paused':
            self.status_attr.set_attr_map({None: 'paused'})
        else:
            self.status_attr.set_attr_map({None: 'playing'})

        # Call back to ourselves
        self.loop.event_loop.alarm(1, self.update_status)

def main():

    parser = argparse.ArgumentParser(
            description='Control MPRIS2 clients using a simple TUI',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )

    parser.add_argument('-p', '--player',
            type=str,
            default='audacious',
            help='Player string to match on in D-BUS',
            )

    args = parser.parse_args()

    p = TUIPlayer(args.player)
    p.start()

if __name__ == '__main__':

    main()

