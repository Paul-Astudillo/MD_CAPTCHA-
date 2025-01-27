import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configuración de Selenium y rutas
CHROMEDRIVER_PATH = r"C:\\Users\\Paul\\chromedriver-win64\\chromedriver.exe"
CAPTCHA_SAVE_DIR = "captchas_reales"
os.makedirs(CAPTCHA_SAVE_DIR, exist_ok=True)
MAX_ATTEMPTS = 5  # Máximo de intentos para resolver el captcha

# Leer cédula desde el archivo de texto
CEDULA_FILE = "cedula.txt"
if not os.path.exists(CEDULA_FILE):
    print(f"Archivo {CEDULA_FILE} no encontrado. Asegúrate de crearlo con la cédula.")
    exit()

with open(CEDULA_FILE, "r") as file:
    cedula = file.read().strip()
    if not cedula.isdigit() or len(cedula) != 10:
        print(f"El contenido del archivo {CEDULA_FILE} no parece ser una cédula válida.")
        exit()

# Función para procesar y predecir texto con Tesseract
def predict_with_tesseract(image_path):
    captcha_image = Image.open(image_path).convert("L")
    captcha_image = ImageOps.autocontrast(captcha_image)
    captcha_image = captcha_image.filter(ImageFilter.MedianFilter(size=3))
    captcha_image = ImageEnhance.Contrast(captcha_image).enhance(4)
    captcha_image = captcha_image.point(lambda x: 0 if x < 150 else 255)
    processed_image_path = f"{CAPTCHA_SAVE_DIR}/processed_{os.path.basename(image_path)}"
    captcha_image.save(processed_image_path)

    tesseract_config = "--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    prediction = pytesseract.image_to_string(captcha_image, config=tesseract_config).strip()
    prediction = prediction.replace("l", "1").replace("I", "1").replace("O", "0").replace("Z", "2").replace("S", "5")
    return prediction[:4]

# Configuración de Selenium
chrome_service = Service(CHROMEDRIVER_PATH)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Inicializar WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navegar a la página de SENESCYT
url = "https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml"
driver.get(url)
time.sleep(3)

captcha_resuelto = False
for attempt in range(MAX_ATTEMPTS):
    try:
        # Ingresar la cédula en cada intento
        identificacion_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:identificacion"]')
        identificacion_input.clear()
        identificacion_input.send_keys(cedula)
        time.sleep(1)

        # Capturar el captcha
        captcha_element = driver.find_element(By.XPATH, '//img[@id="formPrincipal:capimg"]')
        captcha_path = os.path.join(CAPTCHA_SAVE_DIR, f"captcha_attempt_{attempt}.png")
        captcha_element.screenshot(captcha_path)

        predicted_text = predict_with_tesseract(captcha_path)
        print(f"Intento {attempt + 1}: Predicción del captcha = {predicted_text}")

        if len(predicted_text) != 4:
            print("Predicción inválida, reintentando...")
            continue

        # Ingresar el texto del captcha
        captcha_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:captchaSellerInput"]')
        captcha_input.clear()
        captcha_input.send_keys(predicted_text)

        # Hacer clic en el botón "Buscar"
        submit_button = driver.find_element(By.XPATH, '//button[@id="formPrincipal:boton-buscar"]')
        submit_button.click()

        # Esperar a que la tabla esté presente después de la recarga
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="formPrincipal:j_idt52:0:tablaAplicaciones"]'))
        )
        print("Captcha resuelto correctamente y la tabla está disponible.")
        captcha_resuelto = True
        break
    except Exception as e:
        print(f"Error en el intento {attempt + 1}: {e}")

if not captcha_resuelto:
    print("No se pudo resolver el captcha después de varios intentos.")
    driver.quit()
    exit()

# Extraer la información de la tabla
try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="formPrincipal:j_idt52:0:tablaAplicaciones"]'))
    )
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    print("Información encontrada en la tabla:")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text.strip() for cell in cells]
        print(data)
except Exception as e:
    print(f"Error al extraer datos de la tabla: {e}")

driver.quit()
