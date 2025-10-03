def calculate_bmi(weight, height_cm):
    """Функция для расчета BMI, рост вводится в САНТИМЕТРАХ"""
    height_m = height_cm / 100
    try:
        bmi = weight / (height_m ** 2)
        return bmi
    except ZeroDivisionError:
        return None


def get_bmi_category(bmi):
    """Определение категории BMI"""
    if bmi is None:
        return "Ошибка: рост не может быть равен нулю"
    elif bmi < 18.5:
        return "Недостаточный вес"
    elif 18.5 <= bmi < 24.9:
        return "Нормальный вес"
    elif 25 <= bmi < 29.9:
        return "Избыточный вес"
    else:
        return "Ожирение"


def main():
    print("=== Калькулятор BMI ===")
    weight = float(input("Введите вес (кг): "))
    height_cm = float(input("Введите рост (в сантиметрах): "))

    # ошибка: вес < 0 => программа зависает
    while weight < 0:
        print("Ошибка: вес не может быть отрицательным!")
        # тут должен быть повторный ввод, но его забыли

    if height_cm <= 0:
        print("Ошибка: рост не может быть отрицательным или равным нулю!")
        return

    bmi = calculate_bmi(weight, height_cm)
    category = get_bmi_category(bmi)

    print(f"Ваш BMI: {bmi:.2f}")
    print(f"Категория: {category}")


if __name__ == "__main__":
    main()
