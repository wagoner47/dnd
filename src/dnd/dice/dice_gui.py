# noinspection PyPep8Naming
import PySimpleGUI as sg

from dice import Die
from assets.output import images

sg.Button("KH", k="-KEEP HIGHEST-", tooltip="Keep N highest dice")
buttons = [
    [
        sg.Button("d%", k="-D100-", tooltip="100 sided dice", s=(8, 4)),
        sg.Button("d()", k="-DN-", tooltip="Roll dice of N sides", s=(8, 4)),
        sg.Button("del", k="-DELETE-", tooltip="Delete last item", s=(8, 4)),
        sg.Button("C", k="-CLEAR-", tooltip="Clear current memory", s=(8, 4)),
    ],
    [
        sg.Button(f"d{n}", k=f"-D{n}-", tooltip=f"{n} sided dice", s=(8, 4))
        for n in [4, 6, 8]
    ]
    + [sg.Button("\u00F7", k="-DIVIDE-", tooltip="Divide", s=(8, 4))],
    [
        sg.Button(f"d{n}", k=f"-D{n}-", tooltip=f"{n} sided dice", s=(8, 4))
        for n in [10, 12, 20]
    ]
    + [sg.Button("\u00D7", k="-MULTIPLY-", tooltip="Multiply", s=(8, 4))],
    [sg.Button(f"{n}", k=f"-{n}-", s=(8, 4)) for n in [7, 8, 9]]
    + [sg.Button("-", k="-MINUS-", tooltip="Subtract", s=(8, 4))],
    [sg.Button(f"{n}", k=f"-{n}-", s=(8, 4)) for n in [4, 5, 6]]
    + [sg.Button("+", k="-PLUS-", tooltip="Add", s=(8, 4))],
    [sg.Button(f"{n}", k=f"-{n}-", s=(8, 4)) for n in [1, 2, 3]]
    + [sg.Button("KHn", k="-KEEP HIGHEST-", tooltip="Keep n Highest Dice", s=(8, 4))],
    [
        sg.Button("0", k="-0-", s=(8, 4)),
        sg.Button("Adv()", k="-ADVANTAGE-", tooltip="Roll with advantage", s=(8, 4)),
        sg.Button("Dis()", k="-Disadvantage-", tooltip="Roll with disadvantage", s=(8, 4)),
        sg.Button("Roll", key="-ROLL-", tooltip="Roll", s=(8, 4)),
    ],
]

layout = [
    [sg.Text("Dice Calculator")],
    [sg.Output(size=(45, 10), key="-INPUT-")],
    [sg.Output(size=(45, 5), key="-OUTPUT-")],
]
layout += buttons

# Window
window = sg.Window(title="Output Element", layout=layout)

# Event loop
input_display = ""
output_display = ""
num_pressed = 0
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    # if event == "-BUTTON1-":
    #     if len(input_display) == 0:
    #         input_display = event
    #     else:
    #         input_display += f" + {event}"
    #     num_pressed += 1
    # elif event == "-EQUAL-":
    #     output_display += " ".join("Hi!" for _ in range(num_pressed))
    # else:
    #     input_display = ""
    #     output_display = ""
    #     num_pressed = 0

    # # Prints get redirected to the Output Element
    # window["-INPUT-"].update(input_display)
    # window["-OUTPUT-"].update(output_display)
window.close()
