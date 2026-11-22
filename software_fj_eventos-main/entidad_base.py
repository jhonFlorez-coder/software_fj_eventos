# -*- coding: utf-8 -*-
"""
Módulo que define la clase abstracta EntidadBase del sistema Software FJ.

Aplica el principio de Abstracción de la Programación Orientada a Objetos (POO),
estableciendo el contrato común para todas las entidades del dominio (Cliente,
Servicio y Reserva).
"""

# Importa ABC y abstractmethod para definir clases y métodos abstractos en Python.
from abc import ABC, abstractmethod
# Importa datetime para registrar la marca de tiempo de creación de cada entidad.
from datetime import datetime
# Importa las excepciones personalizadas para validar el identificador de entidad.
from src.excepciones import ErrorDatosInvalidos, ErrorParametroFaltante


class EntidadBase(ABC):
    """
    Clase abstracta que representa cualquier entidad general dentro de Software FJ.

    Encapsula el identificador único y la fecha de creación, y obliga a las clases
    derivadas a implementar sus propios métodos de validación y resumen.
    """

    def __init__(self, id_entidad: str) -> None:
        """
        Inicializa los atributos comunes de toda entidad del sistema.

        Parámetros:
            id_entidad (str): Identificador único no vacío de la entidad.
        """
        # Verifica que el parámetro id_entidad no sea None antes de validarlo.
        if id_entidad is None:
            raise ErrorParametroFaltante("El parámetro obligatorio 'id_entidad' no fue proporcionado.")
        # Valida que el identificador sea una cadena de texto no vacía.
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ErrorDatosInvalidos("El 'id_entidad' debe ser una cadena de texto no vacía.")
        # Almacena el identificador limpio como atributo privado (encapsulación).
        self.__id_entidad: str = id_entidad.strip().upper()
        # Registra automáticamente la fecha y hora exacta de creación del objeto.
        self.__fecha_creacion: datetime = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        # Devuelve el valor del atributo privado __id_entidad.
        return self.__id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora en que fue creada la entidad (solo lectura)."""
        # Devuelve el objeto datetime de creación.
        return self.__fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """
        Método abstracto que cada subclase debe sobrescribir para validar
        la integridad completa de sus atributos.
        """
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """
        Método abstracto que cada subclase debe sobrescribir para retornar
        una representación legible y resumida de la entidad.
        """
        pass

    def __repr__(self) -> str:
        """Devuelve una representación técnica uniforme para depuración y logs."""
        # Incluye el nombre real de la subclase y su identificador único.
        return f"<{self.__class__.__name__} id={self.__id_entidad}>"