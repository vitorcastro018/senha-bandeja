import tkinter as tk
from tkinter import simpledialog
from threading import Thread
from pynput import keyboard
import pyperclip
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import pyautogui

senha = None
pressed_keys = set()
combination = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('l')}

def pedir_senha():
    global senha
    root = tk.Tk()
    root.withdraw()
    senha = simpledialog.askstring("Senha", "Digite sua senha:", show='*')
    root.destroy()

def colar_senha():
    if senha:
        pyperclip.copy(senha)
        pyautogui.typewrite(pyperclip.paste())

def on_press(key):
    pressed_keys.add(key)
    if all(k in pressed_keys for k in combination):
        colar_senha()

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

def iniciar_escuta():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def gerar_icone():
    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 30, 44, 50], fill='black')
    draw.arc([18, 10, 46, 38], start=0, end=180, fill='black', width=4)
    return img

def criar_icone():
    def on_exit(icon, item):
        global senha
        senha = None
        icon.stop()

    icon = pystray.Icon("SenhaAtalho")
    icon.icon = gerar_icone()
    icon.menu = pystray.Menu(item('Sair', on_exit))
    icon.run()

def main():
    pedir_senha()
    iniciar_escuta()
    criar_icone()

if __name__ == "__main__":
    main()
