import tkinter as tk
from tkinter import simpledialog
from threading import Thread
from pynput import keyboard
import pyperclip
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

senha = None
pressed_keys = set()

# Atalho Ctrl + Ç
combination = {keyboard.Key.ctrl, keyboard.KeyCode(char='l')}

def pedir_senha():
    global senha
    root = tk.Tk()
    root.withdraw()
    senha = simpledialog.askstring("Senha", "Digite sua senha:", show='*')
    root.destroy()

def colar_senha():
    if senha:
        pyperclip.copy(senha)

def on_press(key):
    if key in combination:
        pressed_keys.add(key)
        if all(k in pressed_keys for k in combination):
            colar_senha()
    else:
        pressed_keys.clear()

def on_release(key):
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

def iniciar_escuta():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

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
    icon.menu = pystray.Menu(
        item('Sair', on_exit)
    )
    icon.run()

def main():
    pedir_senha()
    escuta_thread = Thread(target=iniciar_escuta, daemon=True)
    escuta_thread.start()
    criar_icone()

if __name__ == "__main__":
    main()
