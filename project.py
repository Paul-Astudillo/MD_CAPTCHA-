import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configuración de Selenium y rutas
CHROMEDRIVER_PATH = r"C:\\Users\\Paul\\chromedriver-win64\\chromedriver.exe"
CAPTCHA_SAVE_DIR = "captchas_reales"  # Carpeta para guardar captchas reales
os.makedirs(CAPTCHA_SAVE_DIR, exist_ok=True)  # Crear carpeta si no existe
MAX_ATTEMPTS = 5  # Máximo de intentos para resolver el captcha

# Función para procesar y predecir texto con Tesseract
def predict_with_tesseract(image_path):
    # Cargar la imagen
    captcha_image = Image.open(image_path).convert("L")  # Convertir a escala de grises
    captcha_image = ImageOps.autocontrast(captcha_image)  # Mejorar contraste
    captcha_image = captcha_image.filter(ImageFilter.MedianFilter(size=3))  # Reducir ruido
    captcha_image = ImageEnhance.Contrast(captcha_image).enhance(3)  # Aumentar contraste adicional
    captcha_image = captcha_image.point(lambda x: 0 if x < 160 else 255)  # Binarización ajustada
    captcha_image.save(f"{CAPTCHA_SAVE_DIR}/processed_{os.path.basename(image_path)}")  # Guardar imagen procesada

    # Predecir con Tesseract, configurando para solo 4 caracteres alfanuméricos
    return pytesseract.image_to_string(
        captcha_image, config="--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ).strip()[:4]

# Configuración de Selenium
chrome_service = Service(CHROMEDRIVER_PATH)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU
chrome_options.add_argument("--no-sandbox")

# Inicializar WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navegar a la página de SENESCYT
url = "https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml"
driver.get(url)
time.sleep(3)

# Ingresar cédula
try:
    identificacion_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:identificacion"]')
    identificacion_input.send_keys("0107235764")  # Cédula proporcionada
    print("Cédula ingresada correctamente.")
except Exception as e:
    print(f"Error al ingresar la cédula: {e}")
    driver.quit()
    exit()

# Intentar resolver el captcha y buscar
captcha_resuelto = False
for attempt in range(MAX_ATTEMPTS):
    try:
        # Capturar el captcha
        captcha_element = driver.find_element(By.XPATH, '//img[@id="formPrincipal:capimg"]')
        captcha_path = os.path.join(CAPTCHA_SAVE_DIR, f"captcha_attempt_{attempt}.png")
        captcha_element.screenshot(captcha_path)

        # Predecir texto del captcha con Tesseract
        predicted_text = predict_with_tesseract(captcha_path)
        print(f"Intento {attempt + 1}: Predicción del captcha = {predicted_text}")

        # Validar longitud de 4 caracteres
        if len(predicted_text) != 4:
            print(f"Predicción inválida (longitud {len(predicted_text)}), reintentando...")
            continue

        # Ingresar el texto del captcha
        captcha_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:captchaSellerInput"]')
        captcha_input.clear()
        captcha_input.send_keys(predicted_text)

        # Hacer clic en el botón "Buscar"
        submit_button = driver.find_element(By.XPATH, '//button[@id="formPrincipal:boton-buscar"]')
        submit_button.click()
        time.sleep(5)

        # Verificar si el captcha fue resuelto correctamente
        if "tablaAplicaciones" in driver.page_source:  # Cambiar según el contenido esperado
            print("Captcha resuelto correctamente.")
            captcha_resuelto = True
            break
        else:
            print("Captcha incorrecto, intentando de nuevo...")
    except Exception as e:
        print(f"Error en el intento {attempt + 1}: {e}")

if not captcha_resuelto:
    print("No se pudo resolver el captcha después de varios intentos.")
    driver.quit()
    exit()

# Extraer la información de la tabla
try:
    table = driver.find_element(By.XPATH, '//div[@id="formPrincipal:j_idt48:0:tablaAplicaciones"]')
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    print("Información encontrada en la tabla:")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text.strip() for cell in cells]
        print(data)  # Imprimir la fila completa
except Exception as e:
    print(f"Error al extraer datos de la tabla: {e}")

# Cerrar el navegador
driver.quit()
