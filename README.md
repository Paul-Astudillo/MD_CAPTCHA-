### README: Resolución Automática de Captchas y Extracción de Datos de una Tabla en la Web
#### Universidad Politécnica Salesiana - UPS

#### Asignatura : Mineria de Datos
#### Autor :Paul Astudillo
#### Perdido :65

Este proyecto utiliza **Selenium** y **Tesseract OCR** para automatizar el llenado de un formulario web, resolver un captcha alfanumérico y extraer información de una tabla resultante. El flujo está diseñado para trabajar con la página de consulta de títulos de **SENESCYT**.

---

### Requisitos

1. **Python 3.x** instalado.
2. Las siguientes bibliotecas de Python:
   - `selenium`
   - `pytesseract`
   - `Pillow`
3. **Tesseract OCR** instalado:
   - Descarga: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
   - Configura la ruta en el código (`pytesseract.pytesseract.tesseract_cmd`).
4. **ChromeDriver** correspondiente a la versión de Google Chrome instalada:
   - Descarga: [ChromeDriver](https://chromedriver.chromium.org/downloads).
5. Acceso a la página web de **SENESCYT**:  
   - URL: `https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml`

---

### Archivos y Directorios

- `main.py`: Contiene el script principal.
- Carpeta `captchas_reales`: Contendrá las imágenes del captcha capturadas y procesadas para su análisis.

---

### Cómo funciona el script

#### 1. **Configuración inicial**
- Se configura la ruta de Tesseract OCR y ChromeDriver.
- Se crean directorios necesarios para guardar las imágenes del captcha.

#### 2. **Automatización con Selenium**
- El script abre la página de consulta de títulos en **SENESCYT**.
- Llena automáticamente el campo de **cédula** con el valor especificado (`0107235764`).

#### 3. **Captura y resolución del captcha**
- Captura la imagen del captcha y la guarda en la carpeta `captchas_reales`.
- Preprocesa la imagen usando la biblioteca **Pillow**:
  - Escala de grises.
  - Mejora del contraste.
  - Filtro de reducción de ruido.
  - Binarización ajustada.
- Usa **Tesseract OCR** para predecir el texto del captcha, limitando a 4 caracteres alfanuméricos.

#### 4. **Validación y reintentos**
- Si el texto predicho tiene 4 caracteres, lo ingresa en el campo del captcha.
- Si no se resuelve correctamente, reintenta hasta un máximo de 5 veces.

#### 5. **Búsqueda y extracción de datos**
- Una vez resuelto el captcha, el script hace clic en el botón **Buscar**.
- Extrae las filas y columnas de la tabla de resultados y las imprime en la terminal.

#### 6. **Cierre del navegador**
- Finalmente, cierra el navegador de forma segura.

---

### Instrucciones para usar el script

1. Clona este repositorio o copia el archivo `main.py` en tu máquina local.
2. Configura la ruta de Tesseract OCR en la línea:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```
3. Configura la ruta de ChromeDriver en la línea:
   ```python
   CHROMEDRIVER_PATH = r"C:\\Users\\Paul\\chromedriver-win64\\chromedriver.exe"
   ```
4. Instala las bibliotecas necesarias ejecutando:
   ```bash
   pip install selenium pillow pytesseract
   ```
5. Ejecuta el script:
   ```bash
   python main.py
   ```

---

### Resultado esperado

1. **Captura y resolución del captcha**:
   - Se capturan imágenes del captcha y se guardan en la carpeta `captchas_reales` para revisión.
   - La predicción del captcha se valida y se ingresa en el formulario.

2. **Extracción de datos**:
   - La tabla de resultados se extrae y se muestra en la terminal. Por ejemplo:
     ```plaintext
     Información encontrada en la tabla:
     ['INGENIERO/A BIOMEDICO/A', 'UNIVERSIDAD POLITÉCNICA SALESIANA', 'Nacional', '', '1034-2023-2761003', '2023-10-26', 'CIENCIAS NATURALES, MATEMÁTICAS Y ESTADÍSTICA', '']
     ```

3. **Errores manejados**:
   - Si el captcha no se resuelve después de 5 intentos, el script muestra un mensaje de error:
     ```plaintext
     No se pudo resolver el captcha después de varios intentos.
     ```

---

### Detalles técnicos

1. **Preprocesamiento del captcha**:
   - Escala de grises: Mejora la claridad al eliminar colores.
   - Contraste: Resalta caracteres frente al fondo.
   - Filtro de mediana: Reduce el ruido en la imagen.
   - Binarización: Convierte píxeles claros/oscuros en blanco y negro.

2. **Tesseract OCR**:
   - Configuración específica para captchas de 4 caracteres:
     ```plaintext
     --psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
     ```

3. **Selenium**:
   - Encuentra elementos de la página mediante **XPath** y los interactúa automáticamente:
     - Campo de cédula: `//input[@id="formPrincipal:identificacion"]`
     - Imagen del captcha: `//img[@id="formPrincipal:capimg"]`
     - Campo del captcha: `//input[@id="formPrincipal:captchaSellerInput"]`
     - Botón Buscar: `//button[@id="formPrincipal:boton-buscar"]`
   - Maneja tiempos de espera con `time.sleep` para garantizar que la página cargue completamente antes de interactuar con los elementos.

---

### Notas importantes

- **Revisión manual del captcha**:
  - Si el OCR no funciona correctamente, verifica las imágenes en `captchas_reales` y ajusta los parámetros de preprocesamiento (`ImageOps.autocontrast`, `ImageFilter.MedianFilter`, etc.).

- **XPath dinámicos**:
  - Si la página cambia, puede ser necesario actualizar los identificadores XPath.

- **Mejoras futuras**:
  - Implementar un modelo de aprendizaje automático para resolver captchas de manera más precisa.
  - Usar técnicas de espera explícita en Selenium (`WebDriverWait`) para mejorar la robustez.

---
