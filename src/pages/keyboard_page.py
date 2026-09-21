import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk, GLib

from hardware import AvellKeyboard
from keyboard import KEYS


KEY_LAYOUT = [
    # Function row
    ("Esc", "Esc", 0, 0, 4, 4),
    ("F1", "F1", 4, 0, 4, 4),
    ("F2", "F2", 8, 0, 4, 4),
    ("F3", "F3", 12, 0, 4, 4),
    ("F4", "F4", 16, 0, 4, 4),
    ("F5", "F5", 20, 0, 4, 4),
    ("F6", "F6", 24, 0, 4, 4),
    ("F7", "F7", 28, 0, 4, 4),
    ("F8", "F8", 32, 0, 4, 4),
    ("F9", "F9", 36, 0, 4, 4),
    ("F10", "F10", 40, 0, 4, 4),
    ("F11", "F11", 44, 0, 4, 4),
    ("F12", "F12", 48, 0, 4, 4),
    ("Insert", "Ins", 52, 0, 4, 4),
    ("PrtSc", "PrtSc", 56, 0, 4, 4),
    ("Delete", "Del", 60, 0, 4, 4),

    # Number row
    ("Quote", "'", 0, 4, 4, 4),
    ("1", "1", 4, 4, 4, 4),
    ("2", "2", 8, 4, 4, 4),
    ("3", "3", 12, 4, 4, 4),
    ("4", "4", 16, 4, 4, 4),
    ("5", "5", 20, 4, 4, 4),
    ("6", "6", 24, 4, 4, 4),
    ("7", "7", 28, 4, 4, 4),
    ("8", "8", 32, 4, 4, 4),
    ("9", "9", 36, 4, 4, 4),
    ("0", "0", 40, 4, 4, 4),
    ("Minus", "-", 44, 4, 4, 4),
    ("Equal", "=", 48, 4, 4, 4),
    ("Pause", "Pause", 52, 4, 4, 4),
    ("Backspace", "←", 56, 4, 4, 4),
    ("Home", "Home", 60, 4, 4, 4),

    # Q row
    ("Tab", "Tab", 0, 8, 6, 4),
    ("Q", "Q", 6, 8, 4, 4),
    ("W", "W", 10, 8, 4, 4),
    ("E", "E", 14, 8, 4, 4),
    ("R", "R", 18, 8, 4, 4),
    ("T", "T", 22, 8, 4, 4),
    ("Y", "Y", 26, 8, 4, 4),
    ("U", "U", 30, 8, 4, 4),
    ("I", "I", 34, 8, 4, 4),
    ("O", "O", 38, 8, 4, 4),
    ("P", "P", 42, 8, 4, 4),
    ("Grave", "`", 46, 8, 4, 4),
    ("BracketLeft", "[", 50, 8, 4, 4),

    # Enter vertical
    ("Enter", "↵", 54, 8, 6, 8),
    ("PgUp", "PgUp", 60, 8, 4, 4),

    # A row
    ("CapsLock", "Caps", 0, 12, 7, 4),
    ("A", "A", 7, 12, 4, 4),
    ("S", "S", 11, 12, 4, 4),
    ("D", "D", 15, 12, 4, 4),
    ("F", "F", 19, 12, 4, 4),
    ("G", "G", 23, 12, 4, 4),
    ("H", "H", 27, 12, 4, 4),
    ("J", "J", 31, 12, 4, 4),
    ("K", "K", 35, 12, 4, 4),
    ("L", "L", 39, 12, 4, 4),
    ("Cedilla", "Ç", 43, 12, 4, 4),
    ("Tilde", "~", 47, 12, 4, 4),
    ("BracketRight", "]", 51, 12, 3, 4),
    ("PgDn", "PgDn", 60, 12, 4, 4),

    # Z row — calibrada para o teclado físico
    ("Shift_L", "Shift", 0, 16, 4, 4),
    ("Backslash", "\\ |", 4, 16, 4, 4),
    ("Z", "Z", 8, 16, 4, 4),
    ("X", "X", 12, 16, 4, 4),
    ("C", "C", 16, 16, 4, 4),
    ("V", "V", 20, 16, 4, 4),
    ("B", "B", 24, 16, 4, 4),
    ("N", "N", 28, 16, 4, 4),
    ("M", "M", 32, 16, 4, 4),
    ("Comma", "<", 36, 16, 4, 4),
    ("Period", ">", 40, 16, 4, 4),
    ("Semicolon", ";", 44, 16, 4, 4),
    ("Slash", "/ ?", 48, 16, 4, 4),
    ("Shift_R", "Shift", 52, 16, 4, 4),
    ("Up", "↑", 56, 16, 4, 4),
    ("End", "End", 60, 16, 4, 4),

    # Bottom row
    ("Ctrl_L", "Ctrl", 0, 20, 5, 4),
    ("Fn", "Fn", 5, 20, 4, 4),
    ("Super", "◆", 9, 20, 4, 4),
    ("Alt", "Alt", 13, 20, 4, 4),
    ("Space", "", 17, 20, 20, 4),
    ("AltGr", "AltGr", 37, 20, 5, 4),
    ("Menu", "Menu", 42, 20, 4, 4),
    ("Ctrl_R", "Ctrl", 46, 20, 6, 4),
    ("Left", "←", 52, 20, 4, 4),
    ("Down", "↓", 56, 20, 4, 4),
    ("Right", "→", 60, 20, 4, 4),
]


class KeyboardKey(Gtk.ToggleButton):
    CELL = 12

    def __init__(self, key_name, label, width, height):
        super().__init__()

        self.key_name = key_name
        self.channel = KEYS[key_name].channel
        self.rgb = (0, 0, 0)
        self._rgb_provider = None

        self.set_can_focus(False)
        self.add_css_class("keyboard-key")
        self.set_size_request(width * self.CELL, 48)

        overlay = Gtk.Overlay()

        label_widget = Gtk.Label(label=label)
        label_widget.add_css_class("key-label")
        overlay.set_child(label_widget)

        self.indicator = Gtk.Box()
        self.indicator.set_halign(Gtk.Align.FILL)
        self.indicator.set_valign(Gtk.Align.END)
        self.indicator.set_size_request(-1, 4)
        self.indicator.set_margin_start(7)
        self.indicator.set_margin_end(7)
        self.indicator.set_margin_bottom(6)
        self.indicator.add_css_class("rgb-indicator")

        overlay.add_overlay(self.indicator)
        self.set_child(overlay)

    def set_rgb_preview(self, rgb):
        self.rgb = tuple(rgb)

        r, g, b = rgb

        provider = Gtk.CssProvider()
        provider.load_from_string(
            f"""
            box {{
                background-color: rgb({r}, {g}, {b});
            }}
            """
        )

        if self._rgb_provider is not None:
            self.indicator.get_style_context().remove_provider(
                self._rgb_provider
            )

        self.indicator.get_style_context().add_provider(
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._rgb_provider = provider


class KeyboardPage(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        self.kbd = AvellKeyboard()
        self.key_buttons = {}

        self.add_css_class("page")

        self._loading_brightness = False

        self._build_ui()
        GLib.idle_add(self.refresh)

    def _build_ui(self):
        title = Gtk.Label(label="Iluminação do teclado")
        title.set_xalign(0)
        title.add_css_class("hero-title")

        subtitle = Gtk.Label(
            label="Personalize individualmente a iluminação de cada tecla."
        )
        subtitle.set_xalign(0)
        subtitle.add_css_class("hero-subtitle")

        self.append(title)
        self.append(subtitle)

        shell = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )
        shell.set_margin_top(22)
        shell.add_css_class("keyboard-shell")

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(1)
        grid.set_halign(Gtk.Align.CENTER)

        for name, label, col, row, width, height in KEY_LAYOUT:
            button = KeyboardKey(
                name,
                label,
                width,
                height,
            )

            button.connect(
                "toggled",
                self._selection_changed,
            )

            self.key_buttons[name] = button

            grid.attach(
                button,
                col,
                row,
                width,
                height,
            )

        shell.append(grid)
        self.append(shell)

        # =====================================================
        # Brilho
        # =====================================================

        brightness_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )

        brightness_box.add_css_class(
            "brightness-panel"
        )

        brightness_box.set_margin_top(14)

        brightness_label = Gtk.Label(
            label="Brilho"
        )

        brightness_label.add_css_class(
            "brightness-label"
        )

        brightness_box.append(
            brightness_label
        )

        brightness_icon = Gtk.Image.new_from_icon_name(
            "display-brightness-symbolic"
        )

        brightness_icon.add_css_class(
            "dim-label"
        )

        brightness_box.append(
            brightness_icon
        )

        self.brightness_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0,
            100,
            1,
        )

        self.brightness_scale.set_hexpand(
            True
        )

        self.brightness_scale.set_draw_value(
            False
        )

        self.brightness_scale.set_round_digits(
            0
        )

        self.brightness_scale.connect(
            "value-changed",
            self._brightness_changed,
        )

        brightness_box.append(
            self.brightness_scale
        )

        self.brightness_value_label = Gtk.Label(
            label="100%"
        )

        self.brightness_value_label.set_width_chars(
            4
        )

        self.brightness_value_label.set_xalign(
            1
        )

        self.brightness_value_label.add_css_class(
            "brightness-value"
        )

        brightness_box.append(
            self.brightness_value_label
        )

        self.append(
            brightness_box
        )

        controls = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
        )
        controls.add_css_class("toolbar-panel")

        self.selection_label = Gtk.Label(
            label="Nenhuma tecla selecionada"
        )
        self.selection_label.add_css_class(
            "selection-count"
        )
        controls.append(self.selection_label)

        color_label = Gtk.Label(label="Cor")
        color_label.add_css_class("muted")
        color_label.set_margin_start(12)
        controls.append(color_label)

        self.color_button = Gtk.ColorDialogButton(
            dialog=Gtk.ColorDialog(
                title="Escolher cor"
            )
        )

        default = Gdk.RGBA()
        default.parse("#00de97")
        self.color_button.set_rgba(default)

        controls.append(self.color_button)

        select_all = Gtk.Button(
            label="Selecionar tudo"
        )
        select_all.connect(
            "clicked",
            self._select_all,
        )
        controls.append(select_all)

        clear = Gtk.Button(label="Limpar")
        clear.connect(
            "clicked",
            self._clear_selection,
        )
        controls.append(clear)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        controls.append(spacer)

        self.apply_button = Gtk.Button(
            label="Aplicar cor"
        )
        self.apply_button.add_css_class(
            "suggested-action"
        )
        self.apply_button.set_sensitive(False)
        self.apply_button.connect(
            "clicked",
            self._apply,
        )

        controls.append(self.apply_button)
        self.append(controls)

    def refresh(self):
        # RGB das teclas
        for button in self.key_buttons.values():
            try:
                button.set_rgb_preview(
                    self.kbd.get_rgb(
                        button.channel
                    )
                )

            except Exception as exc:
                print(
                    f"Erro lendo "
                    f"{button.key_name}: {exc}"
                )

        # Brilho global
        try:
            self._loading_brightness = True

            percent = (
                self.kbd
                .get_brightness_percent()
            )

            self.brightness_scale.set_value(
                percent
            )

            self.brightness_value_label.set_text(
                f"{percent}%"
            )

        except Exception as exc:
            print(
                f"Erro lendo brilho: {exc}"
            )

        finally:
            self._loading_brightness = False

        return False

    def _brightness_changed(
        self,
        scale,
    ):
        percent = round(
            scale.get_value()
        )

        self.brightness_value_label.set_text(
            f"{percent}%"
        )

        if self._loading_brightness:
            return

        try:
            self.kbd.set_brightness_percent(
                percent
            )

        except Exception as exc:
            print(
                f"Erro alterando brilho: {exc}"
            )

    def get_state(self):
        keys = {
            str(button.channel): list(
                self.kbd.get_rgb(
                    button.channel
                )
            )
            for button
            in self.key_buttons.values()
        }

        return {
            "brightness":
                self.kbd.get_brightness(),

            "keys":
                keys,
        }

    def apply_state(
        self,
        state,
    ):
        # Compatibilidade com os perfis antigos.
        #
        # Antigo:
        # {
        #   "0": [...],
        #   "2": [...]
        # }
        #
        # Novo:
        # {
        #   "brightness": 50,
        #   "keys": {
        #       "0": [...],
        #       ...
        #   }
        # }

        if "keys" in state:
            keys = state["keys"]

            brightness = state.get(
                "brightness"
            )

        else:
            keys = state
            brightness = None

        with self.kbd.batch():
            for channel, rgb in keys.items():
                self.kbd.set_rgb(
                    int(channel),
                    *rgb,
                )

        if brightness is not None:
            self.kbd.set_brightness(
                int(brightness)
            )

        self.refresh()

    def _selected(self):
        return [
            button
            for button in self.key_buttons.values()
            if button.get_active()
        ]

    def _selection_changed(self, _button):
        count = len(self._selected())

        if count == 0:
            text = "Nenhuma tecla selecionada"
        elif count == 1:
            text = "1 tecla selecionada"
        else:
            text = f"{count} teclas selecionadas"

        self.selection_label.set_text(text)
        self.apply_button.set_sensitive(count > 0)

    def _select_all(self, _button):
        for button in self.key_buttons.values():
            button.set_active(True)

    def _clear_selection(self, _button):
        for button in self.key_buttons.values():
            button.set_active(False)

    def _apply(self, _button):
        rgba = self.color_button.get_rgba()

        rgb = (
            round(rgba.red * 255),
            round(rgba.green * 255),
            round(rgba.blue * 255),
        )

        selected = self._selected()

        if not selected:
            return

        with self.kbd.batch():
            for button in selected:
                self.kbd.set_rgb(
                    button.channel,
                    *rgb,
                )

        for button in selected:
            button.set_rgb_preview(rgb)