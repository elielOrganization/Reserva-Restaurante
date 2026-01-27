from dataclasses import dataclass, asdict

@dataclass
class User:
    email: str
    nombre: str
    passwd: str
    telefono: str
    usuario: str

    def to_dict(self) -> dict:
        d = asdict(self)
        return d
