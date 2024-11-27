#!/usr/bin/env python3

import random
import tkinter as tk
from PIL import Image, ImageTk
import configparser

class RadVanFortuinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Not Any Other Weekend 2024 - Rad van Fortuin")
        self.root.geometry("600x400")
        self.root.configure(background="black")

        # Rijen en kolommen configureren om mee te schalen
        self.root.grid_rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Config en namen inlezen vanuit .ini bestand
        self.original_logo = Image.open("NAOW_logo.png")
        self.logo_afbeelding = ImageTk.PhotoImage(self.original_logo)
        
        self.create_widgets()
        self.toon_standaard_weergave()
        
        self.config = configparser.ConfigParser()
        self.config.read("namenlijst.ini")
        self.namen = self.laad_namen()

        self.kleuren = ["red", "orange", "yellow", "blue", "indigo", "violet"]
        self.draai_door = True

    def laad_namen(self):
        namen_string = self.config.get("namen", "lijst", fallback="")
        return [naam.strip() for naam in namen_string.splitlines() if naam.strip()]

    def sla_namen_op(self):
        namen_string = "\n".join(self.namen)
        self.config.set("namen", "lijst", "\n" + namen_string)
        with open("namenlijst.ini", "w") as configfile:
            self.config.write(configfile)

    def create_widgets(self):
        # Hoofdframe voor de naam met zwarte achtergrond
        self.naam_frame = tk.Frame(self.root, bg="black")
        self.naam_frame.grid(row=1, column=0, sticky="nsew")
        self.naam_frame.grid_rowconfigure(0, weight=1)
        self.naam_frame.grid_columnconfigure(0, weight=1)
        
        # Label voor de naam met highlight mogelijkheid
        self.naam_label = tk.Label(self.naam_frame, text="", font=("Arial", 40), fg="green", bg="black", wraplength=1800, justify="center", borderwidth=5, relief="flat")
        self.naam_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.draai_knop = tk.Button(self.root, text="Draai het rad", command=self.draai_rad, font=("Arial", 15))
        self.reset_knop = tk.Button(self.root, text="Reset", command=self.reset, font=("Arial", 15), state="disabled")
        
        self.draai_knop.grid(row=2, column=0, sticky="SE", padx=10, pady=(10,5))
        self.reset_knop.grid(row=2, column=1, sticky="S", padx=10, pady=(10,5))

        # Frame voor de afbeelding
        self.logo_frame = tk.Frame(self.root, bg="black")
        self.logo_frame.grid(row=1, column=1, sticky="nsew")

        # Label voor het logo binnen het frame
        self.standaard_logo = tk.Label(self.logo_frame, image=self.logo_afbeelding, bg="black")
        self.standaard_logo.place(relx=0.5, rely=0.5, anchor="center")

        # Bind het resize-event aan het frame
        self.logo_frame.bind("<Configure>", self.resize_logo)

    def toon_standaard_weergave(self):
        self.naam_frame.grid_remove()
        self.logo_frame.grid(row=1, column=0, sticky="nsew")

    def verberg_standaard_weergave(self):
        self.logo_frame.grid_remove()
        self.naam_frame.grid()

    def resize_logo(self, event):
        frame_width, frame_height = event.width, event.height
        original_width, original_height = self.original_logo.size
        scale_factor = min(frame_width / original_width, frame_height / original_height)
        
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        resized_logo = self.original_logo.resize((new_width, new_height), Image.LANCZOS)
        self.logo_afbeelding = ImageTk.PhotoImage(resized_logo)
        self.standaard_logo.config(image=self.logo_afbeelding)

    def draai_rad(self):
        self.verberg_standaard_weergave()
        self.draai_door = True
        self.draai_knop.config(state="disabled")
        self.reset_knop.config(state="disabled")
        self.reset_highlight()
        self.draai_animatie(draai_tijd=50)

    def draai_animatie(self, draai_tijd):
        if not self.draai_door:
            return

        gekozen_naam = random.choice(self.namen)
        kleur = random.choice(self.kleuren)
        self.naam_label.config(text=gekozen_naam, font=("Arial", 175), fg=kleur)

        draai_tijd += 15
        if draai_tijd < 400:
            self.root.after(draai_tijd, lambda: self.draai_animatie(draai_tijd))
        else:
            winnaar_naam = random.choice(self.namen)
            self.toon_winnaar(winnaar_naam)

    def toon_winnaar(self, naam):
        self.draai_door = False
        self.naam_label.config(
            text=naam,
            font=("Arial", 190, "bold"),
            fg="#00ff00",
            relief="solid",  # Voegt een rand toe
            borderwidth=5,   # Dikte van de rand
            highlightbackground="#00ff00",
            highlightcolor="#00ff00",
            highlightthickness=15
        )
        self.reset_knop.config(state="normal")

    def reset(self):
        self.naam_label.config(
            text="",
            font=("Arial", 40),
            fg="black",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.draai_knop.config(state="normal")
        self.reset_knop.config(state="disabled")
        self.toon_standaard_weergave()

    def reset_highlight(self):
        self.naam_label.config(
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        
if __name__ == "__main__":
    root = tk.Tk()
    app = RadVanFortuinApp(root)
    root.mainloop()