import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

class AplikasiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Item")
        self.root.geometry("400x100")
        self.root.configure(bg='#87CEEB')

        self.items = []

        self.tambah_button = tk.Button(root, text="Tambah Item", command=self.tambah_item)
        self.tambah_button.pack(pady=5)

        self.cari_button = tk.Button(root, text="Cari Item", command=self.cari_item)
        self.cari_button.pack(pady=5)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="your_user",
            password="your_password",
            database="kelompok"
        )

        self.cursor = self.db_connection.cursor()

        self.create_table()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

    def tambah_item(self):
        nama_item = simpledialog.askstring("Tambah Item", "Masukkan Item:")
        if nama_item:
            harga_item = simpledialog.askfloat("Tambah Item", "Masukkan Harga ayamma:")
            if harga_item is not None:
                self.insert_item(nama_item, harga_item)
                self.items.append({"nama": nama_item, "harga": harga_item})
                messagebox.showinfo("Info", f"Item '{nama_item}' dengan harga {harga_item} berhasil ditambahkan.")

    def insert_item(self, name, price):
        insert_query = "INSERT INTO items (name, price) VALUES (%s, %s)"
        data = (name, price)
        self.cursor.execute(insert_query, data)
        self.db_connection.commit()

    def cari_item(self):
        nama_item_dicari = simpledialog.askstring("Cari Item", "Masukkan Nama Item yang Dicari:")
        if nama_item_dicari:
            items_ditemukan = self.get_items_by_name(nama_item_dicari)
            if items_ditemukan:
                info = "\n".join([f"{item[1]}: {item[2]}" for item in items_ditemukan])
                messagebox.showinfo("Info", f"Item '{nama_item_dicari}' ditemukan:\n{info}")
            else:
                messagebox.showinfo("Info", f"Item '{nama_item_dicari}' tidak ditemukan.")

    def get_items_by_name(self, name):
        select_query = "SELECT * FROM items WHERE name = %s"
        self.cursor.execute(select_query, (name,))
        return self.cursor.fetchall()

if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = AplikasiGUI(root)
    root.mainloop()
