import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re
from typing import List


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("500x400")

        self.setup_ui()

    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        title_label = ttk.Label(main_frame, text="Генератор и анализатор паролей",
                                font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Параметры генерации
        params_frame = ttk.LabelFrame(main_frame, text="Параметры пароля", padding="10")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Длина пароля
        ttk.Label(params_frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W)
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(params_frame, from_=6, to=50, textvariable=self.length_var, width=10)
        length_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # Типы символов
        self.uppercase_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Заглавные буквы (A-Z)",
                        variable=self.uppercase_var).grid(row=1, column=0, sticky=tk.W)

        self.lowercase_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Строчные буквы (a-z)",
                        variable=self.lowercase_var).grid(row=2, column=0, sticky=tk.W)

        self.digits_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Цифры (0-9)",
                        variable=self.digits_var).grid(row=1, column=1, sticky=tk.W)

        self.symbols_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Спецсимволы (!@#$%)",
                        variable=self.symbols_var).grid(row=2, column=1, sticky=tk.W)

        # Кнопки управления
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="Сгенерировать пароль",
                   command=self.generate_password).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(buttons_frame, text="Проверить сложность",
                   command=self.check_password_strength).pack(side=tk.LEFT)

        # Поле для ввода/вывода пароля
        ttk.Label(main_frame, text="Пароль:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=40, font=("Arial", 10))
        password_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 10))

        # Результат проверки сложности
        self.strength_var = tk.StringVar(value="Введите пароль для проверки сложности")
        strength_label = ttk.Label(main_frame, textvariable=self.strength_var,
                                   font=("Arial", 10))
        strength_label.grid(row=5, column=0, columnspan=2, pady=5)

        # История паролей
        history_frame = ttk.LabelFrame(main_frame, text="История паролей", padding="10")
        history_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.history_listbox = tk.Listbox(history_frame, height=6, font=("Arial", 9))
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

        # Привязка события для копирования пароля из истории
        self.history_listbox.bind("<Double-1>", self.copy_from_history)

    def generate_password(self) -> str:
        """Генерация случайного пароля с заданными параметрами"""
        length = self.length_var.get()

        # Создание пула символов на основе выбранных опций
        char_pool = ""
        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        if self.digits_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Проверка, что выбран хотя бы один тип символов
        if not char_pool:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return ""

        # Генерация пароля
        password = ''.join(random.choice(char_pool) for _ in range(length))

        # Обновление интерфейса
        self.password_var.set(password)
        self.add_to_history(password)
        self.check_password_strength()

        return password

    def check_password_strength(self) -> str:
        """Проверка сложности пароля и вывод результата"""
        password = self.password_var.get()

        if not password:
            self.strength_var.set("Введите пароль для проверки сложности")
            return "weak"

        score = 0
        feedback = []

        # Проверка длины
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Слишком короткий пароль")

        # Проверка на наличие разных типов символов
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Добавьте строчные буквы")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")

        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Добавьте цифры")

        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")

        # Определение уровня сложности
        if score >= 5:
            strength = "Очень сильный"
            color = "green"
        elif score >= 4:
            strength = "Сильный"
            color = "blue"
        elif score >= 3:
            strength = "Средний"
            color = "orange"
        else:
            strength = "Слабый"
            color = "red"

        result = f"Сложность: {strength} (оценка: {score}/6)"
        if feedback:
            result += f"\nРекомендации: {', '.join(feedback)}"

        self.strength_var.set(result)
        return strength.lower()

    def add_to_history(self, password: str):
        """Добавление пароля в историю"""
        # Ограничиваем историю 10 последними паролями
        items = list(self.history_listbox.get(0, tk.END))
        if password not in items:
            items.insert(0, password)
            if len(items) > 10:
                items = items[:10]

            self.history_listbox.delete(0, tk.END)
            for item in items:
                self.history_listbox.insert(tk.END, item)

    def copy_from_history(self, event):
        """Копирование выбранного пароля из истории в основное поле"""
        selection = self.history_listbox.curselection()
        if selection:
            password = self.history_listbox.get(selection[0])
            self.password_var.set(password)
            self.check_password_strength()

    def calculate_entropy_buggy(self, password: str) -> float:
        """
        Функция с преднамеренной ошибкой для расчета энтропии пароля.
        ОШИБКА: неправильный расчет мощности алфавита
        """
        if not password:
            return 0.0

        # Определение мощности алфавита (НЕПРАВИЛЬНО!)
        char_types = 0
        if any(c.islower() for c in password):
            char_types += 26  # Ошибка: должно быть len(string.ascii_lowercase)
        if any(c.isupper() for c in password):
            char_types += 26  # Ошибка: должно быть len(string.ascii_uppercase)
        if any(c.isdigit() for c in password):
            char_types += 10  # Ошибка: должно быть len(string.digits)
        if any(not c.isalnum() for c in password):
            char_types += 10  # Ошибка: произвольное число вместо реального количества спецсимволов

        # Расчет энтропии
        entropy = len(password) * (char_types ** 0.5)  # Ошибка: неправильная формула

        return entropy


def main():
    """Основная функция для запуска приложения"""
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()