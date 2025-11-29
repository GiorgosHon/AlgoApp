import tkinter as tk
from tkinter import messagebox


class StartingBalanceWindow():

    def __init__(self, on_complete_callback, saved_balance=0.0):
        self.saved_balance = saved_balance
        self.on_complete = on_complete_callback
        self.window = tk.Tk()
        self.window.configure(background="black")
        self.window.title("Starting Balance")
        self.window.geometry("350x200")

        self._create_widgets()

    def _create_widgets(self):
        # Header
        tk.Label(self.window, text="Αρχικό Ταμείο",
                 font=("Arial", 18, "bold"), bg="black", fg="white").pack(pady=15)

        # Show saved balance if exists
        if self.saved_balance > 0:
            tk.Label(self.window, text=f"Προηγούμενο: €{self.saved_balance:.2f}",
                     font=("Arial", 11), bg="black", fg="cyan").pack(pady=2)

        # Entry frame
        entry_frame = tk.Frame(self.window, bg="black")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="€", font=("Arial", 16),
                 bg="black", fg="cyan").pack(side="left", padx=5)

        self.entry = tk.Entry(entry_frame, font=("Arial", 16), width=12,
                              justify="center", bg="white", fg="black")
        self.entry.pack(side="left")
        self.entry.insert(0, "0")
        self.entry.focus()
        self.entry.select_range(0, tk.END)

        # Button
        tk.Button(self.window, text="Συνέχεια →", command=self._on_next,
                  font=("Arial", 14, "bold"), bg="green", fg="white",
                  width=15).pack(pady=15)

        # Bind Enter key - FIXED: added () to actually call the function
        self.window.bind('<Return>', lambda e: self._on_next())

    def _on_next(self):
        try:
            value = float(self.entry.get())
            if value < 0:
                messagebox.showerror("Σφάλμα", "Το ποσό δεν μπορεί να είναι αρνητικό!")
                return

            self.window.destroy()
            self.on_complete(value)

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρο αριθμό!")

    def show(self):
        self.window.mainloop()