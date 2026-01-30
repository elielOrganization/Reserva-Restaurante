user: DiegoSanJuan
contraseña muy importante: restaurantesyreservas


<!-- La idea general es transformar tu sistema de un aforo estático a un sistema de disponibilidad dinámica. En lugar de "sobrescribir" un número, vamos a hacer que el sistema sea capaz de "leer" cuánta gente hay en un momento dado y calcular el hueco libre.

Aquí tienes el plan de acción estructurado para tu proyecto GastroBook:

1. Modificación de Datos (El "Input")
Para que el sistema sepa cuántos asientos quedan, primero necesita saber cuántos asientos ocupa cada reserva:

En la Base de Datos: Añadiremos un campo num_personas a cada documento de la colección Reservas.

En la Interfaz (Flet): En la vista de reserva, añadiremos un campo (un Dropdown del 1 al 10 o un TextField) para que el usuario diga cuántos son.

2. El Motor de Cálculo (La Lógica)
Crearemos una función de Python que actúe como un "filtro de seguridad" antes de confirmar cualquier reserva. El proceso será:

Consultar: "Dime el aforo_maximo de este restaurante".

Sumar: "Suma todas las personas de las reservas que ya existen para esta fecha y hora".

Comparar: Si la suma de las reservas actuales + la nueva reserva es menor o igual al aforo máximo, se permite guardar.

3. Estados Inteligentes (El "Reset" automático)
No necesitas programar un reset de aforo porque la lógica se basa en el estado de la reserva:

Reserva Confirmada: Resta del total disponible (porque la función la suma).

Reserva Cancelada: Deja de restar automáticamente (porque la función solo suma las que están en estado "confirmada").

Paso del tiempo: Las reservas de ayer ya no afectan a las de hoy porque el filtro siempre busca por la fecha_hora específica.

Beneficios de este método
Consistencia: Nunca tendrás "números negativos" en tu aforo.

Flexibilidad: Puedes tener 100 reservas para diferentes días y cada una respetará el límite de su fecha correspondiente.

Escalabilidad: Si el restaurante amplía su local y cambias el aforo_maximo de 80 a 100, todas las fechas futuras se actualizan solas. -->