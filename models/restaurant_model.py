from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Horario:
    apertura: str
    cierre: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Restaurante:
    id: str
    nombre: str
    direccion: str
    telefono: str
    aforo_maximo: int
    horario: Horario
    reservas: List[dict]
    imagen_url: str
    imagenes: str

    def to_dict(self) -> dict:
        d = asdict(self)
        d['horario'] = self.horario.to_dict()
        return d
