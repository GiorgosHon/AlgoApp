import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv
import os
from datetime import datetime


class AlgoTabWindow():

    def __init__(self, inventory):
        self.inventory = inventory
        self.window = tk.Tk()
        self.window.configure(background="black")
        self.window.title("Algo Tab")
        self.window.geometry("920x700")
        self.total_value = self.inventory.get_total_inventory_value()
        self.current_total = self.inventory.starting_balance

        # Store labels that need to be updated
        self.balance_label = None
        self.inventory_label = None
        self.quantity_labels = {}

        self._create_widgets()

    def _create_widgets(self):
        # Header
        header = tk.Frame(self.window, bg="black", height=20)
        header.pack()
        tk.Label(header, text="Algo Tab", font=("Arial", 20, "bold"),
                 bg="black", fg="white").pack(pady=10)

        # Starting balance info
        info_frame = tk.Frame(self.window, bg="black")
        info_frame.pack(padx=20, pady=5)
        tk.Label(info_frame, text=f"Αρχικό Ταμείο: €{self.inventory.starting_balance:.2f}",
                 font=("Arial", 12), bg="black", fg="cyan").pack(anchor="w", pady=5)

        # Product menu
        self._create_menu()

        # Totals display
        self._create_totals()

        # Action buttons
        button_frame = tk.Frame(self.window, bg="black")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="💾 Εξαγωγή CSV", command=self.confirm_export_to_csv,
                  font=("Arial", 13, "bold"), bg="green", fg="white",
                  width=18, height=2).pack(side="left", padx=5)

        tk.Button(button_frame, text="❌ Κλείσιμο", command=self.close_app,
                  font=("Arial", 13, "bold"), bg="red", fg="white",
                  width=18, height=2).pack(side="left", padx=5)

    def _create_menu(self):
        # Create canvas for scrolling
        canvas = tk.Canvas(self.window, bg="black", highlightthickness=0, height=400)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        product_container = tk.Frame(canvas, bg="black")

        product_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=product_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        product_frame = tk.Frame(product_container, bg="black")
        product_frame.pack(padx=10, pady=10)

        # Header row
        tk.Label(product_frame, text="Προϊόν", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        tk.Label(product_frame, text="Τιμή", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=1, padx=10, pady=8)
        tk.Label(product_frame, text="Πώληση", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=2, columnspan=2, padx=10, pady=8)
        tk.Label(product_frame, text="Απόθεμα", font=("Arial", 12, "bold"),
                 bg="black", fg="white").grid(row=0, column=4, padx=10, pady=8)

        current_row = 1
        for product in self.inventory.products:
            # Product name
            tk.Label(product_frame, text=product.name, font=("Arial", 13),
                     bg="black", fg="white").grid(row=current_row, column=0,
                                                  padx=10, pady=5, sticky="w")

            # Price
            tk.Label(product_frame, text=f"€{product.price:.2f}", font=("Arial", 13),
                     bg="black", fg="cyan").grid(row=current_row, column=1, padx=10, pady=5)

            # Plus button (sell/add to tab)
            plus_btn = tk.Button(product_frame, text="+",
                                 command=lambda p=product: self.add_to_tab(p),
                                 font=("Arial", 14), bg="green", fg="white", width=4, height=1)
            plus_btn.grid(row=current_row, column=2, padx=2, pady=5)

            # Minus button (return/remove from tab)
            # minus_btn = tk.Button(product_frame, text="-",
            #                       command=lambda p=product: self.add_to_tab(p),
            #                       font=("Arial", 14), bg="red", fg="white", width=4, height=1)
            # minus_btn.grid(row=current_row, column=3, padx=2, pady=5)

            # Quantity label
            quantity_label = tk.Label(product_frame, text=str(product.quantity),
                                      font=("Arial", 14, "bold"), bg="black", fg="yellow",
                                      width=6)
            quantity_label.grid(row=current_row, column=4, padx=10, pady=5)
            self.quantity_labels[product.name] = quantity_label

            current_row += 1

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        # scrollbar.pack(side="right", fill="y")

    def _create_totals(self):
        totals_frame = tk.Frame(self.window, bg="black", relief="ridge", borderwidth=2)
        totals_frame.pack(padx=20, pady=15, fill="x")

        # Inventory value label
        self.inventory_label = tk.Label(totals_frame,
                                        text=f"Συνολική Αξία Αποθέματος: €{self.total_value:,.2f}",
                                        font=("Arial", 14, "bold"), bg="black", fg="cyan")
        self.inventory_label.pack(pady=8)

        # Current balance label
        self.balance_label = tk.Label(totals_frame,
                                      text=f"Τρέχον Ταμείο: €{self.current_total:,.2f}",
                                      font=("Arial", 14, "bold"),
                                      bg="black",
                                      fg="green" if self.current_total >= 0 else "red")
        self.balance_label.pack(pady=8)

    def add_to_tab(self, product):
        """Sell product - decrease inventory, increase balance"""
        if product.quantity > 0:
            product.sell_product()
            self.update_total(product.price)
            self.update_displays()
        else:
            messagebox.showwarning("Μη Διαθέσιμο",
                                   f"Δεν υπάρχει απόθεμα για {product.name}!")

    def remove_from_tab(self, product):
        """Return product - increase inventory, decrease balance"""
        product.buy_product()
        self.update_total(-product.price)
        self.update_displays()

    def update_total(self, price_change):
        """Update the current balance"""
        self.current_total += price_change

    def update_displays(self):
        """Update all dynamic labels"""
        # Update total inventory value
        self.total_value = self.inventory.get_total_inventory_value()
        self.inventory_label.config(
            text=f"Συνολική Αξία Αποθέματος: €{self.total_value:,.2f}")

        # Update current balance with color coding
        self.balance_label.config(
            text=f"Τρέχον Ταμείο: €{self.current_total:,.2f}",
            fg="green" if self.current_total >= 0 else "red"
        )

        # Update all quantity labels
        for product in self.inventory.products:
            if product.name in self.quantity_labels:
                self.quantity_labels[product.name].config(text=str(product.quantity))

    def close_app(self):
        """Close the application with confirmation"""
        confirm = messagebox.askokcancel("Κλείσιμο Εφαρμογής",
                                         "Είσαι σίγουρος ότι θέλεις να κλείσεις την εφαρμογή;")
        if confirm:
            self.window.destroy()

    def confirm_export_to_csv(self):
        """Ask for confirmation before exporting to CSV"""
        confirm = messagebox.askokcancel("Επιβεβαίωση Εξαγωγής",
                                         "Θέλεις να εξάγεις τα δεδομένα σε CSV;")
        if confirm:
            self.export_to_csv_with_dialog()

    def export_to_csv_with_dialog(self):

        # Get user's home directory
        user_home = os.path.expanduser("~")

        # Create base directory in Documents
        base_dir = os.path.join(user_home, "Documents", "AlgoTab_Data")
        # Get the current date info
        current_datetime = datetime.now()
        year = current_datetime.strftime("%Y")
        month = current_datetime.strftime("%Y-%m_%B")  # e.g. 2025-11_November
        date_time_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    
        # Create folder structure
        export_dir = os.path.join(base_dir, year, month)
        try:
            os.makedirs(export_dir, exist_ok=True)
        except Exception :
            messagebox.showerror("Error", f"Αδυναμία δημιουργίας φακέλου:\n{str(e)}")
            return
        
        file_name = f"algo_tab_{date_time_string}.csv"
        file_path = os.path.join(export_dir, file_name)

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Προϊόν", "Ποσότητα", "Τιμή μονάδας", "Συνολική αξία"])

                for product in self.inventory.products:
                    total_value = product.get_total_value()
                    csv_writer.writerow([
                        product.name,
                        product.quantity,
                        f"€{product.price:.2f}",
                        f"€{total_value:.2f}"
                    ])

                csv_writer.writerow(["", "", "", ""])

                csv_writer.writerow(["Αρχικό  Ταμείο", "", "", f"€{self.inventory.starting_balance:.2f}"])
                csv_writer.writerow(["Τελικό Ταμείο", "", "", f"€{self.current_total:.2f}"])
                csv_writer.writerow(["Συνολική Αξία αποθέματος", "", "", f"€{self.total_value:.2f}"])

                messagebox.showinfo("Επιτυχία", f"Το αρχειο αποθηκεύτηκε επιτυχώς\n\n{file_path}")


        except Exception as e:
            messagebox.showerror()


    def show(self):
        """Start the main event loop"""
        self.window.mainloop()