# -*- coding: utf-8 -*-
"""
Módulo de servicios de Software FJ.

Implementa:
- La clase abstracta Servicio (hereda de EntidadBase).
- Tres clases derivadas especializadas: ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
- Polimorfismo mediante sobrescritura de calcular_costo(), describir_servicio() y validar_parametros().
- Sobrecarga de métodos en calcular_costo() soportando múltiples combinaciones de parámetros
  (base, con impuesto, con descuento y con cargo adicional).
"""

# Importa abstractmethod para obligar a las subclases a sobrescribir los métodos clave.
from abc import abstractmethod
# Importa Optional y overload para documentar formalmente la sobrecarga de métodos en Python.
from typing import Optional, overload
# Importa la clase abstracta base EntidadBase.
from src.entidad_base import EntidadBase
# Importa las excepciones personalizadas del sistema.
from src.excepciones import (
    ErrorCalculoInconsistente,
    ErrorDatosInvalidos,
    ErrorParametroFaltante,
)


class Servicio(EntidadBase):
    """
    Clase abstracta que modela un servicio genérico ofrecido por Software FJ.
    """

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True,
    ) -> None:
        """
        Inicializa los atributos comunes a todos los servicios.

        Parámetros:
            id_entidad (str): Código único del servicio (ej. 'SRV-001').
            nombre (str): Nombre descriptivo del servicio.
            tarifa_base (float): Tarifa por hora en pesos colombianos (COP).
            disponible (bool): Indica si el servicio puede ser reservado actualmente.
        """
        # Llama al constructor de EntidadBase para validar y guardar id_entidad y fecha_creacion.
        super().__init__(id_entidad)
        # Inicializa los atributos privados con valores por defecto antes de usar los setters.
        self.__nombre: str = ""
        self.__tarifa_base: float = 0.0
        self.__disponible: bool = True

        # Asigna los atributos mediante sus propiedades validadas.
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        # Devuelve el atributo privado __nombre.
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del servicio."""
        # Comprueba que el nombre no haya sido omitido.
        if valor is None:
            raise ErrorParametroFaltante("El nombre del servicio es obligatorio.")
        # Valida que sea un texto de al menos 3 caracteres.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre del servicio debe tener al menos 3 caracteres.")
        # Almacena el nombre limpio.
        self.__nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por hora del servicio."""
        # Devuelve el atributo privado __tarifa_base.
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida y asigna la tarifa base por hora (debe ser estrictamente positiva)."""
        # Verifica que la tarifa no sea None.
        if valor is None:
            raise ErrorParametroFaltante("La tarifa base del servicio es obligatoria.")
        # Valida que sea un número real (excluyendo booleanos) y mayor que cero.
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise ErrorDatosInvalidos(f"La tarifa base '{valor}' debe ser un número mayor que cero.")
        # Almacena la tarifa convertida a float.
        self.__tarifa_base = float(valor)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para reserva."""
        # Devuelve el estado privado __disponible.
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Valida y actualiza la disponibilidad del servicio."""
        # Exige estrictamente un valor booleano.
        if not isinstance(valor, bool):
            raise ErrorDatosInvalidos("La disponibilidad del servicio debe ser booleana (True/False).")
        # Actualiza el atributo privado.
        self.__disponible = valor

    def _aplicar_ajustes_financieros(
        self,
        subtotal: float,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float:
        """
        Método protegido compartido que aplica descuentos, cargos adicionales e impuestos
        para soportar las variantes sobrecargadas de calcular_costo().
        """
        # Verifica que el subtotal base calculado por la subclase sea positivo.
        if subtotal <= 0:
            raise ErrorCalculoInconsistente(
                f"El subtotal base ({subtotal}) no puede ser menor o igual a cero."
            )

        # Inicia el cálculo partiendo del subtotal base.
        total = subtotal

        # Si se especificó descuento, valida que esté entre 0 y menor a 1 (0% a <100%).
        if descuento is not None:
            if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
                raise ErrorCalculoInconsistente("El descuento debe ser un valor numérico.")
            if descuento < 0 or descuento >= 1:
                raise ErrorCalculoInconsistente(
                    f"Descuento inconsistente ({descuento * 100:.1f}%): debe estar entre 0% y menos de 100%."
                )
            # Aplica la reducción proporcional por descuento.
            total -= total * descuento

        # Si se especificó un cargo adicional, valida que no sea negativo.
        if cargo_extra is not None:
            if isinstance(cargo_extra, bool) or not isinstance(cargo_extra, (int, float)):
                raise ErrorCalculoInconsistente("El cargo adicional debe ser un valor numérico.")
            if cargo_extra < 0:
                raise ErrorCalculoInconsistente(
                    f"Cargo adicional inconsistente ({cargo_extra}): no puede ser negativo."
                )
            # Suma el cargo adicional al monto acumulado.
            total += cargo_extra

        # Si se especificó tasa de impuesto (ej. IVA 0.19), valida que esté entre 0 y 0.50.
        if tasa_impuesto is not None:
            if isinstance(tasa_impuesto, bool) or not isinstance(tasa_impuesto, (int, float)):
                raise ErrorCalculoInconsistente("La tasa de impuesto debe ser un valor numérico.")
            if tasa_impuesto < 0 or tasa_impuesto > 0.50:
                raise ErrorCalculoInconsistente(
                    f"Tasa de impuesto inconsistente ({tasa_impuesto * 100:.1f}%): debe estar entre 0% y 50%."
                )
            # Incrementa el total con el impuesto correspondiente.
            total += total * tasa_impuesto

        # Verificación final de consistencia: el costo final nunca puede ser <= 0.
        if total <= 0:
            raise ErrorCalculoInconsistente("El cálculo final arrojó un monto no positivo.")

        # Retorna el valor redondeado a dos decimales.
        return round(total, 2)

    # --- Declaraciones formales de sobrecarga de calcular_costo() ---
    @overload
    def calcular_costo(self, duracion: int) -> float: ...

    @overload
    def calcular_costo(self, duracion: int, tasa_impuesto: float) -> float: ...

    @overload
    def calcular_costo(self, duracion: int, tasa_impuesto: float, descuento: float) -> float: ...

    @overload
    def calcular_costo(
        self,
        duracion: int,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float: ...

    @abstractmethod
    def calcular_costo(
        self,
        duracion: int,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float:
        """
        Método abstracto y sobrecargado que calcula el costo total del servicio según
        la duración y parámetros opcionales (impuesto, descuento, cargo adicional).
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto que devuelve la descripción detallada propia de cada servicio."""
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Método abstracto que valida los parámetros específicos de cada tipo de servicio."""
        pass

    def validar(self) -> bool:
        """Implementa EntidadBase.validar() delegando en la validación específica del servicio."""
        # Invoca el método polimórfico validar_parametros() de la subclase concreta.
        return self.validar_parametros()

    def obtener_resumen(self) -> str:
        """Implementa EntidadBase.obtener_resumen() usando la descripción polimórfica."""
        # Determina la etiqueta textual de disponibilidad.
        estado = "Disponible" if self.__disponible else "No disponible"
        # Retorna el identificador, la descripción específica y la disponibilidad actual.
        return f"Servicio [{self.id_entidad}] {self.describir_servicio()} | Estado: {estado}"


class ReservaSala(Servicio):
    """
    Servicio especializado para la reserva de salas de reuniones o auditorios.
    """

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        incluye_audiovisual: bool = False,
        disponible: bool = True,
    ) -> None:
        """
        Inicializa una sala reservable con capacidad de personas y opción audiovisual.
        """
        # Invoca el constructor de la clase abstracta Servicio.
        super().__init__(id_entidad, nombre, tarifa_base, disponible)
        # Almacena la capacidad máxima de asistentes como atributo privado.
        self.__capacidad: int = capacidad
        # Almacena si la sala incluye equipamiento audiovisual (proyector y sonido).
        self.__incluye_audiovisual: bool = incluye_audiovisual
        # Ejecuta la validación específica de los parámetros de la sala.
        self.validar_parametros()

    @property
    def capacidad(self) -> int:
        """Retorna la capacidad máxima de personas de la sala."""
        # Devuelve el atributo privado __capacidad.
        return self.__capacidad

    @property
    def incluye_audiovisual(self) -> bool:
        """Indica si la sala cuenta con equipo audiovisual incluido."""
        # Devuelve el atributo privado __incluye_audiovisual.
        return self.__incluye_audiovisual

    def validar_parametros(self) -> bool:
        """Sobrescribe validar_parametros() verificando capacidad y bandera audiovisual."""
        # Comprueba que la capacidad sea un entero entre 2 y 200 personas.
        if isinstance(self.__capacidad, bool) or not isinstance(self.__capacidad, int) or not (2 <= self.__capacidad <= 200):
            raise ErrorDatosInvalidos(
                f"La capacidad de la sala ({self.__capacidad}) debe ser un entero entre 2 y 200 personas."
            )
        # Verifica que incluye_audiovisual sea booleano.
        if not isinstance(self.__incluye_audiovisual, bool):
            raise ErrorDatosInvalidos("El indicador 'incluye_audiovisual' debe ser booleano.")
        # Retorna True si todos los parámetros son válidos.
        return True

    def calcular_costo(
        self,
        duracion: int,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float:
        """
        Calcula el costo de la reserva de sala (sobrescrito y sobrecargado).
        Añade un recargo fijo de $35.000 COP si incluye equipo audiovisual.
        """
        # Valida que la duración en horas sea un entero positivo.
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ErrorCalculoInconsistente("La duración en horas debe ser un entero mayor que cero.")
        # Calcula el costo base multiplicando tarifa por horas.
        subtotal = self.tarifa_base * duracion
        # Si incluye equipo audiovisual, suma el recargo técnico correspondiente.
        if self.__incluye_audiovisual:
            subtotal += 35000.0
        # Aplica las variantes sobrecargadas (descuento, cargo extra e impuesto) y retorna el total.
        return self._aplicar_ajustes_financieros(subtotal, tasa_impuesto, descuento, cargo_extra)

    def describir_servicio(self) -> str:
        """Sobrescribe describir_servicio() con los detalles propios de una sala."""
        # Define el texto del equipamiento audiovisual.
        av = "con equipo audiovisual (+$35,000)" if self.__incluye_audiovisual else "sin equipo audiovisual"
        # Retorna la descripción estructurada de la sala.
        return (
            f"Sala '{self.nombre}' | Capacidad: {self.__capacidad} personas | "
            f"Tarifa: ${self.tarifa_base:,.0f}/h | {av}"
        )


class AlquilerEquipo(Servicio):
    """
    Servicio especializado para el alquiler de equipos tecnológicos (portátiles, proyectores, etc.).
    """

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        categoria_equipo: str,
        cantidad_unidades: int,
        seguro_incluido: bool = True,
        disponible: bool = True,
    ) -> None:
        """
        Inicializa un servicio de alquiler de equipos con categoría, cantidad y seguro.
        """
        # Llama al constructor de la clase abstracta Servicio.
        super().__init__(id_entidad, nombre, tarifa_base, disponible)
        # Guarda la categoría tecnológica del equipo.
        self.__categoria_equipo: str = categoria_equipo
        # Guarda el número de unidades a alquilar.
        self.__cantidad_unidades: int = cantidad_unidades
        # Guarda si el alquiler incluye seguro contra daños.
        self.__seguro_incluido: bool = seguro_incluido
        # Valida los parámetros propios del alquiler de equipos.
        self.validar_parametros()

    @property
    def categoria_equipo(self) -> str:
        """Retorna la categoría del equipo alquilado."""
        # Devuelve el atributo privado __categoria_equipo.
        return self.__categoria_equipo

    @property
    def cantidad_unidades(self) -> int:
        """Retorna la cantidad de unidades incluidas en el alquiler."""
        # Devuelve el atributo privado __cantidad_unidades.
        return self.__cantidad_unidades

    def validar_parametros(self) -> bool:
        """Sobrescribe validar_parametros() validando categoría, unidades y seguro."""
        # Verifica que la categoría de equipo no sea nula ni vacía.
        if not isinstance(self.__categoria_equipo, str) or not self.__categoria_equipo.strip():
            raise ErrorDatosInvalidos("La categoría del equipo debe ser un texto no vacío.")
        # Valida que la cantidad de unidades sea un entero entre 1 y 50.
        if isinstance(self.__cantidad_unidades, bool) or not isinstance(self.__cantidad_unidades, int) or not (1 <= self.__cantidad_unidades <= 50):
            raise ErrorDatosInvalidos(
                f"La cantidad de unidades ({self.__cantidad_unidades}) debe ser un entero entre 1 y 50."
            )
        # Verifica que el indicador de seguro sea booleano.
        if not isinstance(self.__seguro_incluido, bool):
            raise ErrorDatosInvalidos("El parámetro 'seguro_incluido' debe ser booleano.")
        # Retorna True al superar todas las validaciones.
        return True

    def calcular_costo(
        self,
        duracion: int,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float:
        """
        Calcula el costo del alquiler multiplicando tarifa x duración x unidades,
        más un 8% de seguro si está activado.
        """
        # Valida que la duración sea un entero positivo.
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ErrorCalculoInconsistente("La duración del alquiler debe ser un entero mayor que cero.")
        # Calcula el subtotal base multiplicando tarifa, horas y cantidad de equipos.
        subtotal = self.tarifa_base * duracion * self.__cantidad_unidades
        # Si el seguro contra daños está incluido, añade el 8% sobre el subtotal.
        if self.__seguro_incluido:
            subtotal *= 1.08
        # Aplica los parámetros sobrecargados y retorna el valor final.
        return self._aplicar_ajustes_financieros(subtotal, tasa_impuesto, descuento, cargo_extra)

    def describir_servicio(self) -> str:
        """Sobrescribe describir_servicio() detallando el equipo, unidades y seguro."""
        # Define el texto correspondiente al seguro.
        seguro = "con seguro (+8%)" if self.__seguro_incluido else "sin seguro"
        # Retorna la descripción completa del alquiler.
        return (
            f"Alquiler '{self.nombre}' ({self.__categoria_equipo}) | "
            f"Unidades: {self.__cantidad_unidades} | Tarifa: ${self.tarifa_base:,.0f}/h c/u | {seguro}"
        )


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado de consultoría técnica o asesoría profesional en ingeniería.
    """

    # Conjunto de niveles de complejidad admitidos con su multiplicador de tarifa.
    __FACTORES_NIVEL = {
        "BASICO": 1.0,
        "INTERMEDIO": 1.25,
        "AVANZADO": 1.50,
    }

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        tarifa_base: float,
        area_especialidad: str,
        nivel_complejidad: str = "INTERMEDIO",
        modalidad: str = "VIRTUAL",
        disponible: bool = True,
    ) -> None:
        """
        Inicializa una asesoría especializada con área, complejidad y modalidad.
        """
        # Invoca el constructor de la clase abstracta Servicio.
        super().__init__(id_entidad, nombre, tarifa_base, disponible)
        # Guarda el área técnica de la asesoría (ej. Arquitectura de Software, Ciberseguridad).
        self.__area_especialidad: str = area_especialidad
        # Normaliza y guarda el nivel de complejidad.
        self.__nivel_complejidad: str = nivel_complejidad.strip().upper() if isinstance(nivel_complejidad, str) else ""
        # Normaliza y guarda la modalidad (VIRTUAL o PRESENCIAL).
        self.__modalidad: str = modalidad.strip().upper() if isinstance(modalidad, str) else ""
        # Ejecuta la validación específica de los parámetros de la asesoría.
        self.validar_parametros()

    @property
    def area_especialidad(self) -> str:
        """Retorna el área temática de la asesoría."""
        # Devuelve el atributo privado __area_especialidad.
        return self.__area_especialidad

    @property
    def nivel_complejidad(self) -> str:
        """Retorna el nivel de complejidad técnica de la asesoría."""
        # Devuelve el atributo privado __nivel_complejidad.
        return self.__nivel_complejidad

    @property
    def modalidad(self) -> str:
        """Retorna la modalidad de prestación (VIRTUAL o PRESENCIAL)."""
        # Devuelve el atributo privado __modalidad.
        return self.__modalidad

    def validar_parametros(self) -> bool:
        """Sobrescribe validar_parametros() comprobando área, nivel y modalidad."""
        # Verifica que el área de especialidad sea una cadena no vacía.
        if not isinstance(self.__area_especialidad, str) or not self.__area_especialidad.strip():
            raise ErrorDatosInvalidos("El área de especialidad de la asesoría es obligatoria.")
        # Valida que el nivel de complejidad pertenezca al catálogo permitido.
        if self.__nivel_complejidad not in self.__FACTORES_NIVEL:
            raise ErrorDatosInvalidos(
                f"Nivel de complejidad '{self.__nivel_complejidad}' inválido; "
                f"use uno de: {', '.join(self.__FACTORES_NIVEL.keys())}."
            )
        # Valida que la modalidad sea VIRTUAL o PRESENCIAL.
        if self.__modalidad not in {"VIRTUAL", "PRESENCIAL"}:
            raise ErrorDatosInvalidos(
                f"Modalidad '{self.__modalidad}' inválida; debe ser 'VIRTUAL' o 'PRESENCIAL'."
            )
        # Retorna True al confirmar la validez de los parámetros.
        return True

    def calcular_costo(
        self,
        duracion: int,
        tasa_impuesto: Optional[float] = None,
        descuento: Optional[float] = None,
        cargo_extra: Optional[float] = None,
    ) -> float:
        """
        Calcula el costo de la asesoría aplicando el factor de complejidad
        y un recargo de viáticos ($25.000 COP) si la modalidad es PRESENCIAL.
        """
        # Verifica que la duración sea un entero positivo.
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ErrorCalculoInconsistente("La duración de la asesoría debe ser un entero mayor que cero.")
        # Obtiene el multiplicador correspondiente al nivel de complejidad.
        factor = self.__FACTORES_NIVEL[self.__nivel_complejidad]
        # Calcula el subtotal base ajustado por complejidad.
        subtotal = self.tarifa_base * duracion * factor
        # Si la modalidad es presencial, añade el costo logístico de desplazamiento.
        if self.__modalidad == "PRESENCIAL":
            subtotal += 25000.0
        # Aplica los parámetros sobrecargados y retorna el total final.
        return self._aplicar_ajustes_financieros(subtotal, tasa_impuesto, descuento, cargo_extra)

    def describir_servicio(self) -> str:
        """Sobrescribe describir_servicio() con los detalles técnicos de la asesoría."""
        # Construye y retorna la descripción legible de la asesoría especializada.
        return (
            f"Asesoría '{self.nombre}' | Área: {self.__area_especialidad} | "
            f"Nivel: {self.__nivel_complejidad} | Modalidad: {self.__modalidad} | "
            f"Tarifa base: ${self.tarifa_base:,.0f}/h"
        )