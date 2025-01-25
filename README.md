# Proyecto Final de Minería de Datos: Resolución de Captchas y Extracción de Datos

Este proyecto, desarrollado por **Paul Andrés Astudillo Calle**, es el trabajo final de la materia de Minería de Datos. El objetivo principal es automatizar la interacción con la página de consulta de títulos de la SENESCYT. El script implementa técnicas de minería de datos y visión por computadora para resolver captchas y extraer información de interés.

---

## Funcionalidades del Proyecto

1. **Ingreso Automático de Datos:**
   - Se ingresa un número de cédula en el formulario de la página web de SENESCYT.

2. **Resolución de Captchas:**
   - Los captchas de la página son resueltos automáticamente utilizando **Tesseract OCR**, previa limpieza y procesamiento de la imagen.

3. **Extracción de Información de la Tabla:**
   - Una vez resuelto el captcha, se extrae la información de la tabla de resultados, que contiene datos como:
     - Título profesional
     - Institución de educación superior
     - Tipo de título (nacional o internacional)
     - Fecha de registro
     - Área o campo de conocimiento

4. **Procesamiento de Captchas:**
   - El script guarda tanto los captchas originales como las imágenes procesadas en una carpeta específica para depuración y análisis.

---

## Requisitos del Sistema

- **Python 3.7 o superior**
- **Google Chrome** instalado en tu sistema
- **Chromedriver** compatible con tu versión de Google Chrome
- **Tesseract OCR** instalado y configurado

---

## Instalación y Configuración

### 1. Instalar Dependencias
Clona este repositorio e instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
