# -*- coding: utf-8 -*-
"""
Módulo que implementa la clase Cliente del sistema Software FJ.

Aplica Herencia (desde EntidadBase), Encapsulación (atributos privados con
propiedades y setters) y Validaciones estrictas sobre los datos personales.
"""

# Importa expresiones regulares para validar correos electrónicos y teléfonos.
import re
# Importa la clase abstracta base de la que hereda Cliente.
from src.entidad_base import EntidadBase
# Importa las excepciones personalizadas de validación y parámetros faltantes.
from src.excepciones import ErrorDatosInvalidos, ErrorParametroFaltante


class Cliente(EntidadBase):
    """
    Representa un cliente registrado en Software FJ con encapsulación de datos personales.
    """

    # Expresión regular compilada para validar correos electrónicos con formato estándar.
    __PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    # Expresión regular compilada para validar números telefónicos de 7 a 15 dígitos.
    __PATRON_TELEFONO = re.compile(r"^\+?\d{7,15}$")

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
        activo: bool = True,
    ) -> None:
        """
        Construye un cliente validando estrictamente todos sus datos personales.

        Parámetros:
            id_entidad (str): Código identificador del cliente (ej. 'CLI-001').
            nombre (str): Nombre completo del cliente.
            documento (str): Número de documento de identidad (6 a 15 dígitos).
            correo (str): Dirección de correo electrónico válida.
            telefono (str): Número de teléfono de contacto.
            activo (bool): Indica si el cliente está habilitado para realizar reservas.
        """
        # Invoca el constructor de EntidadBase para inicializar id_entidad y fecha_creacion.
        super().__init__(id_entidad)
        # Inicializa los atributos privados con valores vacíos antes de aplicar los setters.
        self.__nombre: str = ""
        self.__documento: str = ""
        self.__correo: str = ""
        self.__telefono: str = ""
        self.__activo: bool = True

        # Asigna cada propiedad pasando obligatoriamente por su setter con validación.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.activo = activo

        # Ejecuta la validación integral de la entidad al finalizar la construcción.
        self.validar()

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo encapsulado del cliente."""
        # Devuelve el atributo privado __nombre.
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre completo del cliente."""
        # Verifica que el nombre no haya sido omitido (None).
        if valor is None:
            raise ErrorParametroFaltante("El nombre del cliente es obligatorio y no puede ser None.")
        # Comprueba que sea texto y tenga al menos 3 caracteres útiles.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre del cliente debe ser un texto de al menos 3 caracteres.")
        # Verifica que el nombre no contenga dígitos numéricos.
        if any(caracter.isdigit() for caracter in valor):
            raise ErrorDatosInvalidos(f"El nombre del cliente no puede contener números: '{valor}'.")
        # Guarda el nombre normalizado eliminando espacios sobrantes.
        self.__nombre = " ".join(valor.strip().split())

    @property
    def documento(self) -> str:
        """Retorna el documento de identidad del cliente."""
        # Devuelve el atributo privado __documento.
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Valida y asigna el documento de identidad del cliente."""
        # Comprueba que el documento no sea None.
        if valor is None:
            raise ErrorParametroFaltante("El documento de identidad del cliente es obligatorio.")
        # Valida que sea una cadena compuesta únicamente por 6 a 15 dígitos.
        if not isinstance(valor, str) or not valor.strip().isdigit() or not (6 <= len(valor.strip()) <= 15):
            raise ErrorDatosInvalidos(
                f"El documento '{valor}' es inválido; debe contener entre 6 y 15 dígitos numéricos."
            )
        # Almacena el documento limpio en el atributo privado.
        self.__documento = valor.strip()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        # Devuelve el atributo privado __correo.
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida y asigna el correo electrónico del cliente."""
        # Verifica que el correo electrónico no haya sido omitido.
        if valor is None:
            raise ErrorParametroFaltante("El correo electrónico del cliente es obligatorio.")
        # Valida el tipo de dato y el formato mediante la expresión regular compilada.
        if not isinstance(valor, str) or not self.__PATRON_CORREO.match(valor.strip()):
            raise ErrorDatosInvalidos(f"El correo electrónico '{valor}' no tiene un formato válido.")
        # Almacena el correo normalizado en minúsculas.
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el número de teléfono del cliente."""
        # Devuelve el atributo privado __telefono.
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida y asigna el teléfono de contacto del cliente."""
        # Verifica que el teléfono no sea None.
        if valor is None:
            raise ErrorParametroFaltante("El teléfono del cliente es obligatorio.")
        # Elimina espacios o guiones comunes antes de comprobar el patrón numérico.
        limpio = valor.strip().replace(" ", "").replace("-", "") if isinstance(valor, str) else ""
        # Verifica que el teléfono cumpla con el patrón de 7 a 15 dígitos (opcionalmente con '+').
        if not isinstance(valor, str) or not self.__PATRON_TELEFONO.match(limpio):
            raise ErrorDatosInvalidos(
                f"El teléfono '{valor}' es inválido; debe tener entre 7 y 15 dígitos."
            )
        # Guarda el teléfono limpio en el atributo privado.
        self.__telefono = limpio

    @property
    def activo(self) -> bool:
        """Retorna True si el cliente está activo o False si está suspendido."""
        # Devuelve el estado booleano privado __activo.
        return self.__activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        """Valida y actualiza el estado de actividad del cliente."""
        # Verifica estrictamente que el valor sea de tipo booleano.
        if not isinstance(valor, bool):
            raise ErrorDatosInvalidos("El estado 'activo' del cliente debe ser un valor booleano.")
        # Asigna el nuevo estado de actividad.
        self.__activo = valor

    def validar(self) -> bool:
        """
        Sobrescribe el método abstracto de EntidadBase para confirmar que todos
        los atributos personales del cliente están completos y válidos.
        """
        # Verifica que ninguno de los campos principales esté vacío.
        if not all([self.__nombre, self.__documento, self.__correo, self.__telefono]):
            raise ErrorDatosInvalidos("Los datos personales del cliente están incompletos.")
        # Retorna True confirmando que la entidad es consistente.
        return True

    def obtener_resumen(self) -> str:
        """Sobrescribe el método abstracto para entregar un resumen legible del cliente."""
        # Determina la etiqueta textual del estado del cliente.
        estado = "Activo" if self.__activo else "Inactivo"
        # Construye y retorna la cadena formateada con los datos encapsulados.
        return (
            f"Cliente [{self.id_entidad}] {self.__nombre} | "
            f"Doc: {self.__documento} | Correo: {self.__correo} | "
            f"Tel: {self.__telefono} | Estado: {estado}"
        )