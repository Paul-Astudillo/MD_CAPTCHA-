### README: Resolución Automática de Captchas y Extracción de Datos

#### Universidad Politécnica Salesiana (UPS)  
#### Asignatura: Minería de Datos  
#### Autor: Paul Astudillo  
#### Período: 65  

Este proyecto automatiza el ingreso de cédulas, la resolución de captchas y la extracción de información de la tabla de resultados en la página de consulta de títulos de la **SENESCYT**. Utiliza **Selenium** y **Tesseract OCR** para realizar estas tareas de forma eficiente.

---

### Requisitos

1. **Python 3.x** instalado.
2. Librerías necesarias:
   - `selenium`
   - `pytesseract`
   - `Pillow`
3. **Tesseract OCR** instalado:
   - Descárgalo desde [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) y asegúrate de configurar la ruta en el código.
4. **ChromeDriver** correspondiente a la versión de Google Chrome instalada:
   - Descarga desde [ChromeDriver](https://chromedriver.chromium.org/downloads) y actualiza la ruta en el script.
5. **Acceso a la página de SENESCYT:**
   - URL: `https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml`
6. Un archivo `cedula.txt` que contenga una cédula válida de 10 dígitos.

---

### Archivos y Estructura del Proyecto

- **`project.py`**: Script principal del proyecto.
- **`cedula.txt`**: Archivo de texto con el número de cédula a consultar.
- **`captchas_reales/`**: Carpeta que almacena las imágenes de los captchas descargados y procesados.
- **`resultados/`**: Carpeta donde se guarda  capturas del proceso de ejecucion de los captchas resueltos y los datos extraídos.

---

### Pasos del Script

#### 1. **Configuración inicial**
- Configura la ruta de **Tesseract OCR** y **ChromeDriver**.
- Crea directorios para guardar captchas y resultados.

#### 2. **Ingreso de datos**
- Lee la cédula desde `cedula.txt` y verifica que sea válida.
- Abre la página de SENESCYT y llena automáticamente el campo de cédula.

#### 3. **Resolución del captcha**
- Captura la imagen del captcha y la procesa:
  - Escala de grises.
  - Mejora de contraste.
  - Filtro de mediana para reducir ruido.
  - Binarización para resaltar caracteres.
- Predice el texto del captcha con **Tesseract OCR**.

#### 4. **Validación y reintentos**
- Si el captcha no se resuelve correctamente, realiza hasta 5 intentos.
- Si se resuelve correctamente, envía el formulario.

#### 5. **Extracción de datos**
- Una vez resuelto el captcha, espera a que la tabla de resultados cargue.
- Extrae y muestra las filas y columnas de la tabla.

#### 6. **Registro de resultados**
- Guarda las imágenes procesadas del captcha en `captchas_reales/`.
- Los resultados extraídos de la tabla se registran en consola.

#### 7. **Cierre del navegador**
- El navegador se cierra automáticamente al finalizar.

---

### Cómo ejecutar el script

1. Coloca la cédula en el archivo `cedula.txt` (solo 10 dígitos, por ejemplo: `0107235764`).
2. Asegúrate de que las rutas de **Tesseract OCR** y **ChromeDriver** estén configuradas correctamente en el script:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   CHROMEDRIVER_PATH = r"C:\\Users\\Paul\\chromedriver-win64\\chromedriver.exe"
   ```
3. Instala las librerías necesarias ejecutando:
   ```bash
   pip install selenium pillow pytesseract
   ```
4. Ejecuta el script con:
   ```bash
   python project.py
   ```

---

### Resultado esperado

1. **Resolución del captcha:**
   - Se capturan imágenes del captcha en la carpeta `captchas_reales/`.
   - Las predicciones del captcha se registran y verifican.

2. **Extracción de datos:**
   - Se imprime en consola el contenido de la tabla de resultados. Ejemplo:
     ```plaintext
     Información encontrada en la tabla:
     ['INGENIERO/A BIOMEDICO/A', 'UNIVERSIDAD POLITÉCNICA SALESIANA', 'Nacional', '', '1034-2023-2761003', '2023-10-26', 'CIENCIAS NATURALES, MATEMÁTICAS Y ESTADÍSTICA', '']
     ```

3. **Errores manejados:**
   - Si no se resuelve el captcha después de 5 intentos, muestra:
     ```plaintext
     No se pudo resolver el captcha después de varios intentos.
     ```

---

### Detalles técnicos

1. **Preprocesamiento de imágenes:**  
   Mejora la calidad de los captchas mediante técnicas de procesamiento de imágenes:
   - Escala de grises: Elimina distracciones de color.
   - Contraste: Resalta los caracteres.
   - Filtro de mediana: Reduce el ruido.
   - Binarización: Convierte la imagen a blanco y negro para facilitar el reconocimiento.

2. **OCR con Tesseract:**  
   Configuración optimizada para captchas de 4 caracteres:
   ```plaintext
   --psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
   ```

3. **Automatización con Selenium:**  
   - Interactúa con elementos de la página mediante XPath.
   - Espera explícitas (`WebDriverWait`) aseguran que los elementos estén cargados antes de interactuar con ellos.

---

### Notas adicionales

- **Precisión del OCR:**  
  Actualmente, el script tiene una precisión aproximada del 75%. Esto significa que podría fallar en algunos casos. Las imágenes de captchas fallidos se guardan para su análisis.

- **Universidad Politécnica Salesiana:**  
  Este proyecto fue desarrollado para la asignatura de  **Minería de Datos** en el período **65**.

---
