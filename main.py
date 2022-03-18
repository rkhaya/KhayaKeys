import PySimpleGUI as Sg
from pynput import keyboard
from pynput.keyboard import Key, Controller


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Prefix:
    def __init__(self, prefix="", taken=None):
        if taken is None:
            taken = {}
        self.prefix = prefix
        self.taken = taken
        self.pressed = ""
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def __str__(self):
        return self.prefix

    def get_prefix(self):
        return self.prefix

    def start_macro(self, letter):
        your_keyboard = Controller()
        tab_index = -1
        print(self.taken[letter])
        if "<TAB>" in self.taken[letter]:
            tab_index = self.taken[letter].index("<TAB>")

        for i in range(len(self.prefix) + len(letter)):
            your_keyboard.press(Key.backspace)
            your_keyboard.release(Key.backspace)
        for i in range(len(self.taken[letter])):
            if i == tab_index:
                your_keyboard.press(Key.tab)
                your_keyboard.release(Key.tab)
            elif tab_index + 1 <= i <= tab_index+4:
                print("TAB SPOT!")
            else:
                your_keyboard.press(self.taken[letter][i])
                your_keyboard.release(self.taken[letter][i])

    def on_press(self, key):
        try:
            print('alphanumeric key {} pressed'.format(
                key.char))
            self.pressed = self.pressed + key.char
            for i in self.taken:
                print(i)
                print(self.pressed)
                if self.pressed.endswith(self.prefix + i):
                    print("Found!")
                    self.start_macro(i)

        except AttributeError:
            print('special key {} pressed'.format(
                key))

    def addkey(self):
        layout = [[Sg.Text("What key would you like to add?")],
                  [Sg.Input(key='addedKey')],
                  [Sg.Text("What would you like it to type?")],
                  [Sg.Input(key='keyInput')],
                  [Sg.Text(size=(40, 1), key='output')],
                  [Sg.Button('Add!'), Sg.Button('Close')]]

        window = Sg.Window("Add Keys", layout)

        while True:
            event, values = window.read()
            if event == Sg.WINDOW_CLOSED or event == "Close":
                break
            elif values['addedKey'] != '':
                self.taken[values['addedKey']] = values['keyInput']
                window['output'].update('{} was added to your list'.format(values['addedKey']))

        window.close()

    def viewkeys(self):
        layout = []
        for i in self.taken:
            layout.append([Sg.Text('Prefix: ' + i + ' ' + self.taken[i])])
        layout.append([Sg.Button('Close')])
        window = Sg.Window("View Keys", layout)

        while True:
            event, values = window.read()
            if event == Sg.WINDOW_CLOSED or event == "Close":
                break

        window.close()

    @staticmethod
    def error_message(error):
        error_message = [[Sg.Text("{}".format(error))],
                         [Sg.Button("Close")]]
        error_window = Sg.Window('Error', error_message)
        while True:
            ev, va = error_window.read()
            if ev == Sg.WINDOW_CLOSED or ev == "Close":
                break
        error_window.close()

    def main_window(self):
        layout = [[Sg.Text("Welcome! Your current prefix is '{}'".format(self.get_prefix()))],
                  [Sg.Text("What would you like to do?")],
                  [Sg.Button('Add a key'), Sg.Button("View My Keys"), Sg.Button('Quit')]]

        window = Sg.Window("Shorter Keys", layout)
        while True:
            event, values = window.read()
            if event == Sg.WINDOW_CLOSED or event == "Quit":
                break
            elif event == 'Add a key':
                self.addkey()
            elif event == 'View My Keys':
                if len(self.taken) >= 1:
                    self.viewkeys()
                else:
                    self.error_message("You don't have any keys")
        window.close()

    def create_sk(self):
        layout = [[Sg.Text("What would you like your prefix to be?")],
                  [Sg.Input(key='-INPUT-')],
                  [Sg.Button('Set Prefix'), Sg.Button('Quit')],
                  [Sg.Text(size=(40, 1), key='-OUTPUT-')]]

        # Create the window
        window = Sg.Window('Window Title', layout)

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == Sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif values['-INPUT-'] != '':
                self.prefix = values['-INPUT-']
                break
            else:
                window['-OUTPUT-'].update('Please enter a prefix')

        # Finish up by removing from the screen
        window.close()
        #print(values['-INPUT-'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sk = Prefix()
    sk.create_sk()
    if sk.get_prefix() != '':
        sk.main_window()
