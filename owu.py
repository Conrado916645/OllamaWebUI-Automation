import subprocess
import logging
import pystray
import PIL.Image
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, Toplevel, Label

image = PIL.Image.open("OpenWebUI_Ollama_Icon.png")

def show_loading(title, message):
    """Show a loading window that does not exit until closed manually."""
    root = tk.Tk()
    root.withdraw()
    loading_window = Toplevel()
    loading_window.title(title)
    Label(loading_window, text=message, padx=20, pady=20).pack()
    loading_window.update()
    return loading_window

def on_clicked_about(icon, item):
    show_alert("About", f"OllamaWebUI v1.0.1")

def on_clicked_update(icon, item):
    """Check if 'open-webui' has an update available."""
    try:
        loading_window = show_loading("Checking for Updates", "Verifying if an update is available...")
        logging.info("Checking for updates...")
        result = subprocess.run(
            ['pip', 'install', '--upgrade', 'open-webui', '--dry-run'],
            capture_output=True, text=True
        )
        loading_window.destroy()
        if "Requirement already satisfied" not in result.stdout:
            logging.info("Update available! Updating...")
            updating_window = show_loading("Update Available", "Updating open-webui...")
            subprocess.run(['pip', 'install', '--upgrade', 'open-webui'])
            updating_window.destroy()
            logging.info("Update installed successfully.")
            show_alert("Update Installed", "open-webui has been updated successfully.")
        else:
            logging.info("No update available.")
            show_alert("No Update", "open-webui is already up to date.")
    except Exception as e:
        logging.error(f"Error checking for update: {e}")
        show_alert("Update Error", f"Error checking for update: {e}")

def run_open_webui():
    """Run open-webui serve in the background."""
    loading_window = show_loading("Starting..", "Opening Open-webui...")
    logging.info("Starting open-webui server...")
    subprocess.Popen(['open-webui', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logging.info("Open-webui Started.")
    loading_window.destroy()

def show_alert(title, message):
    """Show an alert message box and properly close it when clicking OK."""
    root = tk.Tk()
    root.withdraw()
    alert_window = Toplevel()
    alert_window.title(title)
    Label(alert_window, text=message, padx=20, pady=20).pack()
    tk.Button(alert_window, text="OK", command=alert_window.destroy).pack()
    alert_window.mainloop()

def on_clicked_exit(icon, item):
    icon.stop()

icon = pystray.Icon("Neural", image,
 menu=pystray.Menu(
    pystray.MenuItem("Update WebUI", on_clicked_update),
    pystray.MenuItem("About", on_clicked_about),
    pystray.MenuItem("Exit", on_clicked_exit),
    ))

run_open_webui()
icon.run()