# Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Software FJ** — Proyecto académico desarrollado por el grupo de la Fase 4 del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

---

## 📌 Descripción

Sistema orientado a objetos en Python que gestiona **clientes**, **servicios** (reservas de salas, alquiler de equipos y asesorías especializadas) y **reservas**, sin uso de bases de datos. Toda la información se mantiene en memoria mediante objetos y listas. Los eventos y errores se registran en un archivo de logs.

## 🎯 Objetivos de aprendizaje

Implementar el manejo de excepciones en el desarrollo de aplicaciones orientadas a objetos buscando estabilidad y robustez, permitiendo una gestión adecuada de errores en el funcionamiento de las soluciones.

## 🏗️ Arquitectura

| Componente | Tipo | Descripción |
|-----------|------|-------------|
| `EntidadBase` | Clase abstracta | Representa cualquier entidad del sistema. Define `descripcion()` y `validar()` como abstractos. |
| `Cliente` | Clase concreta | Hereda de `EntidadBase`. Encapsula datos personales con validación estricta (correo, teléfono, documento). |
| `Servicio` | Clase abstracta | Define la interfaz común de los servicios. Implementa `calcular_costo_total()` con sobrecarga (impuestos y descuentos). |
| `ReservaSala` | Clase concreta | Reserva de salas por horas. |
| `AlquilerEquipo` | Clase concreta | Alquiler por días con recargo después de 7 días y control de stock. |
| `AsesoriaTecnica` | Clase concreta | Asesoría por hora con tarifa premium para sesiones de 5+ horas. |
| `Reserva` | Clase concreta | Vincula cliente y servicio. Maneja el ciclo de vida (PENDIENTE → CONFIRMADA → PROCESADA / CANCELADA). |
| `GestorSoftwareFJ` | Clase concreta | Coordinador central con listas internas. |

## ⚠️ Manejo de excepciones

| Excepción personalizada | Caso de uso |
|-------------------------|-------------|
| `SoftwareFJError` | Excepción base del sistema. |
| `DatoInvalidoError` | Datos que no cumplen reglas de validación. |
| `ParametroFaltanteError` | Parámetro obligatorio ausente. |
| `ServicioNoDisponibleError` | Servicio agotado o inactivo. |
| `ReservaInvalidaError` | Reserva con datos inconsistentes. |
| `CalculoInconsistenteError` | Cálculo con resultado imposible. |

Se utilizan los bloques `try/except`, `try/except/else`, `try/except/finally` y se demuestra el **encadenamiento de excepciones** con `raise ... from ...` (operación 10 de la simulación).

## 📁 Estructura del repositorio

```
.
├── sistema_software_fj.ipynb   # Jupyter Notebook principal (entregable)
├── sistema_software_fj.py      # Equivalente .py para revisión rápida
├── software_fj.log             # Archivo de logs generado en ejecución
└── README.md                   # Este archivo
```

## 👥 Distribución de responsabilidades

| Estudiante | Módulo asignado |
|-----------|-----------------|
| Integrante 1 | Clase `Cliente` y validaciones de datos personales |
| Integrante 2 | Clase abstracta `Servicio` y los tres servicios especializados |
| Integrante 3 | Clase `Reserva` y ciclo de vida con manejo de excepciones |
| Integrante 4 | Excepciones personalizadas y sistema de logs |
| Integrante 5 | `GestorSoftwareFJ`, integración final y simulación |

## ▶️ Ejecución

### Opción 1 – Jupyter Notebook
```bash
jupyter notebook sistema_software_fj.ipynb
```

### Opción 2 – Script Python
```bash
python sistema_software_fj.py
```

Ambas opciones generan el archivo `software_fj.log` con el registro completo de eventos y errores.

## ✅ Validación

La simulación ejecuta **10+ operaciones** que combinan casos válidos e inválidos:

| # | Operación | Resultado esperado |
|---|-----------|--------------------|
| 1 | Registro de cliente válido | OK |
| 2 | Cliente con correo inválido | Excepción controlada |
| 3 | Segundo cliente válido | OK |
| 4 | Servicio con tarifa negativa | Excepción controlada |
| 5 | Tres servicios válidos | OK |
| 6 | Reserva exitosa con descuento | OK |
| 7 | Reserva con duración cero | Excepción controlada |
| 8 | Asesoría con tarifa premium | OK |
| 9 | Procesar reserva sin confirmar | Excepción controlada |
| 10 | Descuento >100% (encadenamiento) | Excepción controlada con causa original |
| Extra | Cliente con documento duplicado | Excepción controlada |

El sistema **mantiene estabilidad** en todos los escenarios.

## 📚 Referencias

- Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
- Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.
- Romano, F., Baka, B., & Phillips, D. (2019). *Getting Started with Python*. Packt Publishing.

---
*Universidad Nacional Abierta y a Distancia (UNAD) — Curso 213023 — 2026*
