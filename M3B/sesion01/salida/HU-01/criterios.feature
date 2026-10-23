# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos,
  quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso,
  para darlo de alta en la empresa.

  Escenario: Registro exitoso con número de empleado asignado por el sistema
    Dado que el último empleado registrado tiene el número "EMP-0007"
    Y que no existe ningún empleado con el correo "ana.lopez@empresa.com"
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Analista de datos", departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces el empleado queda guardado con el número de empleado "EMP-0008"
    Y su estado es "activo"
    Y su fecha de registro (creado_en) la asigna el sistema
    Y la pantalla muestra un mensaje de confirmación que incluye el número "EMP-0008"

  Escenario: El formulario no permite escribir el número de empleado
    Dado que estoy en la pantalla de registro de empleado
    Cuando reviso los campos del formulario
    Entonces veo los campos nombre, correo, puesto, departamento y fecha de ingreso
    Y no existe un campo para escribir el número de empleado

  Escenario: El correo se guarda en minúsculas
    Dado que no existe ningún empleado con el correo "luis.perez@empresa.com"
    Cuando registro un empleado con nombre "Luis Pérez", correo "Luis.Perez@Empresa.com", puesto "Vendedor", departamento "Ventas" y fecha de ingreso "2026-09-15"
    Entonces el empleado queda guardado con el correo "luis.perez@empresa.com"

  Escenario: Correo duplicado sin importar mayúsculas (regla 1)
    Dado que existe un empleado con el correo "ana.lopez@empresa.com"
    Cuando registro un empleado con nombre "Ana María López", correo "ANA.LOPEZ@empresa.com", puesto "Contadora", departamento "Finanzas" y fecha de ingreso "2026-10-01"
    Entonces la API responde 409 con el mensaje "El correo ya está registrado"
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea un nuevo empleado

  Escenario: Correo que no es corporativo (regla 2)
    Dado que estoy en la pantalla de registro de empleado
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@gmail.com", puesto "Analista de datos", departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422 con el mensaje "Usa el correo corporativo @empresa.com"
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"
    Y no se crea un nuevo empleado

  Escenario: Fecha de ingreso futura (regla 4)
    Dado que la fecha de hoy es "2026-10-23"
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Analista de datos", departamento "Tecnología" y fecha de ingreso "2026-10-24"
    Entonces la API responde 422 con el mensaje "La fecha de ingreso no puede ser futura"
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"
    Y no se crea un nuevo empleado

  Escenario: Fecha de ingreso igual a hoy es válida
    Dado que la fecha de hoy es "2026-10-23"
    Y que no existe ningún empleado con el correo "marta.ruiz@empresa.com"
    Cuando registro un empleado con nombre "Marta Ruiz", correo "marta.ruiz@empresa.com", puesto "Coordinadora", departamento "Operaciones" y fecha de ingreso "2026-10-23"
    Entonces el empleado queda guardado con estado "activo"

  Escenario: Nombre demasiado corto (regla 3)
    Dado que estoy en la pantalla de registro de empleado
    Cuando registro un empleado con nombre "A", correo "a.sanchez@empresa.com", puesto "Analista de datos", departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422
    Y la pantalla indica que se debe corregir el campo "nombre"
    Y no se crea un nuevo empleado

  Escenario: Nombre de más de 80 caracteres (regla 3)
    Dado que estoy en la pantalla de registro de empleado
    Cuando registro un empleado con un nombre de 81 caracteres, correo "nombre.largo@empresa.com", puesto "Analista de datos", departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422
    Y la pantalla indica que se debe corregir el campo "nombre"
    Y no se crea un nuevo empleado

  Escenario: Puesto demasiado corto (regla 3)
    Dado que estoy en la pantalla de registro de empleado
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "A", departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422
    Y la pantalla indica que se debe corregir el campo "puesto"
    Y no se crea un nuevo empleado

  Escenario: Puesto de más de 60 caracteres (regla 3)
    Dado que estoy en la pantalla de registro de empleado
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", un puesto de 61 caracteres, departamento "Tecnología" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422
    Y la pantalla indica que se debe corregir el campo "puesto"
    Y no se crea un nuevo empleado

  Escenario: Departamento fuera de la lista permitida (regla 3)
    Dado que los departamentos permitidos son "Tecnología", "Ventas", "Finanzas", "Recursos Humanos" y "Operaciones"
    Cuando registro un empleado con nombre "Ana López", correo "ana.lopez@empresa.com", puesto "Abogada", departamento "Legal" y fecha de ingreso "2026-10-01"
    Entonces la API responde 422
    Y la pantalla indica que se debe corregir el campo "departamento"
    Y no se crea un nuevo empleado

  Escenario: Campos obligatorios vacíos (regla 3)
    Dado que estoy en la pantalla de registro de empleado
    Cuando envío el registro de empleado con nombre, correo, puesto, departamento y fecha de ingreso vacíos
    Entonces la API responde 422
    Y la pantalla indica que se deben corregir los campos "nombre", "correo", "puesto", "departamento" y "fecha_ingreso"
    Y no se crea un nuevo empleado

# Preguntas abiertas
# - ¿Cuál es el texto exacto del mensaje de confirmación tras guardar? (p. ej., «Empleado registrado con el número EMP-0008»)
# - ¿Qué código HTTP responde la API en un registro exitoso (201 o 200) y qué campos devuelve?
# - Si la petición a la API incluye numero_empleado, estado o creado_en, ¿se ignoran o se responde 422?
# - ¿Cuál es el número del primer empleado cuando no hay ninguno registrado? Se asume "EMP-0001" por el formato, pero conviene confirmarlo.
# - ¿Qué pasa con el consecutivo al superar EMP-9999?
# - ¿Se recortan los espacios al inicio y al final de nombre y puesto antes de validar la longitud?
# - ¿El mensaje de error por campo inválido (regla 3) tiene un texto definido por campo?
# - ¿La fecha "hoy" para validar la fecha de ingreso se toma en qué zona horaria?
