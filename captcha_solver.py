from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import time
import os

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración de Selenium y rutas
CHROMEDRIVER_PATH = r'C:/Users/andy-/OneDrive/Escritorio/8voCiclo/HCP/chromedriver-win64/chromedriver.exe'
CAPTCHA_SAVE_DIR = "captchas_reales"  # Carpeta para guardar captchas reales
os.makedirs(CAPTCHA_SAVE_DIR, exist_ok=True)  # Crear carpeta si no existe
MAX_ATTEMPTS = 3  # Máximo de intentos para resolver el captcha

# Función para procesar y predecir texto con Tesseract
def predict_with_tesseract(image_path):
    captcha_image = Image.open(image_path).convert("L")  # Escala de grises
    captcha_image = captcha_image.filter(ImageFilter.MedianFilter())  # Reducir ruido
    captcha_image = ImageOps.autocontrast(captcha_image)  # Aumentar contraste
    captcha_image = captcha_image.point(lambda x: 0 if x < 128 else 255)  # Binarización
    captcha_image.save("processed_tesseract.png")  # Guardar la imagen procesada (opcional)
    return pytesseract.image_to_string(captcha_image, config='--psm 8').strip()

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

# Ingresar apellidos y número de identificación
apellido_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:apellidos"]')
apellido_input.send_keys("Pérez")  # Cambia esto por el apellido deseado
identificacion_input = driver.find_element(By.XPATH, '//input[@id="formPrincipal:identificacion"]')
identificacion_input.send_keys("1234567890")  # Cambia esto por la identificación deseada

# Intentar resolver el captcha
for attempt in range(MAX_ATTEMPTS):
    # Capturar el captcha
    captcha_element = driver.find_element(By.XPATH, '//img[@id="formPrincipal:capimg"]')
    captcha_path = os.path.join(CAPTCHA_SAVE_DIR, f"captcha_attempt_{attempt}.png")
    captcha_element.screenshot(captcha_path)

    # Usar Tesseract para predecir el texto
    predicted_text = predict_with_tesseract(captcha_path)
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
    if "resultado esperado" in driver.page_source:  # Cambia según el texto esperado en la página
        print("Captcha resuelto correctamente.")
        break
else:
    print("No se pudo resolver el captcha después de varios intentos.")

# Cerrar el navegador
driver.quit()
