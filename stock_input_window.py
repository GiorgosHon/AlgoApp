import tkinter as tk
from tkinter import messagebox


class StockInputWindow():

    def __init__(self, products, on_complete_callback):
        self.products = products
        self.on_complete = on_complete_callback
        self.window = tk.Tk()
        self.window.configure(background="black")
        self.window.title("Stock Input")
        self.window.geometry("600x550")

        self.unumbered_products = [
            "Καφές",
            "Φραπές",
            "Ποτό",
            "Σφηνάκι"
        ]
        self.stocked_products = []

        for product in self.products:
            self.stocked_products.append(product)

        for product in self.products:
            if product.name in self.unumbered_products:
                product.set_quantity(100)
                self.stocked_products.remove(product)

        print(self.stocked_products)
        self.entries = {}
        self._create_widgets()

    def _create_widgets(self):
        # Header
        tk.Label(self.window, text="Εισαγωγή Αποθέματος",
                 font=("Arial", 16, "bold"), bg="black", fg="white").pack(pady=15)

        # Create scrollable frame for products
        canvas = tk.Canvas(self.window, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Product entry grid
        frame = tk.Frame(scrollable_frame, bg="black")
        frame.pack(padx=10, pady=10)

        # Headers
        tk.Label(frame, text="Προϊόν", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame, text="Τιμή", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame, text="Ποσότητα", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=2, padx=10, pady=5)

        current_row = 1
        first_entry = None

        for product in self.stocked_products:

            # Product name
            tk.Label(frame, text=f"{product.name}", font=("Arial", 13),
                     bg="black", fg="white").grid(row=current_row, column=0,
                                                  padx=10, pady=5, sticky="w")

            # Product price
            tk.Label(frame, text=f"€{product.price:.2f}", font=("Arial", 13),
                     bg="black", fg="cyan").grid(row=current_row, column=1,
                                                 padx=10, pady=5)

            # Quantity entry
            entry = tk.Entry(frame, font=("Arial", 12), width=10,
                             justify="center", bg="white", fg="black")
            entry.grid(row=current_row, column=2, padx=10, pady=5)
            entry.insert(0, "0")
            self.entries[product] = entry

            if first_entry is None:
                first_entry = entry

            # Bind Enter key to move to next entry
            if current_row < len(self.stocked_products):
                entry.bind('<Return>', lambda e, r=current_row: self._focus_next(r))
            else:
                entry.bind('<Return>', lambda e: self.update_stock())

            current_row += 1

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        button_frame = tk.Frame(self.window, bg="black")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Επιβεβαίωση", command=self.update_stock,
                  font=("Arial", 14, "bold"), bg="green", fg="white",
                  width=15).pack(pady=5)

        tk.Button(button_frame, text="Μηδενισμός", command=self.reset_entries,
                  font=("Arial", 12), bg="orange", fg="white",
                  width=15).pack(pady=5)

        # Focus on first entry
        if first_entry:
            first_entry.focus()

    def _focus_next(self, current_row):
        """Move focus to next entry field"""
        products_list = list(self.entries.keys())
        if current_row < len(products_list):
            next_product = products_list[current_row]
            self.entries[next_product].focus()

    def reset_entries(self):
        """Reset all entries to 0"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        # Focus on first entry
        first_entry = list(self.entries.values())[0]
        first_entry.focus()

    def update_stock(self):
        """Update product quantities and proceed to next window"""
        try:
            for product, entry in self.entries.items():
                quantity = int(entry.get())
                if quantity < 0:
                    raise ValueError("Negative quantity")
                product.set_quantity(quantity)

            self.window.destroy()
            self.on_complete()

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρους αριθμούς για όλα τα προϊόντα!")

    def show(self):
        """Start the window main loop"""
        self.window.mainloop()