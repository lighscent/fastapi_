from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import dotenv, os, time, winsound

dotenv.load_dotenv()


def send_whatsapp_message(phone_number, message):
    # Lancer Chrome avec Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=./chrome-data")  # garde ta session QR
    options.add_argument(r"--user-data-dir=C:\whatsapp-selenium-profile")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # Ouvrir WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    print("➡️ Scan le QR code si nécessaire…")

    # Attendre que WhatsApp soit chargé
    time.sleep(7)

    # Ouvrir la conversation
    driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
    time.sleep(5)

    # Trouver la zone de saisie
    # input_box = driver.find_element(
    #     By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"
    # )
    # AUTRE SELECTEUR FIABLE
    input_box = driver.find_element(
        By.XPATH, "//footer//div[@contenteditable='true' and @role='textbox']"
    )

    # IMPORTANT : Cliquer pour activer le focus interne (not yet utile actuellement)
    # input_box.click()
    # time.sleep(0.5)

    # Envoyer le message
    input_box.send_keys(message)
    time.sleep(12)

    input_box.send_keys(Keys.ENTER)
    print("✔ Message envoyé !")
    time.sleep(12)

    # Optionnel : fermer le navigateur
    # driver.quit()


# Exemple d'utilisation
dateNow = datetime.now().strftime("%H:%M:%S")
phone_number = os.getenv("MY_GSM_NUMBER")
message = f"{dateNow} - Hello depuis Georges !"

winsound.Beep(1000, 500)
print(f"{message} ➡️ {phone_number} via WhatsApp…")

send_whatsapp_message(phone_number, message)
winsound.Beep(1000, 500)
