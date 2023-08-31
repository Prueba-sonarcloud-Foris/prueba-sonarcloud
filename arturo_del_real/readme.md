### Problema de código Arturo del Real

Para resolver el problema se hicieron 3 clases, estas tienen distintos métodos, que buscan cada uno hacer una sola tarea.
 Estos métodos fueron pensados para poder ser reutilizados en caso de extensión del problema, como por ejemplo, 
 ingresar datos desde otro input o poder generar otro tipo de resumen. Eventualmente podría permitir un mayor trabajo 
 sobre las asistencias, permitiendo validar si se solapan, o unir 2 o más asistnecias muy pegadas.
 
 Adicionalmente se agregan algunas validaciones básicas del archivo de entrada.

##### Clases

* University: Clase que contiene todo el ecosistema
    * add_data_from_file: lee un archivo y aplica los comandos correctos.
    * add_student: método reutilizable para agregar estudiantes
    * add_data_for_student: método reutilizable para agregar asistencias a un estudiante
    * get_resume: obtiene el resumen solicitado
* Student: Clase que se define cada uno de los estudiantes de la universidad
    * add_data: agrega una nueva asistencia al empleado (si esque esta es correcta)
    * total_minutes: según los datos, calcula los minutos totales
    * days_present: según los datos, calcula la cantidad de días que asistió el estudiante
    * get_resume: obtiene el resumen del estudiante, esto será utilizado por la universidad
* Attendance: Clase que define cada una de las presencias válidas del estudiante
    * consider: según el criterio indicado, valida si la asistencia es o no válida
    * minutes: obtiene la duración de la asistencia
    
##### Test

Se realizó test unitarios de los distintos métodos y funciones, todos ubicados dentro de la carpeta tests

   
##### Consideraciones

* Se utilizó pipenv, pero se adjunta también un requirements.txt
* Se utilizó python 3.7
* Se debe ejecutar de la forma python main.py {file_path}

De antemano muchas gracias y que tengan buen(a) día/tarde/noche (lease según la hora del día)
