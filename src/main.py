import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw
from window import AvellRGBWindow


APP_ID = "io.github.jobsr.AvellRGBControl"
APP_NAME = "Avell RGB Control"
APP_VERSION = "0.1.0"


class AvellRGBApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=APP_ID
        )

    def do_activate(self):
        window = self.props.active_window

        if window is None:
            window = AvellRGBWindow(
                application=self
            )

        window.present()


def main():
    app = AvellRGBApplication()

    return app.run(
        sys.argv
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )