import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gdk, GLib

from lightbar import Lightbar


class LightbarPage(Gtk.Box):
    # ~60 FPS
    ANIMATION_INTERVAL = 16

    # Aproximadamente 4,8 segundos para:
    # RED -> YELLOW -> GREEN -> RED
    ANIMATION_STEP = 0.0035

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        self.lightbar = Lightbar()

        # Última cor estática escolhida.
        # Usada também para restaurar a Lightbar após desligar/ligar.
        self.last_rgb = (0, 255, 0)

        self._preview_provider = None
        self._animation_source = None
        self._animation_phase = 0.0

        # Impede que alterações programáticas feitas em refresh()
        # disparem escrita no hardware.
        self._refreshing = False

        self.add_css_class("page")

        self._build_ui()
        self.refresh()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):
        title = Gtk.Label(
            label="Lightbar"
        )
        title.set_xalign(0)
        title.add_css_class("hero-title")

        subtitle = Gtk.Label(
            label="Controle a iluminação frontal do notebook."
        )
        subtitle.set_xalign(0)
        subtitle.add_css_class("hero-subtitle")

        self.append(title)
        self.append(subtitle)

        # -----------------------------------------------------
        # Card principal
        # -----------------------------------------------------

        card = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
        )

        card.add_css_class("lightbar-card")
        card.set_margin_top(22)

        # -----------------------------------------------------
        # Preview
        # -----------------------------------------------------

        preview_shell = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )

        preview_shell.add_css_class(
            "lightbar-preview-shell"
        )

        self.preview = Gtk.Box()

        self.preview.set_hexpand(True)
        self.preview.set_size_request(
            -1,
            16,
        )

        self.preview.add_css_class(
            "lightbar-preview"
        )

        preview_shell.append(
            self.preview
        )

        card.append(
            preview_shell
        )

        # -----------------------------------------------------
        # Controles
        # -----------------------------------------------------

        controls = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=16,
        )

        controls.set_valign(
            Gtk.Align.CENTER
        )

        # Liga/desliga
        enabled_label = Gtk.Label(
            label="Lightbar"
        )

        self.enabled_switch = Gtk.Switch()

        self.enabled_switch.set_valign(
            Gtk.Align.CENTER
        )

        self.enabled_switch.connect(
            "notify::active",
            self._enabled_changed,
        )

        controls.append(
            enabled_label
        )

        controls.append(
            self.enabled_switch
        )

        # Separador
        separator = Gtk.Separator(
            orientation=Gtk.Orientation.VERTICAL
        )

        controls.append(
            separator
        )

        # Cor
        color_label = Gtk.Label(
            label="Cor"
        )

        controls.append(
            color_label
        )

        self.color_button = Gtk.ColorDialogButton(
            dialog=Gtk.ColorDialog(
                title="Cor da Lightbar"
            )
        )

        self.color_button.connect(
            "notify::rgba",
            self._color_changed,
        )

        controls.append(
            self.color_button
        )

        # Separador
        separator2 = Gtk.Separator(
            orientation=Gtk.Orientation.VERTICAL
        )

        controls.append(
            separator2
        )

        # Animação
        animation_label = Gtk.Label(
            label="Animação"
        )

        controls.append(
            animation_label
        )

        self.animation_switch = Gtk.Switch()

        self.animation_switch.set_valign(
            Gtk.Align.CENTER
        )

        self.animation_switch.connect(
            "notify::active",
            self._animation_changed,
        )

        controls.append(
            self.animation_switch
        )

        card.append(
            controls
        )

        self.append(
            card
        )

    # =========================================================
    # ESTADO DO HARDWARE
    # =========================================================

    def refresh(self):
        """
        Sincroniza a GUI com o estado atual do hardware.
        """

        self._refreshing = True

        try:
            rgb = self.lightbar.get_rgb()

            enabled = self.lightbar.is_on()

            animation = (
                self.lightbar.get_animation()
            )

            if any(rgb):
                self.last_rgb = rgb

            # Atualiza ColorDialogButton
            rgba = Gdk.RGBA()

            rgba.red = (
                self.last_rgb[0] / 255
            )

            rgba.green = (
                self.last_rgb[1] / 255
            )

            rgba.blue = (
                self.last_rgb[2] / 255
            )

            rgba.alpha = 1.0

            self.color_button.set_rgba(
                rgba
            )

            # Atualiza switches
            self.enabled_switch.set_active(
                enabled
            )

            self.animation_switch.set_active(
                animation
            )

        finally:
            self._refreshing = False

        # Atualiza o preview depois de liberar os callbacks.
        if enabled and animation:
            self._start_preview_animation()

        elif enabled:
            self._stop_preview_animation(
                redraw=False
            )

            self._draw_static_preview(
                rgb
            )

        else:
            self._stop_preview_animation(
                redraw=False
            )

            self._draw_off_preview()

    # =========================================================
    # CSS DO PREVIEW
    # =========================================================

    def _apply_preview_css(
        self,
        css,
    ):
        """
        Troca somente o CSS do preview da Lightbar.
        """

        provider = Gtk.CssProvider()

        try:
            provider.load_from_string(
                css
            )

        except Exception as exc:
            print(
                f"Erro no CSS da Lightbar: {exc}"
            )
            return

        context = (
            self.preview.get_style_context()
        )

        if (
            self._preview_provider
            is not None
        ):
            context.remove_provider(
                self._preview_provider
            )

        context.add_provider(
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._preview_provider = (
            provider
        )

    # =========================================================
    # PREVIEW DESLIGADO
    # =========================================================

    def _draw_off_preview(self):
        """
        Aparência da Lightbar desligada.
        """

        css = """
        box {
            background-image:
                linear-gradient(
                    to bottom,
                    #272a2f 0%,
                    #181a1e 45%,
                    #111316 100%
                );

            border-radius: 999px;

            box-shadow:
                inset 0 1px
                rgba(255, 255, 255, 0.05);
        }
        """

        self._apply_preview_css(
            css
        )

    # =========================================================
    # PREVIEW ESTÁTICO
    # =========================================================

    def _draw_static_preview(
        self,
        rgb,
    ):
        """
        Desenha uma Lightbar estática simulando
        o difusor físico.
        """

        r, g, b = rgb

        # Centro ligeiramente mais claro.
        bright_r = min(
            255,
            round(r * 1.18),
        )

        bright_g = min(
            255,
            round(g * 1.18),
        )

        bright_b = min(
            255,
            round(b * 1.18),
        )

        css = f"""
        box {{
            background-image:

                linear-gradient(
                    to bottom,

                    rgba(
                        255,
                        255,
                        255,
                        0.34
                    ) 0%,

                    rgba(
                        255,
                        255,
                        255,
                        0.12
                    ) 22%,

                    rgba(
                        255,
                        255,
                        255,
                        0.02
                    ) 48%,

                    rgba(
                        0,
                        0,
                        0,
                        0.08
                    ) 78%,

                    rgba(
                        0,
                        0,
                        0,
                        0.16
                    ) 100%
                ),

                linear-gradient(
                    90deg,

                    rgb(
                        {r},
                        {g},
                        {b}
                    ) 0%,

                    rgb(
                        {bright_r},
                        {bright_g},
                        {bright_b}
                    ) 50%,

                    rgb(
                        {r},
                        {g},
                        {b}
                    ) 100%
                );

            border-radius: 999px;

            box-shadow:
                0 0 7px
                rgba(
                    {r},
                    {g},
                    {b},
                    0.55
                ),

                0 0 18px
                rgba(
                    {r},
                    {g},
                    {b},
                    0.22
                );
        }}
        """

        self._apply_preview_css(
            css
        )

    # =========================================================
    # ANIMAÇÃO
    # =========================================================

    @staticmethod
    def _mix_color(
        color_a,
        color_b,
        amount,
    ):
        """
        Interpolação linear entre duas cores RGB.
        """

        amount = max(
            0.0,
            min(
                1.0,
                amount,
            ),
        )

        return tuple(
            round(
                color_a[i]
                + (
                    color_b[i]
                    - color_a[i]
                )
                * amount
            )
            for i in range(3)
        )

    def _animation_color(
        self,
        position,
    ):
        """
        Sequência temporal real da Lightbar:

            RED
             ↓ fade
            YELLOW
             ↓ fade
            GREEN
             ↓ fade
            RED
             ↓ ...

        A barra inteira possui a mesma cor.
        """

        RED = (
            255,
            0,
            0,
        )

        YELLOW = (
            255,
            215,
            0,
        )

        GREEN = (
            0,
            255,
            0,
        )

        position %= 1.0

        section = (
            position * 3.0
        )

        # RED -> YELLOW
        if section < 1.0:
            return self._mix_color(
                RED,
                YELLOW,
                section,
            )

        # YELLOW -> GREEN
        if section < 2.0:
            return self._mix_color(
                YELLOW,
                GREEN,
                section - 1.0,
            )

        # GREEN -> RED
        return self._mix_color(
            GREEN,
            RED,
            section - 2.0,
        )

    def _draw_animated_preview(
        self,
    ):
        """
        Desenha um único frame da animação.

        Importante:
        esta animação existe SOMENTE na GUI.

        Não fazemos escrita contínua no hardware.
        O hardware continua usando o modo nativo
        lightbar_animation.
        """

        r, g, b = (
            self._animation_color(
                self._animation_phase
            )
        )

        # Simula o centro mais luminoso
        # do difusor físico.
        bright_r = min(
            255,
            round(r * 1.18),
        )

        bright_g = min(
            255,
            round(g * 1.18),
        )

        bright_b = min(
            255,
            round(b * 1.18),
        )

        css = f"""
        box {{
            background-image:

                linear-gradient(
                    to bottom,

                    rgba(
                        255,
                        255,
                        255,
                        0.36
                    ) 0%,

                    rgba(
                        255,
                        255,
                        255,
                        0.13
                    ) 22%,

                    rgba(
                        255,
                        255,
                        255,
                        0.02
                    ) 48%,

                    rgba(
                        0,
                        0,
                        0,
                        0.08
                    ) 78%,

                    rgba(
                        0,
                        0,
                        0,
                        0.16
                    ) 100%
                ),

                linear-gradient(
                    90deg,

                    rgb(
                        {r},
                        {g},
                        {b}
                    ) 0%,

                    rgb(
                        {bright_r},
                        {bright_g},
                        {bright_b}
                    ) 50%,

                    rgb(
                        {r},
                        {g},
                        {b}
                    ) 100%
                );

            border-radius: 999px;

            box-shadow:

                0 0 7px
                rgba(
                    {r},
                    {g},
                    {b},
                    0.60
                ),

                0 0 18px
                rgba(
                    {r},
                    {g},
                    {b},
                    0.24
                );
        }}
        """

        self._apply_preview_css(
            css
        )

    def _animation_tick(
        self,
    ):
        """
        Chamado aproximadamente a cada 16 ms.
        """

        if (
            not self.animation_switch.get_active()
            or
            not self.enabled_switch.get_active()
        ):
            self._animation_source = None

            return GLib.SOURCE_REMOVE

        self._animation_phase += (
            self.ANIMATION_STEP
        )

        if (
            self._animation_phase
            >= 1.0
        ):
            self._animation_phase -= 1.0

        self._draw_animated_preview()

        return GLib.SOURCE_CONTINUE

    def _start_preview_animation(
        self,
    ):
        """
        Inicia a animação visual da GUI.
        """

        if (
            not self.enabled_switch.get_active()
        ):
            return

        if (
            self._animation_source
            is not None
        ):
            return

        # Renderiza imediatamente.
        self._draw_animated_preview()

        self._animation_source = (
            GLib.timeout_add(
                self.ANIMATION_INTERVAL,
                self._animation_tick,
            )
        )

    def _stop_preview_animation(
        self,
        redraw=True,
    ):
        """
        Interrompe o timer da animação.
        """

        if (
            self._animation_source
            is not None
        ):
            GLib.source_remove(
                self._animation_source
            )

            self._animation_source = None

        if not redraw:
            return

        if (
            self.enabled_switch.get_active()
        ):
            self._draw_static_preview(
                self.lightbar.get_rgb()
            )

        else:
            self._draw_off_preview()

    # =========================================================
    # EVENTOS
    # =========================================================

    def _enabled_changed(
        self,
        switch,
        _pspec,
    ):
        if self._refreshing:
            return

        enabled = (
            switch.get_active()
        )

        if enabled:
            # Restaura a última cor estática conhecida.
            self.lightbar.set_rgb(
                *self.last_rgb
            )

            if (
                self.animation_switch.get_active()
            ):
                self._start_preview_animation()

            else:
                self._draw_static_preview(
                    self.last_rgb
                )

        else:
            # Guarda a cor antes de zerar o hardware.
            current = (
                self.lightbar.get_rgb()
            )

            if any(current):
                self.last_rgb = current

            self.lightbar.turn_off()

            self._stop_preview_animation(
                redraw=False
            )

            self._draw_off_preview()

    def _color_changed(
        self,
        button,
        _pspec,
    ):
        if self._refreshing:
            return

        rgba = (
            button.get_rgba()
        )

        rgb = (
            round(
                rgba.red * 255
            ),

            round(
                rgba.green * 255
            ),

            round(
                rgba.blue * 255
            ),
        )

        self.last_rgb = rgb

        # Se estiver desligada, apenas lembramos a cor.
        if (
            not self.enabled_switch.get_active()
        ):
            return

        # Atualiza a cor-base do hardware.
        self.lightbar.set_rgb(
            *rgb
        )

        # Com animação ligada, o preview representa
        # a animação e não a cor estática escolhida.
        if (
            self.animation_switch.get_active()
        ):
            self._start_preview_animation()

        else:
            self._draw_static_preview(
                rgb
            )

    def _animation_changed(
        self,
        switch,
        _pspec,
    ):
        if self._refreshing:
            return

        enabled = (
            switch.get_active()
        )

        # Aqui ocorre a única escrita necessária
        # para ativar/desativar a animação nativa.
        self.lightbar.set_animation(
            enabled
        )

        if enabled:
            self._start_preview_animation()

        else:
            self._stop_preview_animation()

    # =========================================================
    # PERFIS
    # =========================================================

    def get_state(self):
        """
        Estado serializável para profiles.py.
        """

        rgb = (
            self.lightbar.get_rgb()
        )

        return {
            "enabled":
                self.lightbar.is_on(),

            "rgb":
                list(
                    rgb
                    if any(rgb)
                    else self.last_rgb
                ),

            "animation":
                self.lightbar.get_animation(),
        }

    def apply_state(
        self,
        state,
    ):
        """
        Restaura Lightbar a partir de um perfil.
        """

        rgb = tuple(
            state.get(
                "rgb",
                [
                    0,
                    255,
                    0,
                ],
            )
        )

        enabled = bool(
            state.get(
                "enabled",
                True,
            )
        )

        animation = bool(
            state.get(
                "animation",
                False,
            )
        )

        self.last_rgb = rgb

        # Configura o modo nativo.
        self.lightbar.set_animation(
            animation
        )

        # Restaura estado ligado/desligado.
        if enabled:
            self.lightbar.set_rgb(
                *rgb
            )

        else:
            self.lightbar.turn_off()

        # Sincroniza switches, picker e preview.
        self.refresh()