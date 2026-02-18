from re import M
import pywhatkit as pyw
import dotenv, os, pyautogui, time
import winsound


dotenv.load_dotenv()

msg = "4 Hello world AUTO from pywhatkit!"
msg = "Kikoo... À la bonne tienne !"

timeminute = 13, 42  # ← Indiquer l'heure d'envoi ici

winsound.Beep(1000, 500)  # fréquence 1000 Hz, durée 500 ms
pyw.sendwhatmsg(os.getenv("MY_GSM_NUMBER"), msg, timeminute[0], timeminute[1])

time.sleep(12)

# cliquer dans la zone de saisie (coordonnées à ajuster) & pour trouver le bon endroit :
# python -c "import pyautogui, time; time.sleep(3); print(pyautogui.position())"
pyautogui.click(3794, 1043)


time.sleep(1)

pyautogui.press("enter")

print("Message sent!")
winsound.Beep(1000, 500)  # fréquence 1000 Hz, durée 500 ms
