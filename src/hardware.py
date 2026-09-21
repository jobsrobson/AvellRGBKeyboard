from contextlib import contextmanager
from pathlib import Path


LED_ROOT = Path("/sys/class/leds")
HID_DRIVER = Path("/sys/bus/hid/drivers/ite_8291")


class AvellKeyboard:
    MAX_BRIGHTNESS = 50

    BRIGHTNESS_PATH = (
        LED_ROOT
        / "rgb:kbd_backlight"
        / "brightness"
    )

    def __init__(self):
        self.buffer_path = self._find_buffer()

        if not self.BRIGHTNESS_PATH.exists():
            raise RuntimeError(
                "Controle de brilho do teclado não encontrado: "
                f"{self.BRIGHTNESS_PATH}"
            )

    def _find_buffer(self) -> Path:
        if not HID_DRIVER.exists():
            raise RuntimeError(
                "Driver ite_8291 não encontrado."
            )

        for entry in HID_DRIVER.iterdir():
            if not entry.name.startswith(
                "0003:048D:CE00."
            ):
                continue

            candidate = (
                entry
                / "controls"
                / "buffer_input"
            )

            if candidate.exists():
                return candidate

        raise RuntimeError(
            "ITE 8291 encontrado, mas "
            "controls/buffer_input não foi localizado."
        )

    @staticmethod
    def _led_path(channel: int) -> Path:
        if not 0 <= channel <= 125:
            raise ValueError(
                f"Canal inválido: {channel}"
            )

        if channel == 0:
            name = "rgb:kbd_backlight"
        else:
            name = (
                f"rgb:kbd_backlight_{channel}"
            )

        path = (
            LED_ROOT
            / name
            / "multi_intensity"
        )

        if not path.exists():
            raise RuntimeError(
                f"LED {channel} não encontrado: {path}"
            )

        return path

    # =========================================================
    # RGB
    # =========================================================

    def get_rgb(
        self,
        channel: int,
    ) -> tuple[int, int, int]:
        values = (
            self._led_path(channel)
            .read_text()
            .strip()
            .split()
        )

        if len(values) != 3:
            raise RuntimeError(
                f"Resposta RGB inválida no canal "
                f"{channel}: {values}"
            )

        return tuple(
            map(int, values)
        )

    def set_rgb(
        self,
        channel: int,
        r: int,
        g: int,
        b: int,
    ):
        for value in (r, g, b):
            if not 0 <= value <= 255:
                raise ValueError(
                    "RGB deve estar entre 0 e 255."
                )

        self._led_path(
            channel
        ).write_text(
            f"{r} {g} {b}\n"
        )

    # =========================================================
    # BRILHO
    # =========================================================

    def get_brightness(self) -> int:
        """
        Retorna o brilho nativo do hardware: 0–50.
        """

        return int(
            self.BRIGHTNESS_PATH
            .read_text()
            .strip()
        )

    def set_brightness(
        self,
        value: int,
    ):
        """
        Define o brilho nativo do hardware: 0–50.
        """

        value = int(value)

        if not 0 <= value <= self.MAX_BRIGHTNESS:
            raise ValueError(
                "Brilho deve estar entre 0 e 50."
            )

        self.BRIGHTNESS_PATH.write_text(
            f"{value}\n"
        )

    def get_brightness_percent(self) -> int:
        """
        Retorna o brilho em escala amigável: 0–100%.
        """

        value = self.get_brightness()

        return round(
            value
            / self.MAX_BRIGHTNESS
            * 100
        )

    def set_brightness_percent(
        self,
        percent: int,
    ):
        """
        Recebe 0–100% e converte para 0–50.
        """

        percent = max(
            0,
            min(
                100,
                int(percent),
            ),
        )

        value = round(
            percent
            / 100
            * self.MAX_BRIGHTNESS
        )

        self.set_brightness(
            value
        )

    # =========================================================
    # BUFFER
    # =========================================================

    def set_buffer(
        self,
        enabled: bool,
    ):
        self.buffer_path.write_text(
            "1\n"
            if enabled
            else "0\n"
        )

    @contextmanager
    def batch(self):
        self.set_buffer(True)

        try:
            yield self

        finally:
            self.set_buffer(False)