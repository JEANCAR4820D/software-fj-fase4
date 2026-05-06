"""
==============================================================================
  UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
  Escuela de Ciencias Básicas, Tecnología e Ingeniería - ECBTI
  Curso: Programación (213023)
  Fase 4 - Componente práctico - Prácticas simuladas
------------------------------------------------------------------------------
  Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
  Empresa:  Software FJ
------------------------------------------------------------------------------
  Implementa los principios de Programación Orientada a Objetos:
    * Abstracción     -> Clases abstractas EntidadBase y Servicio
    * Herencia        -> Cliente, ReservaSala, AlquilerEquipo, AsesoriaTecnica
    * Polimorfismo    -> Métodos sobrescritos calcular_costo() y descripcion()
    * Encapsulación   -> Atributos privados con properties (getters/setters)
    * Sobrecarga      -> calcular_costo_total() con parámetros opcionales
  Manejo avanzado de excepciones:
    * Excepciones personalizadas
    * try/except, try/except/else, try/except/finally
    * Encadenamiento de excepciones (raise ... from ...)
    * Registro de eventos y errores en archivo de logs
==============================================================================
"""

# ============================================================================
#  IMPORTACIÓN DE MÓDULOS ESTÁNDAR DE PYTHON
# ============================================================================
import re                       # Para validar formatos con expresiones regulares
import logging                  # Para el sistema de registro (logs)
from abc import ABC, abstractmethod  # Para definir clases y métodos abstractos
from datetime import datetime   # Para registrar fechas y horas de eventos


# ============================================================================
#  MÓDULO 1: CONFIGURACIÓN DEL SISTEMA DE LOGS
#  Estudiante asignado: Manejo de errores y logs
# ============================================================================
# Se configura el logger para registrar TODOS los eventos del sistema
# (informativos, advertencias y errores) en el archivo "software_fj.log".
# El formato incluye fecha/hora, nivel de severidad y mensaje descriptivo.
logging.basicConfig(
    filename="software_fj.log",         # Archivo donde se almacenan los registros
    level=logging.INFO,                 # Nivel mínimo a registrar (INFO en adelante)
    format="%(asctime)s | %(levelname)s | %(message)s",  # Formato del log
    datefmt="%Y-%m-%d %H:%M:%S",        # Formato de la fecha
    encoding="utf-8"                    # Codificación para caracteres en español
)
# Se obtiene una referencia al logger raíz para usar en todo el proyecto
logger = logging.getLogger("SoftwareFJ")


# ============================================================================
#  MÓDULO 2: EXCEPCIONES PERSONALIZADAS
#  Estudiante asignado: Manejo de errores y logs
# ============================================================================
# Jerarquía de excepciones propias del dominio de negocio. Heredan de
# Exception y permiten capturar errores específicos del sistema sin
# interferir con excepciones nativas de Python.

class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato proporcionado no cumple las reglas de validación
    (por ejemplo, un correo mal formado o un documento vacío)."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando un parámetro obligatorio no fue proporcionado."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible
    (por ejemplo, una sala ya ocupada o un equipo agotado)."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando se intenta crear una reserva con datos inconsistentes
    (duración cero, cliente inexistente, etc.)."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce resultados imposibles
    (valores negativos, descuentos mayores al 100%, etc.)."""
    pass


# ============================================================================
#  MÓDULO 3: CLASE ABSTRACTA BASE - EntidadBase
#  Estudiante asignado: Integración final / arquitectura
# ============================================================================
# Representa cualquier entidad general del sistema. Define el contrato
# (métodos abstractos) que todas las entidades concretas deben implementar.

class EntidadBase(ABC):
    """Clase abstracta que representa una entidad genérica del sistema.

    Atributos:
        _id (str): identificador único de la entidad (encapsulado).
        _fecha_creacion (datetime): fecha y hora de creación.
    """

    def __init__(self, identificador: str):
        # Validación inmediata del identificador para evitar entidades inválidas
        if not identificador or not isinstance(identificador, str):
            raise DatoInvalidoError("El identificador no puede estar vacío.")
        self._id = identificador
        self._fecha_creacion = datetime.now()

    # --- Propiedades encapsuladas (lectura controlada) ---
    @property
    def id(self) -> str:
        """Devuelve el identificador único de la entidad."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Devuelve la fecha de creación de la entidad."""
        return self._fecha_creacion

    # --- Métodos abstractos (deben implementarse en subclases) ---
    @abstractmethod
    def descripcion(self) -> str:
        """Retorna una descripción textual de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida la integridad de los datos de la entidad."""
        pass


# ============================================================================
#  MÓDULO 4: CLASE Cliente
#  Estudiante asignado: Clase Cliente
# ============================================================================
# Representa a un cliente de Software FJ. Encapsula sus datos personales
# y aplica validaciones rigurosas (formato de correo, teléfono, documento).

class Cliente(EntidadBase):
    """Cliente registrado en el sistema.

    Atributos privados:
        __nombre (str)
        __documento (str)
        __email (str)
        __telefono (str)
    """

    # Patrones de expresiones regulares para validar formatos
    _PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\d{7,10}$")
    _PATRON_DOCUMENTO = re.compile(r"^\d{6,12}$")

    def __init__(self, identificador: str, nombre: str,
                 documento: str, email: str, telefono: str):
        # Llama al constructor de la clase padre (asigna id y fecha)
        super().__init__(identificador)
        # Asignación a través de los setters para forzar validaciones
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        logger.info(f"Cliente creado correctamente: {self._id} - {self.__nombre}")

    # ---------- Encapsulación: getters y setters con validación ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError(
                "El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        if not self._PATRON_DOCUMENTO.match(str(valor)):
            raise DatoInvalidoError(
                f"Documento inválido '{valor}'. Debe contener entre 6 y 12 dígitos.")
        self.__documento = valor

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not self._PATRON_EMAIL.match(str(valor)):
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self.__email = valor

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not self._PATRON_TELEFONO.match(str(valor)):
            raise DatoInvalidoError(
                f"Teléfono inválido '{valor}'. Debe contener entre 7 y 10 dígitos.")
        self.__telefono = valor

    # ---------- Implementación de métodos abstractos ----------
    def descripcion(self) -> str:
        """Devuelve una descripción legible del cliente."""
        return (f"Cliente[{self._id}] {self.__nombre} | "
                f"Doc: {self.__documento} | Email: {self.__email}")

    def validar(self) -> bool:
        """Verifica que todos los campos del cliente sean coherentes."""
        # Si los setters validaron correctamente, los datos están bien.
        return bool(self.__nombre and self.__documento
                    and self.__email and self.__telefono)


# ============================================================================
#  MÓDULO 5: CLASE ABSTRACTA Servicio Y SUS ESPECIALIZACIONES
#  Estudiante asignado: Clase Servicios
# ============================================================================
# Servicio es una clase abstracta que define el comportamiento común a
# todos los servicios ofrecidos por Software FJ. Cada servicio concreto
# implementa polimórficamente sus propios métodos de cálculo y descripción.

class Servicio(EntidadBase):
    """Clase abstracta que representa cualquier servicio ofertado."""

    def __init__(self, identificador: str, nombre: str,
                 tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        # Validación de la tarifa base
        if tarifa_base <= 0:
            raise DatoInvalidoError(
                f"La tarifa base debe ser positiva (recibido: {tarifa_base}).")
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible
        # Nota: el log de creación se realiza desde cada subclase, una vez
        # que sus atributos específicos (capacidad, stock, área...) ya
        # fueron asignados, para que descripcion() funcione correctamente.

    # ---------- Propiedades comunes ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    # ---------- Métodos abstractos: cada servicio los redefine ----------
    @abstractmethod
    def calcular_costo(self, duracion: float) -> float:
        """Calcula el costo del servicio en función de la duración."""
        pass

    # ---------- Sobrecarga de métodos mediante parámetros opcionales ----------
    def calcular_costo_total(self, duracion: float,
                             impuesto: float = 0.19,
                             descuento: float = 0.0) -> float:
        """Calcula el costo total aplicando impuesto y descuento opcionales.

        Esta es una versión "sobrecargada" del cálculo base. En Python la
        sobrecarga clásica se simula con parámetros con valores por defecto.

        Argumentos:
            duracion (float): horas o unidades del servicio.
            impuesto (float): porcentaje de IVA (por defecto 19%).
            descuento (float): porcentaje de descuento (por defecto 0%).
        """
        # Validaciones de cordura sobre los parámetros recibidos
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                f"El descuento debe estar entre 0 y 1 (recibido: {descuento}).")
        if impuesto < 0:
            raise CalculoInconsistenteError(
                f"El impuesto no puede ser negativo (recibido: {impuesto}).")

        # Se delega el cálculo base al método polimórfico de la subclase
        costo_base = self.calcular_costo(duracion)
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)

        # Validación final del resultado
        if costo_final < 0:
            raise CalculoInconsistenteError(
                "El costo final calculado es negativo.")
        return round(costo_final, 2)

    # ---------- Implementación de validar() ----------
    def validar(self) -> bool:
        return bool(self._nombre) and self._tarifa_base > 0


# --------- Servicios especializados (3 subclases concretas) -----------------

class ReservaSala(Servicio):
    """Servicio de reserva de salas de reunión por horas."""

    def __init__(self, identificador, nombre, tarifa_base,
                 capacidad: int, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser positiva.")
        self._capacidad = capacidad
        logger.info(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion: float) -> float:
        # Para salas el costo es lineal: tarifa * horas
        if duracion <= 0:
            raise DatoInvalidoError("La duración debe ser mayor que cero.")
        return self._tarifa_base * duracion

    def descripcion(self) -> str:
        return (f"[Sala {self._id}] {self._nombre} | Capacidad: "
                f"{self._capacidad} personas | Tarifa: ${self._tarifa_base}/h")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos por días."""

    def __init__(self, identificador, nombre, tarifa_base,
                 stock: int, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if stock < 0:
            raise DatoInvalidoError("El stock no puede ser negativo.")
        self._stock = stock
        logger.info(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion: float) -> float:
        # El costo del alquiler aplica un recargo del 10% si supera 7 días
        if duracion <= 0:
            raise DatoInvalidoError("Los días de alquiler deben ser positivos.")
        recargo = 1.10 if duracion > 7 else 1.0
        return self._tarifa_base * duracion * recargo

    def descripcion(self) -> str:
        return (f"[Equipo {self._id}] {self._nombre} | Stock: {self._stock} | "
                f"Tarifa: ${self._tarifa_base}/día")

    def reducir_stock(self):
        """Decrementa el inventario al reservar una unidad."""
        if self._stock <= 0:
            raise ServicioNoDisponibleError(
                f"No hay stock disponible para el equipo '{self._nombre}'.")
        self._stock -= 1


class AsesoriaTecnica(Servicio):
    """Servicio de asesoría especializada cobrada por hora con tarifa premium."""

    def __init__(self, identificador, nombre, tarifa_base,
                 area_experticia: str, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not area_experticia:
            raise ParametroFaltanteError("Debe indicar el área de experticia.")
        self._area = area_experticia
        logger.info(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion: float) -> float:
        # Asesoría: a partir de 5 horas se cobra una tarifa premium del 20%
        if duracion <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser > 0.")
        factor = 1.20 if duracion >= 5 else 1.0
        return self._tarifa_base * duracion * factor

    def descripcion(self) -> str:
        return (f"[Asesoría {self._id}] {self._nombre} | Área: {self._area} | "
                f"Tarifa: ${self._tarifa_base}/h")


# ============================================================================
#  MÓDULO 6: CLASE Reserva
#  Estudiante asignado: Clase Reservas
# ============================================================================

class Reserva:
    """Representa una reserva que vincula un cliente con un servicio."""

    # Estados válidos del ciclo de vida de la reserva
    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, identificador: str, cliente: Cliente,
                 servicio: Servicio, duracion: float):
        # Validaciones iniciales y específicas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere un objeto Servicio válido.")
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor que cero.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible.")

        self._id = identificador
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._fecha_reserva = datetime.now()
        logger.info(f"Reserva {self._id} creada para "
                    f"{cliente.nombre} -> {servicio.nombre}")

    # ---------- Propiedades de solo lectura ----------
    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    # ---------- Operaciones con manejo de excepciones ----------
    def confirmar(self):
        """Cambia el estado de la reserva a CONFIRMADA usando try/except/else."""
        try:
            if self._estado != "PENDIENTE":
                raise ReservaInvalidaError(
                    f"No se puede confirmar una reserva en estado '{self._estado}'.")
        except ReservaInvalidaError as e:
            # Se registra el error y se relanza para que el llamador lo gestione
            logger.error(f"Error al confirmar reserva {self._id}: {e}")
            raise
        else:
            # Si no hubo excepción, se confirma efectivamente
            self._estado = "CONFIRMADA"
            logger.info(f"Reserva {self._id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si aún no ha sido procesada."""
        if self._estado == "PROCESADA":
            raise ReservaInvalidaError(
                "No se puede cancelar una reserva ya procesada.")
        self._estado = "CANCELADA"
        logger.info(f"Reserva {self._id} cancelada.")

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Procesa la reserva: calcula el costo total y actualiza el estado.

        Demuestra el uso de try/except/finally y el encadenamiento de
        excepciones con `raise ... from ...`.
        """
        costo_total = 0.0
        try:
            if self._estado != "CONFIRMADA":
                raise ReservaInvalidaError(
                    "Solo se pueden procesar reservas confirmadas.")
            # Cálculo polimórfico: cada servicio implementa el suyo
            costo_total = self._servicio.calcular_costo_total(
                self._duracion, impuesto, descuento)
            # Si es alquiler, se descuenta del stock
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.reducir_stock()
            self._estado = "PROCESADA"
        except CalculoInconsistenteError as e:
            # Encadenamiento: se lanza una nueva excepción preservando la causa
            logger.error(f"Error de cálculo en reserva {self._id}: {e}")
            raise ReservaInvalidaError(
                "No se pudo procesar la reserva por un cálculo inválido.") from e
        except SoftwareFJError as e:
            logger.error(f"Error procesando reserva {self._id}: {e}")
            raise
        finally:
            # El bloque finally se ejecuta siempre (con o sin error)
            logger.info(f"Intento de procesamiento finalizado para reserva "
                        f"{self._id} | estado actual: {self._estado}")
        return costo_total

    def __str__(self) -> str:
        return (f"Reserva[{self._id}] Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | "
                f"Duración: {self._duracion} | Estado: {self._estado}")


# ============================================================================
#  MÓDULO 7: GESTOR PRINCIPAL DEL SISTEMA
#  Estudiante asignado: Integración final
# ============================================================================
# El gestor centraliza el manejo de listas internas (clientes, servicios,
# reservas) y expone operaciones de alto nivel con manejo de errores.

class GestorSoftwareFJ:
    """Coordinador central del sistema. Mantiene listas internas en memoria."""

    def __init__(self):
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        logger.info("Gestor SoftwareFJ inicializado correctamente.")

    # ---------- Registro de clientes ----------
    def registrar_cliente(self, cliente: Cliente):
        try:
            if any(c.documento == cliente.documento for c in self._clientes):
                raise DatoInvalidoError(
                    f"Ya existe un cliente con documento {cliente.documento}.")
            self._clientes.append(cliente)
            logger.info(f"Cliente {cliente.id} registrado en el sistema.")
        except SoftwareFJError as e:
            logger.error(f"No se pudo registrar el cliente: {e}")
            raise

    # ---------- Registro de servicios ----------
    def registrar_servicio(self, servicio: Servicio):
        self._servicios.append(servicio)
        logger.info(f"Servicio {servicio.id} registrado en el sistema.")

    # ---------- Creación de reservas ----------
    def crear_reserva(self, identificador: str, cliente: Cliente,
                      servicio: Servicio, duracion: float) -> Reserva:
        reserva = Reserva(identificador, cliente, servicio, duracion)
        self._reservas.append(reserva)
        return reserva

    # ---------- Consultas ----------
    def listar_clientes(self):
        return list(self._clientes)

    def listar_servicios(self):
        return list(self._servicios)

    def listar_reservas(self):
        return list(self._reservas)


# ============================================================================
#  MÓDULO 8: SIMULACIÓN DE 10 OPERACIONES COMPLETAS
#  Estudiante asignado: Integración final / pruebas
# ============================================================================
# Se ejecutan al menos 10 operaciones que combinan registros válidos e
# inválidos, demostrando que el sistema continúa estable ante errores.

def ejecutar_simulacion():
    """Ejecuta una batería de 10 operaciones simuladas con casos
    correctos e incorrectos para demostrar la robustez del sistema."""

    print("=" * 70)
    print("   SISTEMA SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print("=" * 70)

    gestor = GestorSoftwareFJ()
    contador_exitosos = 0
    contador_fallidos = 0

    # --- OPERACIÓN 1: Registro válido de cliente ---
    print("\n[1] Registro de cliente VÁLIDO")
    try:
        c1 = Cliente("CLI001", "Ana María Pérez", "1023456789",
                     "ana.perez@correo.com", "3001234567")
        gestor.registrar_cliente(c1)
        print(f"    OK -> {c1.descripcion()}")
        contador_exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 2: Registro de cliente con email INVÁLIDO ---
    print("\n[2] Registro de cliente con email INVÁLIDO")
    try:
        c_malo = Cliente("CLI002", "Pedro López", "1099887766",
                         "correo_invalido", "3110000000")
        gestor.registrar_cliente(c_malo)
        contador_exitosos += 1
    except DatoInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 3: Registro válido de cliente adicional ---
    print("\n[3] Registro de segundo cliente VÁLIDO")
    try:
        c2 = Cliente("CLI003", "Carlos Rodríguez", "1075432198",
                     "carlos.r@empresa.co", "3157654321")
        gestor.registrar_cliente(c2)
        print(f"    OK -> {c2.descripcion()}")
        contador_exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 4: Creación de servicio con tarifa INVÁLIDA ---
    print("\n[4] Creación de servicio con tarifa INVÁLIDA (negativa)")
    try:
        sala_mala = ReservaSala("SAL999", "Sala Fantasma", -5000, 10)
        gestor.registrar_servicio(sala_mala)
        contador_exitosos += 1
    except DatoInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 5: Creación correcta de los tres tipos de servicios ---
    print("\n[5] Creación VÁLIDA de tres servicios especializados")
    try:
        sala = ReservaSala("SAL001", "Sala Ejecutiva", 50000, 12)
        equipo = AlquilerEquipo("EQU001", "Proyector 4K", 80000, stock=2)
        asesoria = AsesoriaTecnica("ASE001", "Consultoría Cloud",
                                   120000, "AWS / Azure")
        for s in (sala, equipo, asesoria):
            gestor.registrar_servicio(s)
            print(f"    OK -> {s.descripcion()}")
        contador_exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 6: Reserva exitosa de sala ---
    print("\n[6] Reserva EXITOSA de sala con confirmación y procesamiento")
    try:
        r1 = gestor.crear_reserva("RES001", c1, sala, duracion=3)
        r1.confirmar()
        costo = r1.procesar(impuesto=0.19, descuento=0.10)
        print(f"    OK -> {r1} | Costo total: ${costo:,.2f}")
        contador_exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 7: Reserva con duración INVÁLIDA ---
    print("\n[7] Intento de reserva con duración INVÁLIDA (cero)")
    try:
        gestor.crear_reserva("RES002", c2, asesoria, duracion=0)
        contador_exitosos += 1
    except ReservaInvalidaError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 8: Reserva de asesoría con cálculo premium ---
    print("\n[8] Reserva de asesoría con tarifa PREMIUM (5+ horas)")
    try:
        r3 = gestor.crear_reserva("RES003", c2, asesoria, duracion=6)
        r3.confirmar()
        costo = r3.procesar()
        print(f"    OK -> {r3} | Costo total: ${costo:,.2f}")
        contador_exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 9: Procesamiento sin confirmar (error controlado) ---
    print("\n[9] Procesar reserva SIN confirmar (debe fallar)")
    try:
        r4 = gestor.crear_reserva("RES004", c1, equipo, duracion=4)
        r4.procesar()  # No se confirmó: debe lanzar excepción
        contador_exitosos += 1
    except ReservaInvalidaError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        contador_fallidos += 1

    # --- OPERACIÓN 10: Reserva con descuento INVÁLIDO (encadenamiento) ---
    print("\n[10] Procesamiento con descuento INVÁLIDO (>100%)")
    try:
        r5 = gestor.crear_reserva("RES005", c2, equipo, duracion=2)
        r5.confirmar()
        r5.procesar(descuento=1.5)  # Descuento absurdo
        contador_exitosos += 1
    except ReservaInvalidaError as e:
        # Se demuestra el encadenamiento: e.__cause__ es la excepción original
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        if e.__cause__:
            print(f"    Causa original         -> {e.__cause__}")
        contador_fallidos += 1

    # --- Cliente duplicado (operación extra para reforzar la robustez) ---
    print("\n[EXTRA] Intento de registro de cliente DUPLICADO")
    try:
        dup = Cliente("CLI004", "Otra Persona", "1023456789",
                      "otra@correo.com", "3009998877")
        gestor.registrar_cliente(dup)  # Mismo documento que c1
    except DatoInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")

    # --- Resumen final ---
    print("\n" + "=" * 70)
    print("   RESUMEN DE LA SIMULACIÓN")
    print("=" * 70)
    print(f"   Operaciones exitosas: {contador_exitosos}")
    print(f"   Excepciones controladas: {contador_fallidos}")
    print(f"   Total de clientes registrados: {len(gestor.listar_clientes())}")
    print(f"   Total de servicios registrados: {len(gestor.listar_servicios())}")
    print(f"   Total de reservas creadas: {len(gestor.listar_reservas())}")
    print("\n   El sistema permaneció ESTABLE durante toda la simulación.")
    print("   Revise el archivo 'software_fj.log' para ver el registro completo.")
    print("=" * 70)


# ============================================================================
#  PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================
if __name__ == "__main__":
    # Se envuelve la simulación en un try/except/finally global para
    # garantizar que cualquier error inesperado quede registrado y que
    # el programa siempre cierre el sistema de logging correctamente.
    try:
        ejecutar_simulacion()
    except Exception as e:
        logger.critical(f"Error inesperado en la ejecución principal: {e}")
        print(f"\n[CRÍTICO] El sistema reportó un error: {e}")
    finally:
        logger.info("Fin de la ejecución del Sistema Software FJ.")
        logging.shutdown()
