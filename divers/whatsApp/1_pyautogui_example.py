import pywhatkit as pyw
import dotenv, os, pyautogui, time
import winsound
from datetime import datetime

dotenv.load_dotenv()

# dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
dateNow = datetime.now().strftime("%H:%M:%S")
print(dateNow)
msg = f"{dateNow} - Kikoo... À la bonne tienne !"
winsound.Beep(1000, 500)  # fréquence 1000 Hz, durée 500 ms

# timeminute = 13, 45  # ← Indiquer l'heure d'envoi ici
# pyw.sendwhatmsg(os.getenv("MY_GSM_NUMBER"), msg, timeminute[0], timeminute[1]) # Envoi programmé à une heure précise

pyw.sendwhatmsg_instantly(os.getenv("MY_GSM_NUMBER"), msg, tab_close=False)
pyautogui.click(3794, 1043)
# cliquer dans la zone de saisie (coordonnées à ajuster) & pour trouver le bon endroit :
# python -c "import pyautogui, time; time.sleep(3); print(pyautogui.position())"
print("Message sent!")
winsound.Beep(1000, 500)  # fréquence 1000 Hz, durée 500 ms




# exit()
# Effet de bord indésiré: Ajout d'une ligne si lancement depuis l'éditeur avec Win + VSC
# pyautogui.press("esc")
# os.system("notepad.exe")
# pyautogui.click(2953, 572)
# pyautogui.hotkey("alt", "tab")  # amène le navigateur au premier plan
# print("ini")
# # time.sleep(10)
# print("fin attente")
# pyautogui.press("tab")
# print("fin tab 1")
# pyautogui.press("tab")
# print("fin tab 2")
# print("clic")
# pyautogui.hotkey("alt", "tab")
# pyautogui.press("enter")
# time.sleep(1)
