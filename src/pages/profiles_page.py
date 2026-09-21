import json
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

from profiles import ProfileManager


class ProfilesPage(Gtk.Box):
    def __init__(
        self,
        keyboard_page,
        lightbar_page,
    ):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        self.keyboard_page = keyboard_page
        self.lightbar_page = lightbar_page
        self.manager = ProfileManager()

        self.add_css_class("page")

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        title = Gtk.Label(
            label="Perfis"
        )
        title.set_xalign(0)
        title.add_css_class("hero-title")

        subtitle = Gtk.Label(
            label=(
                "Salve e restaure toda a iluminação "
                "do notebook com um clique."
            )
        )
        subtitle.set_xalign(0)
        subtitle.add_css_class("hero-subtitle")

        self.append(title)
        self.append(subtitle)

        save_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
        )
        save_box.set_margin_top(22)
        save_box.add_css_class("toolbar-panel")

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text(
            "Nome do perfil"
        )
        self.name_entry.set_hexpand(True)

        save_box.append(
            self.name_entry
        )

        save_button = Gtk.Button(
            label="Salvar estado atual"
        )
        save_button.add_css_class(
            "suggested-action"
        )
        save_button.connect(
            "clicked",
            self._save,
        )

        save_box.append(save_button)
        self.append(save_box)

        self.list_box = Gtk.ListBox()
        self.list_box.add_css_class(
            "boxed-list"
        )
        self.list_box.set_margin_top(18)

        self.append(self.list_box)

    def refresh(self):
        child = self.list_box.get_first_child()

        while child:
            next_child = child.get_next_sibling()
            self.list_box.remove(child)
            child = next_child

        profiles = self.manager.list_profiles()

        if not profiles:
            row = Adw.ActionRow(
                title="Nenhum perfil salvo",
                subtitle=(
                    "Configure o teclado e a Lightbar "
                    "e salve o primeiro perfil."
                ),
            )

            row.set_sensitive(False)
            self.list_box.append(row)
            return

        for path, data in profiles:
            row = Adw.ActionRow(
                title=data.get(
                    "name",
                    path.stem,
                ),
                subtitle="Teclado + Lightbar",
            )

            apply_button = Gtk.Button(
                label="Aplicar"
            )
            apply_button.set_valign(
                Gtk.Align.CENTER
            )
            apply_button.add_css_class(
                "suggested-action"
            )
            apply_button.connect(
                "clicked",
                self._apply,
                path,
            )

            delete_button = Gtk.Button(
                icon_name="user-trash-symbolic"
            )
            delete_button.set_valign(
                Gtk.Align.CENTER
            )
            delete_button.add_css_class(
                "flat"
            )
            delete_button.connect(
                "clicked",
                self._delete,
                path,
            )

            row.add_suffix(apply_button)
            row.add_suffix(delete_button)

            self.list_box.append(row)

    def _save(self, _button):
        name = self.name_entry.get_text().strip()

        if not name:
            return

        keyboard = self.keyboard_page.get_state()
        lightbar = self.lightbar_page.get_state()

        self.manager.save(
            name,
            keyboard,
            lightbar,
        )

        self.name_entry.set_text("")
        self.refresh()

    def _apply(self, _button, path):
        try:
            data = json.loads(
                path.read_text()
            )

            self.keyboard_page.apply_state(
                data["keyboard"]
            )

            self.lightbar_page.apply_state(
                data["lightbar"]
            )

        except Exception as exc:
            print(
                f"Erro aplicando perfil: {exc}"
            )

    def _delete(self, _button, path):
        self.manager.delete(path)
        self.refresh()