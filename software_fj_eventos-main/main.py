# -*- coding: utf-8 -*-
"""
Punto de entrada principal del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de Software FJ (UNAD - Programación 213023 - Fase 4).

Simula 14 operaciones completas (superando el mínimo de 10 exigido) que incluyen:
- Registros válidos e inválidos de clientes.
- Creación correcta e incorrecta de servicios (3 tipos polimórficos).
- Demostración de polimorfismo y métodos sobrecargados en el cálculo de costos.
- Manejo de cálculos inconsistentes con encadenamiento de excepciones.
- Reservas exitosas, confirmaciones, cancelaciones, procesamientos y fallos controlados.
- Verificación de que el sistema nunca se detiene ante errores graves y registra todo en logs.
"""

# Importa os para construir la ruta absoluta del archivo de logs de manera portable.
import os
# Importa la función de configuración y registro detallado de logs.
from src.logger import configurar_logger, registrar_error_detallado
# Importa el gestor principal que administra las listas internas en memoria.
from src.gestor import GestorSoftwareFJ
# Importa las tres clases concretas derivadas de la clase abstracta Servicio.
from src.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
# Importa las excepciones personalizadas usadas en pruebas directas de cálculo.
from src.excepciones import ErrorCalculoInconsistente, ErrorSoftwareFJ


def imprimir_separador(numero: int, titulo: str) -> None:
    """Imprime un encabezado legible en consola para cada operación simulada."""
    # Construye una línea separadora uniforme para facilitar la lectura de la simulación.
    print("\n" + "=" * 78)
    print(f"OPERACIÓN {numero:02d}: {titulo}")
    print("=" * 78)


def ejecutar_simulacion() -> None:
    """Ejecuta las 14 operaciones completas del sistema Software FJ sin base de datos."""
    # Determina la carpeta raíz del proyecto a partir de la ubicación de main.py.
    directorio_base = os.path.dirname(os.path.abspath(__file__))
    # Define la ruta donde se guardará el archivo de logs de eventos y errores.
    ruta_log = os.path.join(directorio_base, "logs", "software_fj.log")
    # Inicializa el logger reiniciando el archivo para obtener un registro limpio.
    logger = configurar_logger(ruta_archivo=ruta_log, reiniciar_archivo=True)
    # Crea la instancia del gestor principal en memoria.
    gestor = GestorSoftwareFJ(logger)

    print("*" * 78)
    print("  SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("  Ejecución sin base de datos | POO + Manejo Avanzado de Excepciones")
    print("*" * 78)

    # -------------------------------------------------------------------------
    # OPERACIÓN 01: Registro válido de clientes (try/except/else interno)
    # -------------------------------------------------------------------------
    imprimir_separador(1, "Registro válido de clientes (activos e inactivo)")
    # Registra tres clientes con todos sus datos personales válidos.
    c1 = gestor.registrar_cliente("CLI-001", "Laura Gómez", "1023456789", "laura.gomez@correo.co", "+573001112233", True)
    c2 = gestor.registrar_cliente("CLI-002", "Carlos Méndez", "1098765432", "carlos.mendez@empresa.com", "3104445566", True)
    c3 = gestor.registrar_cliente("CLI-003", "Andrés Pardo", "1055667788", "andres.pardo@correo.co", "3207778899", False)
    # Muestra en consola el resumen encapsulado de cada cliente registrado.
    for cliente in (c1, c2, c3):
        if cliente:
            print("  [OK]", cliente.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 02: Registro inválido de cliente (correo y documento inválidos)
    # -------------------------------------------------------------------------
    imprimir_separador(2, "Registro inválido de cliente (datos mal formados)")
    # Intenta registrar un cliente con correo sin dominio válido.
    res_err_1 = gestor.registrar_cliente("CLI-004", "Marta Ruiz", "1044556677", "correo_invalido_sin_arroba", "3009998877")
    # Intenta registrar un cliente con documento demasiado corto y letras.
    res_err_2 = gestor.registrar_cliente("CLI-005", "Pedro Solis", "AB12", "pedro@correo.co", "3012223344")
    # Confirma que ambos errores fueron capturados y el programa continúa.
    print(f"  [CONTROLADO] Intento correo inválido -> Retorno: {res_err_1} (registrado en log).")
    print(f"  [CONTROLADO] Intento documento inválido -> Retorno: {res_err_2} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 03: Registro inválido de cliente por parámetro faltante (None)
    # -------------------------------------------------------------------------
    imprimir_separador(3, "Registro inválido de cliente (parámetro obligatorio faltante)")
    # Envía None como nombre del cliente para disparar ErrorParametroFaltante.
    res_err_3 = gestor.registrar_cliente("CLI-006", None, "1077889900", "sin.nombre@correo.co", "3156667788")
    print(f"  [CONTROLADO] Intento con nombre=None -> Retorno: {res_err_3} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 04: Creación correcta de los tres tipos de servicios
    # -------------------------------------------------------------------------
    imprimir_separador(4, "Creación correcta de servicios (Sala, Alquiler y Asesoría)")
    # Crea un servicio de tipo ReservaSala.
    s1 = gestor.registrar_servicio(
        ReservaSala,
        id_entidad="SRV-001",
        nombre="Sala Ejecutiva Innovación",
        tarifa_base=120000.0,
        capacidad=20,
        incluye_audiovisual=True,
        disponible=True,
    )
    # Crea un servicio de tipo AlquilerEquipo.
    s2 = gestor.registrar_servicio(
        AlquilerEquipo,
        id_entidad="SRV-002",
        nombre="Kit Portátiles Desarrollo",
        tarifa_base=25000.0,
        categoria_equipo="Computación Portátil",
        cantidad_unidades=4,
        seguro_incluido=True,
        disponible=True,
    )
    # Crea un servicio de tipo AsesoriaEspecializada.
    s3 = gestor.registrar_servicio(
        AsesoriaEspecializada,
        id_entidad="SRV-003",
        nombre="Arquitectura Cloud & Seguridad",
        tarifa_base=180000.0,
        area_especialidad="Arquitectura de Software",
        nivel_complejidad="AVANZADO",
        modalidad="PRESENCIAL",
        disponible=True,
    )
    # Crea una segunda sala inicialmente marcada como no disponible para pruebas posteriores.
    s4 = gestor.registrar_servicio(
        ReservaSala,
        id_entidad="SRV-004",
        nombre="Auditorio Principal",
        tarifa_base=250000.0,
        capacidad=100,
        incluye_audiovisual=True,
        disponible=False,
    )
    for srv in (s1, s2, s3, s4):
        if srv:
            print("  [OK]", srv.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 05: Creación incorrecta de servicios (encadenamiento de excepciones)
    # -------------------------------------------------------------------------
    imprimir_separador(5, "Creación incorrecta de servicios (validación y encadenamiento)")
    # Intenta crear una sala con capacidad negativa (-5) y tarifa inválida.
    srv_err_1 = gestor.registrar_servicio(
        ReservaSala,
        id_entidad="SRV-005",
        nombre="Sala Fallida",
        tarifa_base=90000.0,
        capacidad=-5,
        incluye_audiovisual=False,
    )
    # Intenta crear una asesoría con nivel de complejidad inexistente ('EXTREMO').
    srv_err_2 = gestor.registrar_servicio(
        AsesoriaEspecializada,
        id_entidad="SRV-006",
        nombre="Asesoría Inválida",
        tarifa_base=150000.0,
        area_especialidad="Redes",
        nivel_complejidad="EXTREMO",
        modalidad="VIRTUAL",
    )
    print(f"  [CONTROLADO] Sala con capacidad -5 -> Retorno: {srv_err_1} (causa encadenada en log).")
    print(f"  [CONTROLADO] Asesoría nivel 'EXTREMO' -> Retorno: {srv_err_2} (causa encadenada en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 06: Polimorfismo y métodos sobrecargados en calcular_costo()
    # -------------------------------------------------------------------------
    imprimir_separador(6, "Demostración de Polimorfismo y Sobrecarga de calcular_costo()")
    # Itera polimórficamente sobre los tres tipos de servicios registrados.
    for servicio in [s1, s2, s3]:
        # Invoca las 4 variantes sobrecargadas de calcular_costo() para 3 horas.
        costo_base = servicio.calcular_costo(3)
        costo_iva = servicio.calcular_costo(3, tasa_impuesto=0.19)
        costo_desc_iva = servicio.calcular_costo(3, tasa_impuesto=0.19, descuento=0.10)
        costo_completo = servicio.calcular_costo(3, tasa_impuesto=0.19, descuento=0.10, cargo_extra=15000.0)
        print(f"  * {servicio.nombre} ({servicio.__class__.__name__}):")
        print(f"      - Variante 1 (solo duración 3h):                    ${costo_base:,.2f} COP")
        print(f"      - Variante 2 (con IVA 19%):                         ${costo_iva:,.2f} COP")
        print(f"      - Variante 3 (IVA 19% + descuento 10%):             ${costo_desc_iva:,.2f} COP")
        print(f"      - Variante 4 (IVA 19% + desc 10% + recargo $15k):   ${costo_completo:,.2f} COP")
    logger.info("Demostración de polimorfismo y sobrecarga ejecutada sobre 3 servicios distintos.")

    # -------------------------------------------------------------------------
    # OPERACIÓN 07: Cálculo inconsistente (descuento >= 100%) con try/except/finally
    # -------------------------------------------------------------------------
    imprimir_separador(7, "Manejo de cálculo inconsistente (descuento 120%)")
    try:
        # Fuerza un cálculo inconsistente pasando un descuento del 120% (1.20).
        s1.calcular_costo(duracion=2, tasa_impuesto=0.19, descuento=1.20)
    except ErrorCalculoInconsistente as error_calc:
        # Registra el error matemático controlado en el archivo de logs.
        registrar_error_detallado(logger, "Prueba directa de cálculo inconsistente", error_calc)
        print(f"  [CONTROLADO] Excepción capturada: {error_calc}")
    finally:
        # El bloque finally confirma el cierre seguro del cálculo.
        print("  [FINALLY] Auditoría de cálculo inconsistente finalizada sin afectar la app.")

    # -------------------------------------------------------------------------
    # OPERACIÓN 08: Reserva exitosa de Sala (crear -> confirmar -> procesar)
    # -------------------------------------------------------------------------
    imprimir_separador(8, "Reserva exitosa de Sala: ciclo completo (PENDIENTE -> CONFIRMADA -> PROCESADA)")
    # Crea la reserva para Laura Gómez en la Sala Ejecutiva Innovación por 4 horas con 10% descuento.
    r1 = gestor.crear_reserva("RES-001", "CLI-001", "SRV-001", duracion=4, tasa_impuesto=0.19, descuento=0.10)
    # Confirma y procesa la reserva pasando por las validaciones de estado.
    gestor.ejecutar_accion_reserva(r1, "confirmar")
    gestor.ejecutar_accion_reserva(r1, "procesar")
    if r1:
        print("  [OK]", r1.obtener_resumen())
        print(f"  [OK] Disponibilidad restaurada de '{s1.nombre}' tras procesar: {s1.disponible}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 09: Reserva exitosa de Alquiler y cancelación controlada
    # -------------------------------------------------------------------------
    imprimir_separador(9, "Reserva de Alquiler de Equipos: creación, confirmación y cancelación")
    # Crea y confirma la reserva de portátiles para Carlos Méndez.
    r2 = gestor.crear_reserva("RES-002", "CLI-002", "SRV-002", duracion=5, tasa_impuesto=0.19)
    gestor.ejecutar_accion_reserva(r2, "confirmar")
    print(f"  [INFO] Disponibilidad de '{s2.nombre}' mientras está confirmada: {s2.disponible}")
    # Cancela la reserva y verifica que el bloque finally libera el servicio.
    gestor.ejecutar_accion_reserva(r2, "cancelar", motivo="Reprogramación de agenda corporativa")
    if r2:
        print("  [OK]", r2.obtener_resumen())
        print(f"  [OK] Disponibilidad restaurada de '{s2.nombre}' tras cancelar: {s2.disponible}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva fallida por servicio no disponible
    # -------------------------------------------------------------------------
    imprimir_separador(10, "Reserva fallida: servicio no disponible (SRV-004)")
    # Intenta reservar el Auditorio Principal cuya disponibilidad es False.
    r_err_1 = gestor.crear_reserva("RES-003", "CLI-001", "SRV-004", duracion=3)
    print(f"  [CONTROLADO] Reserva de servicio no disponible -> Retorno: {r_err_1} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida por duración inválida y cliente inactivo
    # -------------------------------------------------------------------------
    imprimir_separador(11, "Reservas fallidas: duración negativa y cliente inactivo")
    # Intenta reservar con duración 0 horas.
    r_err_2 = gestor.crear_reserva("RES-004", "CLI-001", "SRV-001", duracion=0)
    # Intenta reservar usando a Andrés Pardo (CLI-003), quien está inactivo.
    r_err_3 = gestor.crear_reserva("RES-005", "CLI-003", "SRV-001", duracion=2)
    print(f"  [CONTROLADO] Duración 0 h -> Retorno: {r_err_2} (registrado en log).")
    print(f"  [CONTROLADO] Cliente inactivo CLI-003 -> Retorno: {r_err_3} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Operación no permitida (procesar reserva sin confirmar)
    # -------------------------------------------------------------------------
    imprimir_separador(12, "Operación no permitida: intentar procesar reserva en estado PENDIENTE")
    # Crea una reserva de Asesoría Especializada dejándola en estado PENDIENTE.
    r3 = gestor.crear_reserva("RES-006", "CLI-002", "SRV-003", duracion=2, tasa_impuesto=0.19, cargo_extra=20000.0)
    # Intenta procesarla directamente sin confirmarla primero.
    exito_proc_indebido = gestor.ejecutar_accion_reserva(r3, "procesar")
    print(f"  [CONTROLADO] Procesar reserva PENDIENTE -> Éxito: {exito_proc_indebido} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 13: Operación no permitida (confirmar una reserva ya CANCELADA)
    # -------------------------------------------------------------------------
    imprimir_separador(13, "Operación no permitida: intentar confirmar una reserva CANCELADA")
    # Intenta confirmar r2, que fue cancelada en la Operación 09.
    exito_conf_cancelada = gestor.ejecutar_accion_reserva(r2, "confirmar")
    print(f"  [CONTROLADO] Confirmar reserva CANCELADA (RES-002) -> Éxito: {exito_conf_cancelada} (registrado en log).")

    # -------------------------------------------------------------------------
    # OPERACIÓN 14: Cierre exitoso de RES-006 (confirmar y procesar) + Resumen final
    # -------------------------------------------------------------------------
    imprimir_separador(14, "Confirmación y procesamiento final de Asesoría + Balance de estabilidad")
    # Confirma y procesa correctamente la reserva r3 que permanecía en estado PENDIENTE.
    gestor.ejecutar_accion_reserva(r3, "confirmar")
    gestor.ejecutar_accion_reserva(r3, "procesar")
    if r3:
        print("  [OK]", r3.obtener_resumen())

    # Imprime el balance general demostrando continuidad operativa sin caídas.
    print("\n" + "*" * 78)
    print("  RESUMEN FINAL DE EJECUCIÓN — SOFTWARE FJ")
    print("*" * 78)
    print(f"  Clientes en memoria:         {len(gestor.clientes)}")
    print(f"  Servicios en memoria:        {len(gestor.servicios)}")
    print(f"  Reservas en memoria:         {len(gestor.reservas)}")
    print(f"  Operaciones exitosas:        {gestor.operaciones_exitosas}")
    print(f"  Errores controlados (log):   {gestor.errores_controlados}")
    print(f"  Archivo de logs generado:    logs/software_fj.log")
    print("  Estado de la aplicación:     ACTIVA Y FINALIZADA SIN INTERRUPCIONES")
    print("*" * 78)
    logger.info(
        "Simulación finalizada sin interrupciones | Éxitos: %d | Errores controlados: %d",
        gestor.operaciones_exitosas,
        gestor.errores_controlados,
    )


# Punto de entrada estándar cuando se ejecuta el archivo directamente desde Python.
if __name__ == "__main__":
    try:
        # Ejecuta la simulación completa de las 14 operaciones.
        ejecutar_simulacion()
    except ErrorSoftwareFJ as error_fatal:
        # Red de seguridad de último nivel ante cualquier error del dominio no capturado.
        print(f"[ERROR CONTROLADO DE NIVEL SUPERIOR] {error_fatal}")