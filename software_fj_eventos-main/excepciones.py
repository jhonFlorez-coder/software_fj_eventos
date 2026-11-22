# -*- coding: utf-8 -*-
"""
Módulo de excepciones personalizadas para el sistema Software FJ.

Define una jerarquía de excepciones específicas del dominio que permiten
identificar, capturar, encadenar y registrar cualquier error sin detener
la ejecución normal de la aplicación.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la que heredan todas las excepciones del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000") -> None:
        """Inicializa la excepción base con un mensaje descriptivo y un código interno."""
        # Almacena el código identificador del error para facilitar su trazabilidad en logs.
        self.codigo = codigo
        # Almacena el mensaje legible del error para mostrarlo al usuario y registrarlo.
        self.mensaje = mensaje
        # Invoca el constructor de la clase padre Exception con el formato estándar.
        super().__init__(f"[{codigo}] {mensaje}")


class ErrorDatosInvalidos(ErrorSoftwareFJ):
    """Se lanza cuando un atributo o dato ingresado no cumple las reglas de validación."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-101 para errores de validación de datos."""
        # Llama al constructor padre con el código correspondiente a datos inválidos.
        super().__init__(mensaje, codigo="ERR-101")


class ErrorParametroFaltante(ErrorSoftwareFJ):
    """Se lanza cuando un parámetro obligatorio es None, vacío o fue omitido."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-102 para parámetros obligatorios ausentes."""
        # Llama al constructor padre con el código correspondiente a parámetros faltantes.
        super().__init__(mensaje, codigo="ERR-102")


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Se lanza cuando se intenta ejecutar una acción prohibida por el estado o reglas de negocio."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-201 para operaciones no permitidas."""
        # Llama al constructor padre con el código de operación no autorizada o inválida.
        super().__init__(mensaje, codigo="ERR-201")


class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza cuando los datos o condiciones para crear una reserva son incorrectos."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-301 para intentos de reserva incorrectos."""
        # Llama al constructor padre con el código de reserva inválida.
        super().__init__(mensaje, codigo="ERR-301")


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio que actualmente no está disponible."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-302 para servicios no disponibles."""
        # Llama al constructor padre con el código de indisponibilidad de servicio.
        super().__init__(mensaje, codigo="ERR-302")


class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo financiero arroja valores incoherentes o parámetros fuera de rango."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-401 para inconsistencias en el cálculo de costos."""
        # Llama al constructor padre con el código de error de cálculo.
        super().__init__(mensaje, codigo="ERR-401")


class ErrorEntidadNoEncontrada(ErrorSoftwareFJ):
    """Se lanza cuando una búsqueda por identificador no encuentra resultados en las listas internas."""

    def __init__(self, mensaje: str) -> None:
        """Asigna el código específico ERR-501 para entidades inexistentes."""
        # Llama al constructor padre con el código de entidad no encontrada.
        super().__init__(mensaje, codigo="ERR-501")