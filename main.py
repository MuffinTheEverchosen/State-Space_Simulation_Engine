from classes.Signals import RectangleSignal, SineSignal, TriangleSignal
from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation
import numpy as np
import customtkinter
import tkinter
from PIL import Image 

czas = 1
step_size = 1
J1 = 1
J2 = 1
n1 = 1 
n2 = 1 
k = 1
b = 1 
Jeq = J2 + J1 * pow(n2/n1, 2)
tolerance = 1 
Amp = 1
Per = 1

state_matrix = [[0, 1],[-k/Jeq, -b/Jeq]]
input_matrix = [[0], [n2/(n1*Jeq)]]
output_matrix = [[1, 0], [0, 1]]
inital_state = [[0], [1]]

system = StateSpaceSystem(state_matrix, input_matrix, output_matrix, inital_state)
simulation = SystemSimulation(step_size, system)


Square_Signal = RectangleSignal(Amp, Per)
Sine_Signal = SineSignal(Amp, Per)
Triangle_Signal = TriangleSignal(Amp, Per)

app = customtkinter.CTk()
app.title("my app")
app.geometry("1200x1000")
main_frame = customtkinter.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = customtkinter.CTkFrame(main_frame, width=250)
left_frame.pack(side="left", fill="y", padx=(0, 10))
left_frame.pack_propagate(False)

right_frame = customtkinter.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)


mojlabel = customtkinter.CTkLabel(right_frame, text="Tu wyświetli się wykres")
mojlabel.pack(fill="both", expand=True)
current_signal = Triangle_Signal

def combobox_callback(choice):
    global current_signal
    if choice == "Square Signal":
        current_signal = Square_Signal
    elif choice == "Sine Signal":
        current_signal = Sine_Signal
    elif choice == "Triangle Signal":
        current_signal = Triangle_Signal

def startsymulacja():
    step_size = float(lotfi_step_size.get())
    czas = float(lotfi_czas.get())
    J1 = float(lotfi_J1.get())
    J2 = float(lotfi_J2.get())
    n1 = float(lotfi_n1.get())
    n2 =float(lotfi_n2.get())
    b = float(lotfi_b.get())
    k = float(lotfi_k.get())
    Per = float(lotfi_Per.get())
    Per = float(lotfi_Amp.get())
    tolerance = float(lotfi_tolerance.get())
    Jeq = J2 + J1 * pow(n2/n1, 2)
    state_matrix = [[0, 1], [-k/Jeq, -b/Jeq]]
    input_matrix = [[0], [n2/(n1*Jeq)]]
    output_matrix = [[1, 0], [0, 1]]
    initial_state = [[0], [1]]
    Square_Signal = RectangleSignal(Amp, Per)
    Sine_Signal = SineSignal(Amp, Per)
    Triangle_Signal = TriangleSignal(Amp, Per)
    symulacja = StateSpaceSystem(state_matrix, input_matrix, output_matrix, inital_state)
    symulacja_Env = SystemSimulation(step_size, symulacja, False, True)
    symulacja_Env.run([[current_signal]], czas)
    symulacja_Env.plot_and_save("wykres.png")
    nowy_obraz = customtkinter.CTkImage(light_image=Image.open('wykres.png'), dark_image=Image.open('wykres.png'),size=(800,500))
    mojlabel.configure(image=nowy_obraz, text="")

class Lotfi(tkinter.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = tkinter.StringVar()
        tkinter.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        value = self.get()
        if value == '':
            self.old_value = value
            return
        try:
            float(value)
            self.old_value = value
        except ValueError:
            self.set(self.old_value)

button = customtkinter.CTkButton(left_frame, text="Simulation Start", command=startsymulacja)
button.pack(padx=20, pady=10, fill="x")

combobox_var = customtkinter.StringVar(value="Triangle Signal")
combobox = customtkinter.CTkComboBox(
    master=app, 
    values=["Square Signal", "Sine Signal", "Triangle Signal"], 
    command=combobox_callback, 
    variable=combobox_var
)

frame_width = right_frame.winfo_width()
frame_height = right_frame.winfo_height()
img_size = (min(frame_width - 40, 800), min(frame_height - 40, 500))

combobox_var = customtkinter.StringVar(value="Triangle Signal")
combobox = customtkinter.CTkComboBox(
    master=left_frame, 
    values=["Square Signal", "Sine Signal", "Triangle Signal"], 
    command=combobox_callback, 
    variable=combobox_var
)
combobox.pack(padx=20, pady=20, fill="x")



Frame1 = customtkinter.CTkFrame(left_frame)
Frame1.pack(padx=20, pady=10, fill="x")

params_frame = customtkinter.CTkFrame(left_frame)
params_frame.pack(padx=20, pady=10, fill="x")

customtkinter.CTkLabel(Frame1, text="Amplituda: ").pack(anchor="w")
lotfi_Amp = Lotfi(Frame1)
lotfi_Amp.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(Frame1, text="Okres: ").pack(anchor="w")
lotfi_Per = Lotfi(Frame1)
lotfi_Per.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Czas trwania symulacji: ").pack(anchor="w")
lotfi_czas = Lotfi(params_frame)
lotfi_czas.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Rozmiar kroku: ").pack(anchor="w")
lotfi_step_size = Lotfi(params_frame)
lotfi_step_size.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Wartość J1: ").pack(anchor="w")
lotfi_J1 = Lotfi(params_frame)
lotfi_J1.pack(fill="x", pady=(0,10))



customtkinter.CTkLabel(params_frame, text="Wartość J2: ").pack(anchor="w")
lotfi_J2 = Lotfi(params_frame)
lotfi_J2.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Liczba zębów przekładni 1 (n1): ").pack(anchor="w")
lotfi_n1 = Lotfi(params_frame)
lotfi_n1.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Liczba zębów przekładni 1 (n2): ").pack(anchor="w")
lotfi_n2 = Lotfi(params_frame)
lotfi_n2.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Sztywność (k): ").pack(anchor="w")
lotfi_k = Lotfi(params_frame)
lotfi_k.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Współczynnik tłumienia (b): ").pack(anchor="w")
lotfi_b = Lotfi(params_frame)
lotfi_b.pack(fill="x", pady=(0,10))

customtkinter.CTkLabel(params_frame, text="Tolerancja: ").pack(anchor="w")
lotfi_tolerance = Lotfi(params_frame)
lotfi_tolerance.pack(fill="x", pady=(0,10))


app.mainloop()



