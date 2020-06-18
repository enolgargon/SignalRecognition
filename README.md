# Signal Recognition
Software para un prototipo de bajo coste basando en aprendizaje profundo (Deep Learning) para la identificación automática de señales de tráfico en vehículos.

## Requisitos
El sistema esta pensado para ser implementado en Intel NUC. Cualquier minipc con una capacidad de procesamiento similar al Intel NUC podría servir para ejecutar el sistema. Utilzar un minipc es de especial interés para emplazar el sistema en un vehículo.

## Instalación
### Preparación del entorno
Para la instalación del sistema desarrollado se requiere como paso previo preparar el Intel NUC con el sistema Ubuntu. Para ello se crea una unidad booteable con la instalación de Ubuntu y se inserta en el equipo al arrancar para que arranque desde ella. Cuando el equipo arranque se deben seguir los pasos indicados por el asistente de instalación para realizarla por completo.
Durante la instalación se debe configurar un único usuario con el nombre de recognition y sin contraseña.

### Instalación del sistema
Para instalar el sistema desarrollado se debe abrir una terminal –puede hacerse con el atajo de teclado Alt+T–, y seguir los siguientes pasos:
1. Instalar las librerías necesarias para que el sistema pueda funcionar con la órden:
`sudo apt-get install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test`
2. Instalar el Sistema gestor de bases de datos con la órden:
`sudo apt-get install sqlite3 libsqlite3-dev`
3. Asegurarse de estar en el home del usuario pi utilizando cd.
4. Crear la base de datos que utilizará la aplicación con la órden:
`sudo sqlite3 SignalRecognition.db`
5. El paso anterior cambiará el prompt reflejando que estamos dentro de una línea de órdenes de sqlite y se esperan acciones relacionadas con bases de datos. No obstante, con el paso número 4, la base de datos ya queda creada y se puede salir del prompt de sqlite con `.quit` y verificar que se ha creado la base de datos correctamente con la orden `ls`, la cual retornará la lista de ficheros y subdirectorios del directorio home de pi, entre los que se encuentra el fichero SignalRecognition.db.
6. Descargarse el sistema desarrollado desde el repositorio en GitHub. Se puede utilizar la orden:
`git clone https://github.com/recognition/SignalRecognition.db`
7. Entrar en el directorio del sistema desarrollado con: `cd SignalRecognition`
8. Crear un entorno virtual para el sistema con la orden:
`python3 -m venv venv`
9. Activar el entorno virtual con la orden:
`source venv/bin/activate`
10. Instalar los requisitos del sistema utilizando el gestor de paquetes pip de Python, se puede utilizar la orden:
`pip3 install -r requirements.txt`
11. Preparar el navegador con lo descrito en el apartado de Preparación del navegador
12. Ejecutar el fichero de instalación. Éste se encargará de crear las tareas del sistema necesarias para que la ejecución del sistema sea automática y se controlen las caídas de los diferentes módulos para volver a ejecutarlos. Se puede hacer con la orden:
`bash setup.bash`

### Preparación del navegador
El usuario va a observar el sistema a través de una ventana del navegador. Como el propio sistema Ubuntu ya incluye el navegador Firefox la preparación se puede hacer desde él. Para preparar el navegador es necesario realizar dos pasos:
- Colocar como página de inicio el fichero html de la interfaz de usuario. Para ello:
	1. Ir a configuración de Firefox y dentro de ella al apartado Home
	2. Seleccionar en la zona que indica Home page and new windows la opción de Custom URLs
	3. Escribir la URL “file:///home/recognition/SignalRecognition/gui/gui.html”
- Preparar el navegador para que siempre se ejecute a pantalla completa. Para ello:
	1. Ir al menú de Firefox y seleccionar la opción Complementos
	2. Pulsar sobre el botón Buscar más complementos
	3. Escribir en el cuadro de búsqueda la página que abre “Full screen”
	4. Instalar el complemento “Full Screen for Firefox”
