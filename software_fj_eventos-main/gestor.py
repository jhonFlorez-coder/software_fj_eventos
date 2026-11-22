# -*- coding: utf-8 -*-
"""
Módulo coordinador GestorSoftwareFJ.

Administra en memoria (listas internas, sin bases de datos) los clientes,
servicios y reservas de Software FJ. Centraliza el manejo de excepciones,
encadenamiento y escritura en el archivo de logs para garantizar que la
aplicación permanezca activa y estable ante cualquier error.
"""

# Importa List y Optional para tipado claro de las colecciones internas.
from typing import List, Optional
# Importa el tipo Logger para anotar el registrador de eventos.
import logging
# Importa las entidades del dominio.
from src.cliente import Cliente
from src.servicios import Servicio
from src.reserva import Reserva
# Importa las excepciones personalizadas del sistema.
from src.excepciones import (
    ErrorDatosInvalidos,
    ErrorEntidadNoEncontrada,
    ErrorSoftwareFJ,
)
# Importa la función auxiliar para registrar errores con causa encadenada en el log.
from src.logger import registrar_error_detallado


class GestorSoftwareFJ:
    """
    Controlador principal del sistema Software FJ basado en listas internas en memoria.
    """

    def __init__(self, logger: logging.Logger) -> None:
        """
        Inicializa las listas internas de clientes, servicios y reservas, además de contadores.
        """
        # Almacena la referencia al logger configurado para el archivo de logs.
        self.__logger: logging.Logger = logger
        # Lista interna en memoria para almacenar objetos Cliente (sin base de datos).
        self.__clientes: List[Cliente] = []
        # Lista interna en memoria para almacenar objetos Servicio (polimórficos).
        self.__servicios: List[Servicio] = []
        # Lista interna en memoria para almacenar objetos Reserva.
        self.__reservas: List[Reserva] = []
        # Contadores de métricas de ejecución para el informe final de estabilidad.
        self.__operaciones_exitosas: int = 0
        self.__errores_controlados: int = 0
        # Registra el arranque del gestor en el archivo de logs.
        self.__logger.info("Sistema GestorSoftwareFJ inicializado correctamente (almacenamiento en memoria).")

    @property
    def clientes(self) -> List[Cliente]:
        """Retorna una copia superficial de la lista de clientes para proteger la encapsulación."""
        # Devuelve una copia para impedir modificaciones externas directas de la lista interna.
        return list(self.__clientes)

    @property
    def servicios(self) -> List[Servicio]:
        """Retorna una copia superficial de la lista de servicios."""
        # Devuelve una copia de la colección interna de servicios.
        return list(self.__servicios)

    @property
    def reservas(self) -> List[Reserva]:
        """Retorna una copia superficial de la lista de reservas."""
        # Devuelve una copia de la colección interna de reservas.
        return list(self.__reservas)

    @property
    def operaciones_exitosas(self) -> int:
        """Retorna la cantidad de operaciones ejecutadas con éxito."""
        # Devuelve el contador interno de éxitos.
        return self.__operaciones_exitosas

    @property
    def errores_controlados(self) -> int:
        """Retorna la cantidad de errores capturados y registrados sin detener el sistema."""
        # Devuelve el contador interno de errores controlados.
        return self.__errores_controlados

    def registrar_cliente(
        self,
        id_entidad: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
        activo: bool = True,
    ) -> Optional[Cliente]:
        """
        Crea y agrega un cliente a la lista interna usando try/except/else.
        Si ocurre un error, lo registra en el log y retorna None sin detener el sistema.
        """
        try:
            # Verifica que no exista ya un cliente con el mismo ID o documento.
            for existente in self.__clientes:
                if existente.id_entidad == str(id_entidad).strip().upper():
                    raise ErrorDatosInvalidos(f"Ya existe un cliente registrado con el ID '{id_entidad}'.")
                if existente.documento == str(documento).strip():
                    raise ErrorDatosInvalidos(f"Ya existe un cliente registrado con el documento '{documento}'.")
            # Instancia el objeto Cliente (ejecuta todas las validaciones de los setters).
            nuevo_cliente = Cliente(id_entidad, nombre, documento, correo, telefono, activo)
        except ErrorSoftwareFJ as error:
            # Incrementa el contador de errores controlados y escribe el fallo en el archivo de logs.
            self.__errores_controlados += 1
            registrar_error_detallado(self.__logger, f"Registro de cliente ({id_entidad})", error)
            # Retorna None indicando que el registro no prosperó, manteniendo la app estable.
            return None
        else:
            # Solo si no hubo excepciones, almacena el cliente en la lista interna.
            self.__clientes.append(nuevo_cliente)
            self.__operaciones_exitosas += 1
            # Registra el evento exitoso en el archivo de logs.
            self.__logger.info("Cliente registrado con éxito: %s", nuevo_cliente.obtener_resumen())
            # Retorna el cliente recién creado.
            return nuevo_cliente

    def registrar_servicio(self, constructor_servicio, **kwargs) -> Optional[Servicio]:
        """
        Instancia y registra cualquier subclase de Servicio usando encadenamiento de excepciones
        y bloque try/except/else.
        """
        # Extrae el ID solicitado para identificar la operación en el archivo de logs.
        id_srv = kwargs.get("id_entidad", "SIN-ID")
        try:
            # Comprueba que no haya otro servicio con el mismo identificador.
            for existente in self.__servicios:
                if existente.id_entidad == str(id_srv).strip().upper():
                    raise ErrorDatosInvalidos(f"Ya existe un servicio registrado con el ID '{id_srv}'.")
            try:
                # Intenta construir la subclase concreta de Servicio con los argumentos recibidos.
                nuevo_servicio = constructor_servicio(**kwargs)
            except TypeError as error_tipo:
                # Encadena un TypeError (parámetros faltantes o inesperados) en una excepción del dominio.
                raise ErrorDatosInvalidos(
                    f"Parámetros incompatibles al crear servicio '{id_srv}'."
                ) from error_tipo
            except ErrorSoftwareFJ as error_dominio:
                # Encadena el error de validación específico con contexto del gestor.
                raise ErrorDatosInvalidos(
                    f"Falló la creación del servicio '{id_srv}' ({constructor_servicio.__name__})."
                ) from error_dominio
        except ErrorSoftwareFJ as error:
            # Contabiliza y registra el error junto con su causa encadenada.
            self.__errores_controlados += 1
            registrar_error_detallado(self.__logger, f"Registro de servicio ({id_srv})", error)
            # Retorna None manteniendo estable la ejecución.
            return None
        else:
            # Agrega el servicio validado a la lista polimórfica interna.
            self.__servicios.append(nuevo_servicio)
            self.__operaciones_exitosas += 1
            # Registra la creación exitosa en el log.
            self.__logger.info("Servicio registrado con éxito: %s", nuevo_servicio.obtener_resumen())
            # Retorna el objeto servicio.
            return nuevo_servicio

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por su ID en la lista interna o lanza ErrorEntidadNoEncontrada."""
        # Recorre la lista interna de clientes comparando el identificador normalizado.
        for cliente in self.__clientes:
            if cliente.id_entidad == id_cliente.strip().upper():
                return cliente
        # Si no se encuentra coincidencia, lanza una excepción controlada.
        raise ErrorEntidadNoEncontrada(f"No se encontró ningún cliente con el ID '{id_cliente}'.")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por su ID en la lista interna o lanza ErrorEntidadNoEncontrada."""
        # Recorre la lista interna de servicios comparando el identificador normalizado.
        for servicio in self.__servicios:
            if servicio.id_entidad == id_servicio.strip().upper():
                return servicio
        # Si no existe, lanza la excepción personalizada correspondiente.
        raise ErrorEntidadNoEncontrada(f"No se encontró ningún servicio con el ID '{id_servicio}'.")

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: int,
        tasa_impuesto: Optional[float] = 0.19,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> Optional[Reserva]:
        """
        Crea una reserva vinculando cliente y servicio existentes mediante try/except/else/finally.
        """
        try:
            # Verifica que el ID de reserva no esté duplicado en la lista interna.
            for existente in self.__reservas:
                if existente.id_entidad == str(id_reserva).strip().upper():
                    raise ErrorDatosInvalidos(f"Ya existe una reserva con el ID '{id_reserva}'.")
            # Localiza las entidades cliente y servicio en las listas en memoria.
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            # Crea el objeto Reserva aplicando todas las validaciones de negocio.
            nueva_reserva = Reserva(
                id_entidad=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                tasa_impuesto=tasa_impuesto,
                descuento=descuento,
                cargo_extra=cargo_extra,
            )
        except ErrorSoftwareFJ as error:
            # Registra la excepción (y su causa encadenada si la hay) en el archivo de logs.
            self.__errores_controlados += 1
            registrar_error_detallado(self.__logger, f"Creación de reserva ({id_reserva})", error)
            # Retorna None sin interrumpir el programa.
            return None
        else:
            # Almacena la reserva creada en la lista interna y registra el éxito.
            self.__reservas.append(nueva_reserva)
            self.__operaciones_exitosas += 1
            self.__logger.info("Reserva creada con éxito: %s", nueva_reserva.obtener_resumen())
            # Devuelve la nueva reserva.
            return nueva_reserva
        finally:
            # Registra el cierre del intento de reserva para trazabilidad completa.
            self.__logger.info("Finalizado intento de creación de reserva '%s'.", id_reserva)

    def ejecutar_accion_reserva(self, reserva: Optional[Reserva], accion: str, motivo: str = "") -> bool:
        """
        Ejecuta una transición de estado sobre una reserva ('confirmar', 'cancelar', 'procesar')
        con manejo seguro de excepciones y registro en el log.
        """
        try:
            # Valida que la referencia a la reserva no sea None.
            if reserva is None:
                raise ErrorEntidadNoEncontrada("No se puede ejecutar la acción porque la reserva es nula.")
            # Despacha la operación solicitada según el nombre de la acción.
            if accion == "confirmar":
                mensaje = reserva.confirmar()
            elif accion == "cancelar":
                mensaje = reserva.cancelar(motivo or "Cancelación estándar")
            elif accion == "procesar":
                mensaje = reserva.procesar()
            else:
                raise ErrorDatosInvalidos(f"Acción de reserva no reconocida: '{accion}'.")
        except ErrorSoftwareFJ as error:
            # Registra la falla controlada en el archivo de logs sin abortar la ejecución.
            self.__errores_controlados += 1
            id_ref = reserva.id_entidad if reserva is not None else "NULA"
            registrar_error_detallado(self.__logger, f"Acción '{accion}' en reserva ({id_ref})", error)
            # Retorna False indicando que la transición fue rechazada.
            return False
        else:
            # Contabiliza y registra la transición exitosa en el archivo de logs.
            self.__operaciones_exitosas += 1
            self.__logger.info(mensaje)
            # Retorna True confirmando el cambio de estado.
            return True