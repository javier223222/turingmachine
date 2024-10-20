import tkinter as tk
from tkinter import messagebox

class TuringMachine:
    def __init__(self, tape, blank_symbol='B'):
        # Inicializamos la cinta con los símbolos de entrada y extendemos con espacios en blanco
        self.tape = list(tape) + [blank_symbol] * 10
        self.blank_symbol = blank_symbol
        self.head = 0  # Posición del cabezal de lectura/escritura
        self.state = 'q0'  # Estado inicial
        self.transitions = {
            # Transiciones de la máquina de Turing
            ('q0', 'a'): ('q1', 'X', 'R'),
            ('q0', 'b'): ('q2', 'Y', 'R'),
            ('q1', 'a'): ('q1', 'a', 'R'),
            ('q1', 'b'): ('q1', 'b', 'R'),
            ('q1', blank_symbol): ('q3', blank_symbol, 'R'),
            ('q2', 'a'): ('q2', 'a', 'R'),
            ('q2', 'b'): ('q2', 'b', 'R'),
            ('q2', blank_symbol): ('q3', blank_symbol, 'R')
        }

    def step(self):
        # Leemos el símbolo actual de la cinta
        current_symbol = self.tape[self.head]
        # Obtenemos la transición con el estado actual y el símbolo leído
        key = (self.state, current_symbol)

        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            # Escribimos el nuevo símbolo en la cinta
            self.tape[self.head] = new_symbol
            # Actualizamos el estado
            self.state = new_state
            # Movemos el cabezal según la dirección
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head -= 1
        else:
            # Si no hay transición, detenemos la máquina
            self.state = 'halt'

    def run(self):
        while self.state not in ('q3', 'halt'):
            self.step()

        # Aceptar solo si el estado es q3 y la cinta está completamente procesada
        if self.state == 'q3' and all(symbol == 'B' for symbol in self.tape[self.head:]) and 'X' in self.tape:
            return "Cadena aceptada."
        else:
            return "Cadena rechazada."

# Interfaz con Tkinter con mejoras de UX/UI
class TuringMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Turing")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.header_label = tk.Label(root, text="Simulador de Máquina de Turing", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
        self.header_label.pack(pady=10)

        self.label = tk.Label(root, text="Ingrese la cinta de entrada:", font=("Helvetica", 12), bg="#f0f0f0")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root, font=("Helvetica", 12), width=30, justify='center')
        self.entry.pack(pady=5)

        self.run_button = tk.Button(root, text="Ejecutar", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.run_turing_machine)
        self.run_button.pack(pady=15)

        self.result_label = tk.Label(root, text="Resultado:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333")
        self.result_label.pack(pady=10)

    def run_turing_machine(self):
        tape_input = self.entry.get()
        if not tape_input:
            messagebox.showwarning("Advertencia", "Por favor ingrese una cinta de entrada.")
            return
        
        tm = TuringMachine(tape_input)
        result = tm.run()
        messagebox.showinfo("Resultado", result)
        self.result_label.config(text=f"Resultado: {result}")

# Ejecución de la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = TuringMachineApp(root)
    root.mainloop()
