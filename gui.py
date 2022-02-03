import traceback

import PySimpleGUI as sg

# from main import main

data = (
    'Другое',
    'Москва',
    'Санкт-Петербург',
    'Татарстан',
    'Красноярский край',
    'Ставропольский край',
    'Оренбургская область',
    'Мордовия',
    'Ханты-Мансийский АО',
    'Псковская область'
)


def main_gui():
    layout = [
        [sg.Listbox(data, size=(20, 10), select_mode='LISTBOX_SELECT_MODE_SINGLE', default_values=['Другое'])],
        [sg.Submit('Поиск'), sg.Cancel('Выход')],
        [sg.Output(size=(50, 5))]
    ]
    window = sg.Window('ФССП Парсер', layout)
    while True:  # The Event Loop
        event, values = window.read()
        # print(event, values) #debug
        if event in (None, 'Exit', 'Выход'):
            break

        elif event == 'Поиск':
            try:
                # main()
                pass
            except:
                print('ОШИБКА, свяжитесь с разработчиком')
                print(traceback.format_exc())
            else:
                print('Успешно!')
                print('------------------------------')


if __name__ == '__main__':
    main_gui()