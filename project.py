from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract
import time
import os

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'"C:\Program Files\Tesseract-OCR\tesseract.exe"'

# Configuración de Selenium y rutas
CHROMEDRIVER_PATH = r"C:\\Users\\Paul\\chromedriver-win64\\chromedriver.exe"
CAPTCHA_SAVE_DIR = "captchas_reales"  # Carpeta para guardar captchas reales
os.makedirs(CAPTCHA_SAVE_DIR, exist_ok=True)  # Crear carpeta si no existe
MAX_ATTEMPTS = 3  # Máximo de intentos para resolver el captcha

# Función para procesar y predecir texto con Tesseract
def predict_with_tesseract(image_path):
    captcha_image = Image.open(image_path).convert("L")  # Escala de grises
    captcha_image = captcha_image.filter(ImageFilter.MedianFilter())  # Reducir ruido
    captcha_image = ImageEnhance.Contrast(captcha_image).enhance(3)  # Aumentar contraste
    captcha_image = captcha_image.point(lambda x: 0 if x < 140 else 255)  # Binarización ajustada
    captcha_image.save(f"{CAPTCHA_SAVE_DIR}/processed_{os.path.basename(image_path)}")  # Guardar imagen procesada
    return pytesseract.image_to_string(
        captcha_image, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
    ).strip()

# Función para limpiar y validar la predicción del captcha
def clean_prediction(prediction):
    prediction = prediction.lower()  # Convertir a minúsculas
    prediction = ''.join(filter(str.isalnum, prediction))  # Solo mantener alfanuméricos
    return prediction[:4]  # Asegurar que solo tome los primeros 4 caracteres

# Configuración de Selenium
chrome_service = Service(CHROMEDRIVER_PATH)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
chrome_options.add_argument("--disable-gpu")
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
    identificacion_input.send_keys("0107235764")  # Cambia esto por la cédula deseada
    print("Cédula ingresada correctamente.")
except Exception as e:
    print(f"Error al ingresar la cédula: {e}")
    driver.quit()
    exit()

# Intentar resolver el captcha
captcha_resuelto = False
for attempt in range(MAX_ATTEMPTS):
    try:
        # Capturar el captcha
        captcha_element = driver.find_element(By.XPATH, '//img[@id="formPrincipal:capimg"]')
        captcha_path = os.path.join(CAPTCHA_SAVE_DIR, f"captcha_attempt_{attempt}.png")
        captcha_element.screenshot(captcha_path)

        # Usar Tesseract para predecir el texto
        predicted_text = clean_prediction(predict_with_tesseract(captcha_path))
        print(f"Intento {attempt + 1}: Predicción del captcha = {predicted_text}")

        # Ingresar el texto del captcha en el formulario
        captcha_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:captchaSellerInput"]')
        captcha_input.clear()
        captcha_input.send_keys(predicted_text)

        # Enviar el formulario
        submit_button = driver.find_element(By.XPATH, '//button[@id="formPrincipal:boton-buscar"]')
        submit_button.click()
        time.sleep(5)

        # Verificar si el captcha fue resuelto correctamente
        if "tablaAplicaciones" in driver.page_source:
            print("Captcha resuelto correctamente.")
            captcha_resuelto = True
            break
    except Exception as e:
        print(f"Error al resolver el captcha: {e}")

if not captcha_resuelto:
    print("No se pudo resolver el captcha después de varios intentos.")
    driver.quit()
    exit()

# Extraer la información de la tabla
try:
    table = driver.find_element(By.XPATH, '//div[@id="formPrincipal:j_idt56:0:tablaAplicaciones"]')
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    print("Información encontrada en la tabla:")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text for cell in cells]
        print(data)  # Imprime la fila completa
except Exception as e:
    print(f"Error al extraer datos de la tabla: {e}")

# Cerrar el navegador
driver.quit()
