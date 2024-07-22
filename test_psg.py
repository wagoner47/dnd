import PySimpleGUI as sg

layout = [
    [
        sg.Multiline(size=(30, 10), key="-INPUT-"),
        sg.Column(
            [[sg.Button("Clear", k="-CLEAR-")], [sg.Button("Hi!", k="-BUTTON1-")]]
        ),
    ],
    [sg.Output(size=(30, 5), key="-OUTPUT-"), sg.Button("=", k="-EQUAL-")],
]

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
    if event == "-BUTTON1-":
        if len(input_display) == 0:
            input_display = event
        else:
            input_display += f" + {event}"
        num_pressed += 1
    elif event == "-EQUAL-":
        output_display += " ".join("Hi!" for _ in range(num_pressed))
    else:
        input_display = ""
        output_display = ""
        num_pressed = 0

    # Prints get redirected to the Output Element
    window["-INPUT-"].update(input_display)
    window["-OUTPUT-"].update(output_display)
window.close()
