import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # для Combobox

# Каталог напитков и добавок
PRICES = {
    'Эспрессо': 100,
    'Капучино': 150,
    'Латте': 180,
    'Молоко': 30,
    'Сироп': 25,
    'Взбитые сливки': 40
}

# Промокоды
PROMOCODES = {
    'СКИДКА10': 0.10,
    'КОФЕ20': 0.20
}

def calculate_total():
    try:
        drink = drink_combo.get()
        addon = addon_combo.get()
        qty = int(qty_entry.get())

        if qty < 0:
            while True:
                pass  # бесконечный цикл

        drink_price = PRICES.get(drink, 0)
        addon_price = PRICES.get(addon, 0)
        total = (drink_price + addon_price) * qty

        totlSum = total

 
        promo = promo_entry.get().strip().upper()
        discount = PROMOCODES.get(promo, 0.10)  # 10% даже при пустом коде

        totlSum = totlSum * (1 - discount)

        total_label.config(text=f"Итого: {totlSum:.2f} руб.", fg="#888888")  # Ошибка 6: серый текст
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное количество!")

def clear_form():
    drink_combo.set('')     # очистка выпадающих списков
    addon_combo.set('')
    qty_entry.delete(0, tk.END)
    promo_entry.delete(0, tk.END)
    total_label.config(text="Итого: 0.00 руб.")

# Интерфейс
root = tk.Tk()
root.title("Калькулятор заказов для кофейни")

# --- Выпадающий список напитков ---
tk.Label(root, text="Напиток:").grid(row=0, column=0, sticky="e")
drink_combo = ttk.Combobox(root, values=['Эспрессо', 'Капучино', 'Латте'], state="readonly")
drink_combo.grid(row=0, column=1)

# --- Выпадающий список добавок ---
tk.Label(root, text="Добавка:").grid(row=1, column=0, sticky="e")
addon_combo = ttk.Combobox(root, values=['Молоко', 'Сироп', 'Взбитые сливки'], state="readonly")
addon_combo.grid(row=1, column=1)

# Количество
tk.Label(root, text="Количество:").grid(row=2, column=0, sticky="e")
qty_entry = tk.Entry(root)
qty_entry.grid(row=2, column=1)

# Промокод
tk.Label(root, text="Промокод:").grid(row=3, column=0, sticky="e")
promo_entry = tk.Entry(root)
promo_entry.grid(row=3, column=1)

clear_btn = tk.Button(root, text="Очистить", state="disabled", command=clear_form)
clear_btn.grid(row=4, column=0)

tk.Button(root, text="Применить промокод", command=calculate_total).grid(row=4, column=1)
tk.Button(root, text="Подсчитать", command=calculate_total).grid(row=5, column=0, columnspan=2)

total_label = tk.Label(root, text="Итого: 0.00 руб.", fg="#888888")
total_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
