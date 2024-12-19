import pyautogui
import time
import threading
import customtkinter as ctk
from tkinter import messagebox


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AutoClicker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Clicker Moderno")
        self.geometry("550x550")
        self.resizable(False, False)


        self.x = ctk.StringVar(value="0")
        self.y = ctk.StringVar(value="0")
        self.num_clicks = ctk.StringVar(value="10")
        self.interval = ctk.StringVar(value="1.0")


        self.title_label = ctk.CTkLabel(self, text="Auto Clicker", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)


        self.coord_frame = ctk.CTkFrame(self)
        self.coord_frame.pack(pady=10, padx=20, fill="x")


        self.x_label = ctk.CTkLabel(self.coord_frame, text="Coordenada X:")
        self.x_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.x_entry = ctk.CTkEntry(self.coord_frame, textvariable=self.x)
        self.x_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")


        self.y_label = ctk.CTkLabel(self.coord_frame, text="Coordenada Y:")
        self.y_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.y_entry = ctk.CTkEntry(self.coord_frame, textvariable=self.y)
        self.y_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")


        self.capture_button = ctk.CTkButton(self, text="Capturar Posição do Mouse", command=self.capture_position)
        self.capture_button.pack(pady=10)


        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=10, padx=20, fill="x")


        self.num_label = ctk.CTkLabel(self.config_frame, text="Número de Cliques:")
        self.num_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.num_entry = ctk.CTkEntry(self.config_frame, textvariable=self.num_clicks)
        self.num_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")


        self.interval_label = ctk.CTkLabel(self.config_frame, text="Intervalo (segundos):")
        self.interval_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.interval_entry = ctk.CTkEntry(self.config_frame, textvariable=self.interval)
        self.interval_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")


        self.start_button = ctk.CTkButton(self, text="Iniciar Automação", command=self.start_clicking, fg_color="#4CAF50")
        self.start_button.pack(pady=20)


        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.pack(pady=5)

    def capture_position(self):
        self.status_label.configure(text="Capturando posição em 5 segundos...")
        self.update_idletasks()
        time.sleep(5)
        x, y = pyautogui.position()
        self.x.set(str(x))
        self.y.set(str(y))
        self.status_label.configure(text=f"Posição capturada: X={x}, Y={y}")

    def start_clicking(self):
        try:
            x = int(self.x.get())
            y = int(self.y.get())
            num = int(self.num_clicks.get())
            interval = float(self.interval.get())
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, insira valores válidos.")
            return

        if x == 0 and y == 0:
            messagebox.showwarning("Coordenadas Não Definidas", "Capture a posição do mouse antes de iniciar.")
            return

        confirm = messagebox.askyesno("Confirmar", f"Iniciar {num} cliques em ({x}, {y}) a cada {interval} segundos?")
        if confirm:
            self.start_button.configure(state="disabled")
            self.status_label.configure(text="Automação iniciada...")
            threading.Thread(target=self.click, args=(x, y, num, interval), daemon=True).start()

    def click(self, x, y, num_clicks, interval):
        try:
            for i in range(num_clicks):
                pyautogui.click(x, y)
                self.status_label.configure(text=f"Clique {i+1} de {num_clicks} realizado.")
                time.sleep(interval)
            self.status_label.configure(text="Automação concluída.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            self.start_button.configure(state="normal")

if __name__ == "__main__":
    app = AutoClicker()
    app.mainloop()
