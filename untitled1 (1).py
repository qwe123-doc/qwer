import tkinter as tk
from tkinter import ttk, messagebox
import json

# Создаем основное окно
root = tk.Tk()
root.title("Movie Library")

# -> Поля для ввода данных
fields_frame = tk.Frame(root)
fields_frame.pack(padx=10, pady=10)

# Название
tk.Label(fields_frame, text="Название").grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(fields_frame)
entry_title.grid(row=0, column=1, padx=5, pady=5)

# Жанр
tk.Label(fields_frame, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
entry_genre = tk.Entry(fields_frame)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

# Год выпуска
tk.Label(fields_frame, text="Год выпуска").grid(row=0, column=2, padx=5, pady=5)
entry_year = tk.Entry(fields_frame)
entry_year.grid(row=0, column=3, padx=5, pady=5)

# Рейтинг
tk.Label(fields_frame, text="Рейтинг").grid(row=1, column=2, padx=5, pady=5)
entry_rating = tk.Entry(fields_frame)
entry_rating.grid(row=1, column=3, padx=5, pady=5)

# -> Таблица для отображения фильмов
columns = ("title", "genre", "year", "rating")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.pack(padx=10, pady=10, fill='both', expand=True)

# -> Кнопки для добавления и фильтрации
buttons_frame = tk.Frame(root)
buttons_frame.pack(padx=10, pady=10)

btn_add = tk.Button(buttons_frame, text="Добавить фильм")
btn_add.grid(row=0, column=0, padx=5)

# Фильтры
tk.Label(buttons_frame, text="Фильтр по жанру").grid(row=0, column=1, padx=5)
entry_filter_genre = tk.Entry(buttons_frame)
entry_filter_genre.grid(row=0, column=2, padx=5)

tk.Label(buttons_frame, text="Фильтр по году").grid(row=0, column=3, padx=5)
entry_filter_year = tk.Entry(buttons_frame)
entry_filter_year.grid(row=0, column=4, padx=5)

btn_filter_genre = tk.Button(buttons_frame, text="Фильтр жанр")
btn_filter_year = tk.Button(buttons_frame, text="Фильтр год")
btn_clear_filters = tk.Button(buttons_frame, text="Сбросить фильтры")
btn_filter_genre.grid(row=0, column=5, padx=5)
btn_filter_year.grid(row=0, column=6, padx=5)
btn_clear_filters.grid(row=0, column=7, padx=5)

# -> Кнопки для сохранения и загрузки
save_load_frame = tk.Frame(root)
save_load_frame.pack(padx=10, pady=5)

btn_save = tk.Button(save_load_frame, text="Сохранить") 
btn_load = tk.Button(save_load_frame, text="Загрузить")
btn_save.pack(side=tk.LEFT, padx=5)
btn_load.pack(side=tk.LEFT, padx=5)

# -> Функции

# Добавление фильма
def add_movie():
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()

    # Проверка заполненности
    if not (title and genre and year and rating):
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    # Проверка года
    if not year.isdigit():
        messagebox.showerror("Ошибка", "Год должен быть числом")
        return
    year_int = int(year)

    # Проверка рейтинга
    try:
        rating_float = float(rating)
        if not (0 <= rating_float <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
        return

    # Добавление в таблицу
    tree.insert('', 'end', values=(title, genre, year_int, rating_float))
    # Очистка полей
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

btn_add.config(command=add_movie)

# Фильтрация по жанру
def filter_by_genre():
    genre_filter = entry_filter_genre.get().lower()
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if genre_filter in values[1].lower():
            tree.reattach(item, '', 'end')
        else:
            tree.detach(item)

# Фильтрация по году
def filter_by_year():
    year_filter = entry_filter_year.get()
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values[2] == year_filter:
            tree.reattach(item, '', 'end')
        else:
            tree.detach(item)

# Сброс фильтров
def reset_filters():
    for item in tree.get_children():
        tree.reattach(item, '', 'end')

btn_filter_genre.config(command=filter_by_genre)
btn_filter_year.config(command=filter_by_year)
btn_clear_filters.config(command=reset_filters)

# Сохранение данных
def save_to_json(filename="movies.json"):
    data = []
    for item in tree.get_children():
        data.append(tree.item(item, 'values'))
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Загрузка данных
def load_from_json(filename="movies.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Очистить таблицу
        for item in tree.get_children():
            tree.delete(item)
        # Вставить загруженные
        for record in data:
            tree.insert('', 'end', values=record)
    except FileNotFoundError:
        messagebox.showinfo("Информация", "Файл movies.json не найден")

# Назначение кнопкам
btn_save.config(command=save_to_json)
btn_load.config(command=load_from_json)

# Запуск главного цикла
root.mainloop()