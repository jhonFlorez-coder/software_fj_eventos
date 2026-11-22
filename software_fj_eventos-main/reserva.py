# -*- coding: utf-8 -*-
"""
Módulo que implementa la clase Reserva y su enumeración de estados.

Integra Cliente, Servicio, duración y estado, e implementa los procesos de
confirmación, cancelación y procesamiento con manejo avanzado de excepciones
(try/except, try/except/else, try/except/finally y encadenamiento).
"""

# Importa Enum para definir los estados válidos del ciclo de vida de una reserva.
from enum import Enum
# Importa Optional para parámetros opcionales en el cálculo sobrecargado.
from typing import Optional
# Importa la clase abstracta base EntidadBase.
from src.entidad_base import EntidadBase
# Importa las clases Cliente y Servicio que componen la reserva.
from src.cliente import Cliente
from src.servicios import Servicio
# Importa las excepciones personalizadas requeridas.
from src.excepciones import (
    ErrorCalculoInconsistente,
    ErrorOperacionNoPermitida,
    ErrorParametroFaltante,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
)


class EstadoReserva(Enum):
    """Enumera los estados permitidos dentro del ciclo de vida de una reserva."""

    # Estado inicial cuando la reserva recién se crea.
    PENDIENTE = "PENDIENTE"
    # Estado cuando la reserva fue verificada y aprobada.
    CONFIRMADA = "CONFIRMADA"
    # Estado final exitoso cuando el servicio ya fue ejecutado y facturado.
    PROCESADA = "PROCESADA"
    # Estado final cuando la reserva fue anulada antes de procesarse.
    CANCELADA = "CANCELADA"


class Reserva(EntidadBase):
    """
    Modela una reserva de servicio realizada por un cliente en Software FJ.
    """

    # Límite máximo permitido de duración en horas para una sola reserva.
    MAX_DURACION_HORAS = 72

    def __init__(
        self,
        id_entidad: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        tasa_impuesto: Optional[float] = 0.19,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> None:
        """
        Crea una reserva en estado PENDIENTE validando cliente, servicio, disponibilidad y costo.
        """
        # Invoca el constructor de EntidadBase para validar id_entidad y fecha_creacion.
        super().__init__(id_entidad)

        # Verifica que no falten los objetos obligatorios cliente o servicio.
        if cliente is None or servicio is None:
            raise ErrorParametroFaltante("Para crear una reserva se requieren los parámetros 'cliente' y 'servicio'.")

        # Valida que los objetos recibidos correspondan a las clases esperadas.
        if not isinstance(cliente, Cliente):
            raise ErrorReservaInvalida("El objeto 'cliente' proporcionado no es una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ErrorReservaInvalida("El objeto 'servicio' proporcionado no es una instancia válida de Servicio.")

        # Impide reservar si el cliente se encuentra inactivo.
        if not cliente.activo:
            raise ErrorOperacionNoPermitida(
                f"El cliente '{cliente.nombre}' ({cliente.id_entidad}) está inactivo y no puede reservar."
            )

        # Impide reservar si el servicio no se encuentra disponible.
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{servicio.nombre}' ({servicio.id_entidad}) no está disponible actualmente."
            )

        # Valida que la duración sea un entero dentro del rango permitido (1 a 72 horas).
        if isinstance(duracion, bool) or not isinstance(duracion, int) or not (1 <= duracion <= self.MAX_DURACION_HORAS):
            raise ErrorReservaInvalida(
                f"Duración inválida ({duracion} h): debe ser un entero entre 1 y {self.MAX_DURACION_HORAS} horas."
            )

        # Encapsula las referencias al cliente, servicio, duración y parámetros financieros.
        self.__cliente: Cliente = cliente
        self.__servicio: Servicio = servicio
        self.__duracion: int = duracion
        self.__tasa_impuesto: Optional[float] = tasa_impuesto
        self.__descuento: Optional[float] = descuento
        self.__cargo_extra: Optional[float] = cargo_extra
        # Inicializa el estado de la reserva como PENDIENTE.
        self.__estado: EstadoReserva = EstadoReserva.PENDIENTE
        # Inicializa el costo total calculándolo con manejo y encadenamiento de excepciones.
        self.__costo_total: float = 0.0
        self.__calcular_y_asignar_costo()
        # Registra el motivo de cancelación únicamente si la reserva llega a cancelarse.
        self.__motivo_cancelacion: Optional[str] = None
        # Ejecuta la validación integral de la entidad.
        self.validar()

    def __calcular_y_asignar_costo(self) -> None:
        """
        Calcula el costo total invocando el método polimórfico y sobrecargado del servicio.
        Usa encadenamiento de excepciones si ocurre una inconsistencia matemática.
        """
        try:
            # Invoca el método sobrecargado calcular_costo() del servicio asociado.
            self.__costo_total = self.__servicio.calcular_costo(
                duracion=self.__duracion,
                tasa_impuesto=self.__tasa_impuesto,
                descuento=self.__descuento,
                cargo_extra=self.__cargo_extra,
            )
        except ErrorCalculoInconsistente as error_calc:
            # Encadena la excepción de cálculo dentro de una excepción de reserva inválida.
            raise ErrorReservaInvalida(
                f"No fue posible calcular un costo válido para la reserva {self.id_entidad}."
            ) from error_calc

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente titular de la reserva."""
        # Devuelve el objeto Cliente encapsulado.
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio reservado."""
        # Devuelve el objeto Servicio encapsulado.
        return self.__servicio

    @property
    def duracion(self) -> int:
        """Retorna la duración contratada en horas."""
        # Devuelve el entero privado __duracion.
        return self.__duracion

    @property
    def estado(self) -> EstadoReserva:
        """Retorna el estado actual de la reserva."""
        # Devuelve el miembro del Enum EstadoReserva.
        return self.__estado

    @property
    def costo_total(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        # Devuelve el monto total en COP.
        return self.__costo_total

    def confirmar(self) -> str:
        """
        Cambia el estado de la reserva de PENDIENTE a CONFIRMADA.
        Utiliza bloque try/except/else para garantizar la consistencia del estado.
        """
        try:
            # Verifica que la reserva esté en estado PENDIENTE antes de confirmarla.
            if self.__estado != EstadoReserva.PENDIENTE:
                raise ErrorOperacionNoPermitida(
                    f"No se puede confirmar la reserva {self.id_entidad} porque su estado actual es {self.__estado.value}."
                )
            # Revalida que el servicio siga disponible al momento de la confirmación.
            if not self.__servicio.disponible:
                raise ErrorServicioNoDisponible(
                    f"El servicio '{self.__servicio.nombre}' dejó de estar disponible antes de confirmar."
                )
        except (ErrorOperacionNoPermitida, ErrorServicioNoDisponible):
            # Propaga la excepción controlada hacia el gestor para su registro en logs.
            raise
        else:
            # Se ejecuta solo si no ocurrió ninguna excepción en el bloque try.
            self.__estado = EstadoReserva.CONFIRMADA
            # Marca el servicio como ocupado temporalmente mientras la reserva esté activa.
            self.__servicio.disponible = False
            # Retorna un mensaje de confirmación exitosa.
            return f"Reserva {self.id_entidad} confirmada exitosamente para {self.__cliente.nombre}."

    def cancelar(self, motivo: str = "Cancelación solicitada por el cliente") -> str:
        """
        Cancela una reserva PENDIENTE o CONFIRMADA y libera el servicio en el bloque finally.
        """
        # Bandera auxiliar que indica si se debe liberar la disponibilidad del servicio.
        liberar_servicio = False
        try:
            # Valida que el motivo de cancelación sea una cadena no vacía.
            if not isinstance(motivo, str) or not motivo.strip():
                raise ErrorParametroFaltante("Debe proporcionar un motivo válido para cancelar la reserva.")
            # Impide cancelar reservas que ya fueron procesadas o canceladas previamente.
            if self.__estado in {EstadoReserva.PROCESADA, EstadoReserva.CANCELADA}:
                raise ErrorOperacionNoPermitida(
                    f"No se puede cancelar la reserva {self.id_entidad} en estado {self.__estado.value}."
                )
            # Si estaba confirmada, marca que el servicio debe quedar disponible de nuevo.
            if self.__estado == EstadoReserva.CONFIRMADA:
                liberar_servicio = True
            # Actualiza el estado a CANCELADA y guarda el motivo.
            self.__estado = EstadoReserva.CANCELADA
            self.__motivo_cancelacion = motivo.strip()
            # Retorna el mensaje confirmando la cancelación.
            return f"Reserva {self.id_entidad} cancelada. Motivo: {self.__motivo_cancelacion}."
        except (ErrorParametroFaltante, ErrorOperacionNoPermitida):
            # Re-lanza la excepción para que sea capturada y registrada por el gestor.
            raise
        finally:
            # El bloque finally siempre se ejecuta para liberar el recurso si correspondía.
            if liberar_servicio:
                self.__servicio.disponible = True

    def procesar(self) -> str:
        """
        Procesa y finaliza una reserva que debe encontrarse previamente CONFIRMADA.
        Utiliza try/except/else/finally para asegurar la liberación del servicio al concluir.
        """
        # Bandera para indicar si el procesamiento concluyó y el servicio puede liberarse.
        procesamiento_exitoso = False
        try:
            # Exige que la reserva haya sido confirmada previamente.
            if self.__estado != EstadoReserva.CONFIRMADA:
                raise ErrorOperacionNoPermitida(
                    f"No se puede procesar la reserva {self.id_entidad} porque su estado es "
                    f"{self.__estado.value} (debe estar CONFIRMADA)."
                )
            # Verifica nuevamente que el costo calculado sea consistente antes de facturar.
            if self.__costo_total <= 0:
                raise ErrorCalculoInconsistente(
                    f"El monto de la reserva {self.id_entidad} (${self.__costo_total:,.2f}) es inconsistente."
                )
        except (ErrorOperacionNoPermitida, ErrorCalculoInconsistente):
            # Propaga la excepción para su registro en el archivo de logs.
            raise
        else:
            # Si no hubo errores, cambia el estado final a PROCESADA.
            self.__estado = EstadoReserva.PROCESADA
            procesamiento_exitoso = True
            # Retorna la confirmación de procesamiento con el valor total.
            return (
                f"Reserva {self.id_entidad} procesada y finalizada correctamente. "
                f"Total facturado: ${self.__costo_total:,.2f} COP."
            )
        finally:
            # Al terminar el procesamiento exitoso, el servicio vuelve a quedar disponible.
            if procesamiento_exitoso:
                self.__servicio.disponible = True

    def validar(self) -> bool:
        """Sobrescribe EntidadBase.validar() verificando la integridad de la reserva."""
        # Confirma que cliente, servicio y costo total sean consistentes.
        if self.__costo_total <= 0:
            raise ErrorCalculoInconsistente("La reserva no tiene un costo total válido.")
        # Retorna True confirmando validez.
        return True

    def obtener_resumen(self) -> str:
        """Sobrescribe EntidadBase.obtener_resumen() con el detalle completo de la reserva."""
        # Retorna una línea clara con ID, cliente, servicio, duración, estado y total.
        return (
            f"Reserva [{self.id_entidad}] Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion} h | "
            f"Estado: {self.__estado.value} | Total: ${self.__costo_total:,.2f} COP"
        )