import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import os
import time
import shutil
import subprocess
import sys
import logging
import re

# Configuració del registre
logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Funció per llistar fitxers
def llistar_fitxers():
    carpeta = filedialog.askdirectory()
    if carpeta:
        fitxers = os.listdir(carpeta)
        txt_sortida.delete(1.0, tk.END)
        txt_sortida.insert(tk.END, "\n".join(fitxers))
        logging.info("Fitxers llistats amb èxit.")

def eliminar_fitxers_antics(dies=None):
    directori = filedialog.askdirectory()
    if directori:
        try:
            if not dies:
                dies = int(simpledialog.askstring("Eliminar Fitxers", "Eliminar fitxers més antics que (dies):"))
            if dies <= 0:
                raise ValueError("Els dies han de ser un nombre positiu.")
            ara = time.time()
            for fitxer in os.listdir(directori):
                ruta = os.path.join(directori, fitxer)
                if os.path.isfile(ruta) and ara - os.path.getmtime(ruta) > dies * 86400:
                    os.remove(ruta)
            messagebox.showinfo("Esborrat", "Fitxers antics eliminats.")
            logging.info(f"Fitxers més antics que {dies} dies eliminats.")
        except ValueError as e:
            messagebox.showerror("Error", f"Introdueix un número vàlid. Error: {str(e)}")
            logging.error(f"Error al intentar eliminar fitxers antics: {str(e)}")

# Funció per obtenir informació del sistema
def info_sistema():
    info = f"Sistema Operatiu: {os.name}\n"
    info += f"Directori actual: {os.getcwd()}\n"
    # Obtenir informació de l'espai en disc
    espai_total, espai_usat, espai_llibre = shutil.disk_usage("/")
    espai_total_gb = espai_total / (1024**3)
    espai_usat_gb = espai_usat / (1024**3)
    espai_llibre_gb = espai_llibre / (1024**3)
    
    info += f"\nEspai en Disc:\n"
    info += f"Total: {espai_total_gb:.2f} GB\n"
    info += f"Usat: {espai_usat_gb:.2f} GB\n"
    info += f"Lliure: {espai_llibre_gb:.2f} GB\n"
    
    txt_sortida.delete(1.0, tk.END)
    txt_sortida.insert(tk.END, info + "\n")
    logging.info("Informació del sistema obtinguda.")

# Funció per crear backup
def crear_backup():
    carpeta = filedialog.askdirectory()
    if carpeta:
        copia_seguretat = shutil.make_archive("backup", "zip", carpeta)
        messagebox.showinfo("Èxit", f"Còpia de seguretat creada: {copia_seguretat}")
        logging.info(f"Còpia de seguretat creada: {copia_seguretat}")

# Funció per mostrar l'ajuda
def mostrar_ajuda():
    ajuda = """
    Paràmetres disponibles:
    -h: Mostra aquesta ajuda.
    -t XX: Elimina fitxers més antics que XX dies (XX > 0).
    -b XXXXXX: Modifica el color de fons de la finestra (hexadecimal).
    -x: Només es pot utilitzar la línia d'ordres (interfície gràfica deshabilitada).
    hackeao: Mostra text en color verd i fons negre.
    """
    print(ajuda)
    logging.info("Ajuda mostrada.")

# Validar color hexadecimal
def validar_hex_color(codi):
    if len(codi) != 6:
        return False
    for caracter in codi:
        if caracter not in "0123456789ABCDEFabcdef":
            return False
    return True


# Funció per aplicar el color de fons
def aplicar_color_fons(codi):
    if validar_hex_color(codi) == True:
        finestra.config(bg=f"#{codi}")
        logging.info(f"Color de fons canviat a #{codi}.")
    else:
        messagebox.showerror("Error", "Codi hexadecimal de color no vàlid.")
        logging.error("Codi hexadecimal de color no vàlid.")

# Funció per executar comandes de terminal
def executar_comanda():
    comanda = comanda_entry.get()
    try:
        resultat = subprocess.run(comanda, shell=True, capture_output=True, text=True)
        txt_sortida.delete(1.0, tk.END)
        txt_sortida.insert(tk.END, resultat.stdout + resultat.stderr)
        logging.info(f"Comanda executada: {comanda}")
    except Exception as e:
        logging.error(f"Error executant comanda: {e}")

# Configuració de la interfície gràfica
finestra = tk.Tk()
finestra.title("Gestor d'Administració del Sistema")
finestra.geometry("500x300")

frame_botons = tk.Frame(finestra)
frame_botons.pack(pady=10)

btn_llistar = tk.Button(frame_botons, text="Llistar Fitxers", command=llistar_fitxers)
btn_llistar.grid(row=0, column=0, padx=5, pady=5)

btn_eliminar = tk.Button(frame_botons, text="Eliminar Fitxers Antics", command=lambda: eliminar_fitxers_antics(dies=int(sys.argv[sys.argv.index("-t") + 1] if "-t" in sys.argv else 0)))
btn_eliminar.grid(row=0, column=1, padx=5, pady=5)

btn_info = tk.Button(frame_botons, text="Info Sistema", command=info_sistema)
btn_info.grid(row=1, column=0, padx=5, pady=5)

btn_backup = tk.Button(frame_botons, text="Crear Backup", command=crear_backup)
btn_backup.grid(row=1, column=1, padx=5, pady=5)

frame_cmd = tk.Frame(finestra)
frame_cmd.pack(pady=10)

comanda_entry = tk.Entry(frame_cmd, width=40)
comanda_entry.grid(row=0, column=0, padx=5)

tk.Button(frame_cmd, text="Executar", command=executar_comanda).grid(row=0, column=1, padx=5)

txt_sortida = scrolledtext.ScrolledText(finestra, height=10, width=60)
txt_sortida.pack(pady=10)

# Processar paràmetres de la línia d'ordres
if "-h" in sys.argv:
    mostrar_ajuda()
elif "-t" in sys.argv:
    dies = int(sys.argv[sys.argv.index("-t") + 1])
    if dies > 0:
        eliminar_fitxers_antics(dies)
    finestra.mainloop()
elif "-b" in sys.argv:
    color = sys.argv[sys.argv.index("-b") + 1]
    aplicar_color_fons(color)
    finestra.mainloop()
elif "-x" in sys.argv:
    # Deshabilitar els botons
    frame_botons.pack_forget()
    finestra.mainloop()
elif "hackeao" in sys.argv:
    frame_botons.pack_forget()
    txt_sortida.config(fg="green", bg="black", font=("arial", 30))
    txt_sortida.insert(tk.END, "Hackeado!!")
    logging.info("Hackeado activat.")
    finestra.mainloop()
else:
    finestra.mainloop()
