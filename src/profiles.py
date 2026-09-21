import json
import re
from pathlib import Path


PROFILE_DIR = (
    Path.home()
    / ".config"
    / "avell-rgb-control"
    / "profiles"
)


class ProfileManager:
    def __init__(self):
        PROFILE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _slug(name: str) -> str:
        """
        Converte o nome do perfil em um nome de arquivo seguro.
        Exemplo:
            "Meu Perfil Jogos" -> "meu-perfil-jogos"
        """
        slug = name.strip().lower()

        slug = re.sub(
            r"[^a-z0-9_-]+",
            "-",
            slug,
        )

        slug = slug.strip("-")

        return slug or "perfil"

    def save(
        self,
        name: str,
        keyboard: dict,
        lightbar: dict,
    ) -> Path:
        """
        Salva um perfil completo contendo teclado + lightbar.
        """

        name = name.strip()

        if not name:
            raise ValueError(
                "O perfil precisa de um nome."
            )

        path = PROFILE_DIR / (
            self._slug(name) + ".json"
        )

        data = {
            "version": 1,
            "name": name,
            "keyboard": keyboard,
            "lightbar": lightbar,
        }

        path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        return path

    def load(self, path: Path) -> dict:
        """
        Carrega e valida minimamente um perfil.
        """

        path = Path(path)

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            raise ValueError(
                "Formato de perfil inválido."
            )

        if data.get("version") != 1:
            raise ValueError(
                "Versão de perfil não suportada."
            )

        if "keyboard" not in data:
            raise ValueError(
                "Perfil não contém estado do teclado."
            )

        if "lightbar" not in data:
            raise ValueError(
                "Perfil não contém estado da lightbar."
            )

        return data

    def list_profiles(self):
        """
        Retorna:
            [(Path, dados), ...]
        """

        profiles = []

        for path in sorted(
            PROFILE_DIR.glob("*.json")
        ):
            try:
                data = self.load(path)

                profiles.append(
                    (path, data)
                )

            except Exception as exc:
                print(
                    f"Perfil inválido "
                    f"{path}: {exc}"
                )

        return profiles

    def delete(self, path: Path):
        """
        Exclui um perfil salvo.
        """

        Path(path).unlink(
            missing_ok=True
        )