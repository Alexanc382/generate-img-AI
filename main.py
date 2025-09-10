from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from io import BytesIO
import requests
from PIL import Image, ImageTk
import asyncio
from g4f.client import AsyncClient


def get_text():
    text = search_image_entry.get() # получили текст от пользователя
    asyncio.run(main(text))


async def main(text):
    user_input = text # текст запроса
    if user_input:
        client = AsyncClient()
        response = await client.images.generate(
            prompt=user_input,
            model="flux",
            response_format="url"
            # Add any other necessary parameters
        )
        image_url = response.data[0].url
        get_image(image_url)
        print(f"Generated image URL: {image_url}")
    else:
        print('Ничего не ввели')


def get_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img_result = Image.open(image_data)
        img_result.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img_result)
        if photo:
            new_window = Toplevel()
            new_window.title('Картинка с котиком')
            new_window.geometry('600x480')
            # сюда нужно отправить картинку из апи
            new_label = ttk.Label(new_window)
            new_label.grid(row=4, column=0, padx=(50, 0))
            new_label.config(image=photo)
            new_label.image = photo
        else:
            mb.showerror(title='Ошибка', message='Повторите ваш запрос')
    except Exception as e:
        mb.showerror(title='Ошибка', message=f'Ошибка {e}')


window = Tk()
window.title('Сгенерируем картинку?')

# размер окна и параметры его отображения(посередине экрана)
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
width_position = screenwidth // 2 - 200
height_position = screenheight // 2 - 230
window.geometry(f'400x460+{width_position}+{height_position}')

# метки приветствия
label_1 = ttk.Label(text='Помогу тебе сгенерировать изображение')
label_1.grid(row=0, columnspan=2, padx=(80, 0), pady=(20, 0)) # приветствие
label_2 = ttk.Label(text='Напиши в поле ввода свой запрос на английском')
label_2.grid(row=1, columnspan=2, padx=(75, 0)) # ожидание от пользователя

# поле ввода
search_image_entry = ttk.Entry(window)
search_image_entry.grid(row=2, column=0, padx=(60, 0))

# кнопка
send_button = ttk.Button(text='Тыкни для картинки', command=get_text)
send_button.grid(row=2, column=1)


window.mainloop()