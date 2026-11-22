# -*- coding: utf-8 -*-
"""
Módulo de configuración del sistema de registro de eventos y errores (logging).

Cumple el requisito de usar manejo de archivos únicamente para el archivo de logs,
sin emplear bases de datos.
"""

# Importa el módulo estándar de Python para registro estructurado de eventos.
import logging
# Importa el módulo os para garantizar la existencia de la carpeta de logs.
import os


def configurar_logger(
    nombre_logger: str = "SoftwareFJ",
    ruta_archivo: str = "logs/software_fj.log",
    reiniciar_archivo: bool = True,
) -> logging.Logger:
    """
    Configura y retorna un objeto Logger que escribe eventos y errores en un archivo de texto.

    Parámetros:
        nombre_logger (str): Nombre identificador del registrador.
        ruta_archivo (str): Ruta relativa o absoluta del archivo de logs.
        reiniciar_archivo (bool): Si es True, inicia un archivo limpio en cada ejecución.
    """
    # Obtiene el directorio padre de la ruta del archivo de logs.
    directorio = os.path.dirname(ruta_archivo)
    # Si se especificó un directorio y no existe en disco, lo crea automáticamente.
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    # Recupera o crea la instancia del logger con el nombre indicado.
    logger = logging.getLogger(nombre_logger)
    # Establece el nivel mínimo de registro en INFO para capturar eventos, advertencias y errores.
    logger.setLevel(logging.INFO)
    # Evita que los mensajes se propaguen al logger raíz y se dupliquen.
    logger.propagate = False

    # Si el logger ya tenía manejadores previos, los limpia para evitar líneas repetidas.
    if logger.handlers:
        for manejador in list(logger.handlers):
            manejador.close()
            logger.removeHandler(manejador)

    # Define el modo de apertura del archivo: 'w' reinicia el log; 'a' añade al final.
    modo = "w" if reiniciar_archivo else "a"
    # Crea el manejador de archivo con codificación UTF-8 para preservar tildes y eñes.
    manejador_archivo = logging.FileHandler(ruta_archivo, mode=modo, encoding="utf-8")
    # Configura el nivel del manejador de archivo en INFO.
    manejador_archivo.setLevel(logging.INFO)

    # Define el formato detallado con fecha, hora, nivel de severidad y mensaje.
    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Asocia el formato al manejador de archivo.
    manejador_archivo.setFormatter(formato)
    # Registra el manejador de archivo dentro del logger.
    logger.addHandler(manejador_archivo)

    # Retorna el logger completamente configurado y listo para usar.
    return logger


def registrar_error_detallado(logger: logging.Logger, contexto: str, error: Exception) -> None:
    """
    Registra una excepción en el archivo de logs incluyendo su causa encadenada si existe.

    Parámetros:
        logger (logging.Logger): Instancia del logger activo.
        contexto (str): Descripción de la operación donde ocurrió el fallo.
        error (Exception): Excepción capturada durante la ejecución.
    """
    # Verifica si la excepción fue lanzada mediante encadenamiento (raise ... from causa).
    causa = error.__cause__
    # Si existe una causa encadenada, registra tanto la excepción principal como la original.
    if causa is not None:
        logger.error(
            "%s | Excepción: %s (%s) | Causa encadenada: %s (%s)",
            contexto,
            type(error).__name__,
            error,
            type(causa).__name__,
            causa,
        )
    else:
        # Si no hay causa encadenada, registra el contexto, el tipo y el mensaje de error.
        logger.error(
            "%s | Excepción: %s (%s)",
            contexto,
            type(error).__name__,
            error,
        )