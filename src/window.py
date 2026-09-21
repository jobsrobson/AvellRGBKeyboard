import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk

from pages.keyboard_page import KeyboardPage
from pages.lightbar_page import LightbarPage
from pages.profiles_page import ProfilesPage


class AvellRGBWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("Avell RGB Control")
        self.set_size_request(950, 750)

        self._install_css()
        self._build_ui()

    def _install_css(self):
        provider = Gtk.CssProvider()

        provider.load_from_string("""
            .page {
                padding: 32px;
            }

            .hero-title {
                font-size: 26px;
                font-weight: 700;
            }

            .hero-subtitle {
                opacity: .65;
            }

            .keyboard-shell {
                background: #17191d;
                border-radius: 18px;
                padding: 22px;
            }

            .keyboard-key {
                min-width: 0;
                min-height: 48px;
                padding: 0;

                color: #e8eaed;
                background: #292c31;

                border: 1px solid #383c42;
                border-radius: 7px;

                box-shadow:
                    inset 0 1px rgba(255,255,255,.04),
                    0 1px 2px rgba(0,0,0,.30);
            }

            .keyboard-key:hover {
                background: #32363c;
            }

            .keyboard-key:checked {
                background: #343a43;
                border-color: @accent_color;

                box-shadow:
                    inset 0 0 0 1px @accent_color;
            }

            .key-label {
                font-size: 11px;
                font-weight: 600;
            }

            .rgb-indicator {
                min-height: 4px;
                border-radius: 999px;
            }

            .toolbar-panel {
                padding: 14px 16px;
                margin-top: 18px;

                border-radius: 14px;

                background:
                    alpha(@card_bg_color, .8);

                border:
                    1px solid alpha(@borders, .65);
            }

            .selection-count {
                font-weight: 600;
            }

            .muted {
                opacity: .6;
            }

            .lightbar-card {
                padding: 24px;

                border-radius: 18px;

                background:
                    alpha(@card_bg_color, .8);

                border:
                    1px solid alpha(@borders, .65);
            }

            .lightbar-preview-shell {
                padding: 26px 18px;

                border-radius: 14px;

                background: #17191d;
            }

            .lightbar-preview {
                min-height: 12px;
                border-radius: 999px;
            }

            .brightness-panel {
                padding: 10px 16px;

                border-radius: 12px;

                background:
                    alpha(@card_bg_color, .55);

                border:
                    1px solid alpha(@borders, .45);
            }

            .brightness-label {
                font-weight: 600;
            }

            .brightness-value {
                font-weight: 600;
                font-variant-numeric: tabular-nums;
            }

            .brightness-panel scale {
                min-width: 240px;
            }
        """)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _build_ui(self):
        toolbar = Adw.ToolbarView()

        header = Adw.HeaderBar()

        self.stack = Adw.ViewStack()

        switcher = Adw.ViewSwitcher()
        switcher.set_stack(self.stack)
        switcher.set_policy(
            Adw.ViewSwitcherPolicy.WIDE
        )

        header.set_title_widget(
            switcher
        )

        toolbar.add_top_bar(
            header
        )

        self.keyboard_page = KeyboardPage()
        self.lightbar_page = LightbarPage()

        self.profiles_page = ProfilesPage(
            self.keyboard_page,
            self.lightbar_page,
        )

        keyboard_scroll = Gtk.ScrolledWindow()
        keyboard_scroll.set_child(
            self.keyboard_page
        )

        lightbar_scroll = Gtk.ScrolledWindow()
        lightbar_scroll.set_child(
            self.lightbar_page
        )

        profiles_scroll = Gtk.ScrolledWindow()
        profiles_scroll.set_child(
            self.profiles_page
        )

        self.stack.add_titled_with_icon(
            keyboard_scroll,
            "keyboard",
            "Teclado",
            "input-keyboard-symbolic",
        )

        self.stack.add_titled_with_icon(
            lightbar_scroll,
            "lightbar",
            "Lightbar",
            "display-brightness-symbolic",
        )

        self.stack.add_titled_with_icon(
            profiles_scroll,
            "profiles",
            "Perfis",
            "document-save-symbolic",
        )

        toolbar.set_content(
            self.stack
        )

        self.set_content(
            toolbar
        )