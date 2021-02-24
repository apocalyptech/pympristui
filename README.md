# pympristui (TUI MPRIS2 Control)

This is a tiny little Python script to act as a TUI (Terminal User Interface)
to an [MPRIS2](https://specifications.freedesktop.org/mpris-spec/latest/)-enabled
media player.  MPRIS is a [D-Bus](https://dbus.freedesktop.org/doc/dbus-specification.html)-based
interface which many Linux-based media players support, which allows external
applications to control some aspects of media playback and control.  This is
most often used to provide little audio applets for desktop environments, or
to allow web-based control of a media player.  This app is intended to provide
some basic controls when (for instance) SSHed in to a machine that's running
an MPRIS-compatible media player.

This app has been tested in Python 3.9+, and requires:
* [dbus-python](https://pypi.org/project/dbus-python/) (tested on 1.2.16)
* [mpris2](https://pypi.org/project/mpris2/) (tested on 1.0.2)
* [urwid](https://pypi.org/project/urwid/) (tested on 2.1.2)

It attempts to connect to the [Audacious](https://audacious-media-player.org/)
Media Player by default; to connect to another app instead, you'll have to specify
a commandline arg.

# Installation

I'd recommend using a [virtual environment](https://docs.python.org/3/library/venv.html)
to run the app.  Change to a directory where you want to store your venv,
and create/activate it with:

    $ python -m venv mpris2
    $ . mpris2/bin/activate

You should have an `(mpris2)` prefix on your shell prompt to indicate the
venv is active.  Obviously feel free to name it whatever you like.

### pip Installation

At this point, you can just install using:

    $ pip install pympristui

A `pympristui.py` script should now be available on your `$PATH`.

### Manual Installation

Otherwise, check out the project from git, or download and uncompress an
archive from github.  Then, switch over to this project's dir and install
dependencies, either through:

    $ pip install -r requirements.txt

or by hand:

    $ pip install dbus-python mpris2 urwid

Then run it direct from the CLI (or copy the script anywhere you like):

    $ ./pympristui.py

# Usage

It's a very basic app.  By default it tries to find an MPRIS interface for
the media player Audacious.  If that's not found (or if that's not what you
want to use), you can use the `-p`/`--program` arg to specify another string
to search for.  The string matching here is extremely basic; it'll just pick
the first advertised interface name which matches the string you specify.  If
the specified string isn't found (or if Audacious isn't running, when no `-p`
has been specified), you'll get a list of all available MPRIS interfaces found
on your system, on the commandline, with output like:

    Available Player URIs:
     - org.mpris.MediaPlayer2.firefox.instance319681
     - org.mpris.MediaPlayer2.audacious

To use that `-p`/`--program` argument to connect to that Firefox instance, for
instance:

    $ ./pympristui.py -p firefox
    $ ./pympristui.py --program firefox

Using `instance319681` or even `319681` would also match that Firefox instance.

Once it's started, the app just provides the simple controls pause/play/stop,
next track, and previous track, along with the basic information about what's
being played currently:

![App Screenshot](https://raw.githubusercontent.com/apocalyptech/pympristui/master/screenshot.png)

It only accepts keyboard input, with the following keybinds:

* `space` - play/pause
* `n` - next track
* `p` - previous track
* `s` - stop
* `q` - quit

Note that the "quit" key only quits the control app itself; the actual app
playing audio will continue to run as usual.

# Limitations/TODO

* I'd originally intended to provide support for MPRIS2's
  [TrackList](https://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html)
  interface, but it turns out the Audacious [doesn't provide that](https://redmine.audacious-media-player.org/issues/106),
  so I didn't look into it any further.  As such, control in the app is limited
  to play/pause/stop, next, and prev.  There's no tracklist visibility, or ability
  to hop around with any control other than next/prev.
* I didn't implement in-track seeking or volume control.

# License

All code in this project is licensed under the
[zlib/libpng license](https://opensource.org/licenses/Zlib).  A copy is
provided in [COPYING.txt](COPYING.txt).

# Changelog

**v1.0.0** - *(unreleased)*
 - Initial release

