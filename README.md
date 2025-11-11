## Organizador de ROMs de 3DS: Todo en un Clic
<img width="1288" height="772" alt="image" src="https://github.com/user-attachments/assets/97f69372-d896-4795-a8c1-1b44ea12571f" />

¿Cansado de tener una carpeta de juegos de 3DS desordenada, llena de archivos `.zip`, `.rar`, `.7z` y con formatos confusos como `.3ds` o `.cia`? Esta aplicación es tu solución.

### ¿Qué es esta aplicación y para qué sirve?

Es una pequeña pero potente herramienta diseñada para hacer una sola cosa a la perfección: **limpiar y organizar tu colección de ROMs de Nintendo 3DS** para que funcionen de maravilla en emuladores.

Su trabajo es automático:
1.  **Busca** en la carpeta que le indiques.
2.  **Descomprime** todos los archivos `.zip`, `.rar` o `.7z` que encuentra.
3.  **Identifica** los juegos (archivos `.3ds`, `.cia`, etc.) que estaban dentro.
4.  **Renombra** todos esos juegos al formato `.cci`, que es el ideal para emuladores.
5.  **Mueve** los archivos comprimidos originales a una carpeta de "backup" para mantener todo ordenado.

En resumen: **transforma tu carpeta de juegos desordenada en una biblioteca limpia y lista para jugar.**

---

### Beneficios: ¿Por qué usarla?

* **Ahorro de Tiempo Absoluto:** Olvídate de descomprimir y renombrar cada juego uno por uno. Si tienes 50 juegos, la app lo hace por ti en segundos.
* **Organización Instantánea:** Tu carpeta principal quedará solo con los juegos jugables (`.cci`). Los archivos `.zip` y `.rar` originales se guardan en una carpeta de respaldo, por si los necesitas.
* **Compatibilidad Total:** Funciona con los formatos de compresión más populares (zip, rar, 7z), así no necesitas tener 7-Zip o WinRAR instalados.
* **Fácil de Usar:** No hay menús complicados. Es una sola ventana: seleccionas tu carpeta, presionas "Iniciar" y ves la magia suceder.


---

### Guía de Uso

Usar la aplicación es increíblemente sencillo:

1.  Descarga el programa desde: [Releases](https://github.com/andromux/flet-3dstocci/releases/tag/1.0) **Ejecuta el archivo** `ROM_Renamer_3DS.exe`.
    * *Nota de Seguridad:* Como es una app no firmada, es posible que Windows muestre una advertencia de "SmartScreen". Solo tienes que hacer clic en "Más información" y luego en "Ejecutar de todos modos".
2.  **Selecciona tu Carpeta:** Haz clic en el botón **"Seleccionar Carpeta"**.
3.  **Elige:** Busca y acepta la carpeta donde tienes todos tus juegos de 3DS desordenados.
4.  **Inicia:** Haz clic en el botón verde **"Iniciar Proceso"**.
5.  **Espera:** Verás un registro de todo lo que la app está haciendo (descomprimiendo, renombrando, moviendo).
6.  **¡Listo!** Cuando veas el mensaje "Proceso completado", ve a tu carpeta. Encontrarás todos tus juegos convertidos a `.cci` y una nueva carpeta llamada `archivos_comprimidos_backup` con los archivos originales.

---

### ¿Prefieres compilarlo tú mismo? (La opción más segura)

Si no confías en descargar un `.exe` de Internet (¡lo cual es una práctica excelente!), puedes usar GitHub para crear tu propia versión 100% segura. El proceso se llama "Fork" (bifurcación) y usa los servidores de GitHub para compilar el código por ti.

Aquí te explicamos cómo hacerlo desde el repositorio oficial:

**1. Haz un "Fork" (una copia personal) del proyecto**
* Arriba a la derecha, haz clic en el botón que dice **"Fork"**. 
* GitHub creará una copia exacta del proyecto en tu propia cuenta (ej. `TuUsuario/flet-3dstocci`).

**2. Habilita las "Actions" en tu copia**
* En *tu* repositorio (el que acabas de "forkear"), ve a la pestaña **"Actions"**.
* Si aparece un botón verde que dice **"I understand my workflows, go ahead and enable them"**, haz clic en él.

**3. Ejecuta el Workflow (El trabajo de compilación)**
* En el menú de la izquierda, haz clic en el workflow llamado **"📦 Compilar EXE para Windows"**.
* Verás un botón a la derecha que dice **"Run workflow"** (Ejecutar workflow). Haz clic en él.
* Se abrirá un pequeño menú, asegúrate de que la rama sea `main` y vuelve a hacer clic en el botón verde **"Run workflow"**.

**4. Descarga tu `.exe` seguro**
* Espera unos minutos. Verás que el trabajo (workflow) se pone en amarillo (en progreso) y luego en verde (completado ✅).
* Haz clic en el nombre del workflow que acaba de terminar (el texto azul).
* En la parte de abajo de esa página, verás una sección llamada **"Artifacts"** (Artefactos).
* Ahí estará tu archivo `.zip` (ej. `ROM-Renamer-Windows-EXE.zip`).
* Haz clic en él para **descargarlo**.

Ese archivo `.zip` contiene el `.exe` que fue compilado por los servidores seguros de GitHub directamente desde el código fuente (`main.py`). Es la forma más segura de obtener la aplicación.
