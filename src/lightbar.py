from pathlib import Path


class Lightbar:
    RED = Path(
        "/sys/class/leds/lightbar_rgb:1:status/brightness"
    )

    GREEN = Path(
        "/sys/class/leds/lightbar_rgb:2:status/brightness"
    )

    BLUE = Path(
        "/sys/class/leds/lightbar_rgb:3:status/brightness"
    )

    ANIMATION = Path(
        "/sys/class/leds/lightbar_animation::status/brightness"
    )

    MAX_BRIGHTNESS = 36

    def __init__(self):
        self._check_available()

    def _check_available(self):
        missing = [
            path
            for path in (
                self.RED,
                self.GREEN,
                self.BLUE,
                self.ANIMATION,
            )
            if not path.exists()
        ]

        if missing:
            raise RuntimeError(
                "Lightbar não encontrada:\n"
                + "\n".join(str(path) for path in missing)
            )

    @staticmethod
    def _read(path: Path) -> int:
        return int(path.read_text().strip())

    @staticmethod
    def _write(path: Path, value: int):
        path.write_text(f"{value}\n")

    def get_raw_rgb(self) -> tuple[int, int, int]:
        return (
            self._read(self.RED),
            self._read(self.GREEN),
            self._read(self.BLUE),
        )

    def get_rgb(self) -> tuple[int, int, int]:
        """
        Retorna a cor normalizada para RGB 0–255.
        """
        raw = self.get_raw_rgb()

        return tuple(
            round(value / self.MAX_BRIGHTNESS * 255)
            for value in raw
        )

    def set_rgb(self, r: int, g: int, b: int):
        """
        Recebe RGB convencional 0–255 e converte para
        a escala 0–36 usada pela lightbar.
        """
        for value in (r, g, b):
            if not 0 <= value <= 255:
                raise ValueError(
                    "RGB deve estar entre 0 e 255."
                )

        values = [
            round(value / 255 * self.MAX_BRIGHTNESS)
            for value in (r, g, b)
        ]

        self._write(self.RED, values[0])
        self._write(self.GREEN, values[1])
        self._write(self.BLUE, values[2])

    def is_on(self) -> bool:
        return any(self.get_raw_rgb())

    def turn_off(self):
        self._write(self.RED, 0)
        self._write(self.GREEN, 0)
        self._write(self.BLUE, 0)

    def get_animation(self) -> bool:
        return bool(
            self._read(self.ANIMATION)
        )

    def set_animation(self, enabled: bool):
        self._write(
            self.ANIMATION,
            1 if enabled else 0,
        )