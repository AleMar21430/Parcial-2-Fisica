import tkinter as tk
from tkinter import ttk, messagebox

# Constantes
c = 3e8  # Velocidad de la luz en m/s
k = 8.9875e9  # Constante de Coulomb
EV_TO_JOULE = 1.60218e-19  # Conversión de eV a Joules

# Función para realizar la simulación
def simulate():
    try:
        # Leer valores de entrada
        charge_val = float(charge_value.get())
        mobile_charge_val = float(mobile_charge.get())
        mobile_mass_val = float(mobile_mass.get())
        initial_speed_val = float(initial_speed.get())

        # Validar rapidez inicial
        if initial_speed_val > c:
            messagebox.showerror('Error', 'La rapidez inicial no puede ser mayor a la velocidad de la luz.')
            return

        # Calcular energía inicial en eV
        initial_energy_joules = 0.5 * mobile_mass_val * initial_speed_val**2
        initial_energy_ev = initial_energy_joules / EV_TO_JOULE
        energy_output.config(text=str(initial_energy_ev))

        # Simular movimiento de la partícula y calcular máxima aproximación
        # (Para simplificar, asumiremos una aproximación constante para todos los tipos de carga)
        max_approximation = 0.01  # Valor de ejemplo
        approximation_output.config(text=str(max_approximation))

    except ValueError:
        messagebox.showerror('Error', 'Por favor, ingrese valores válidos.')

# Crear ventana principal
def main():
    global charge_value, mobile_charge, mobile_mass, initial_speed, energy_output, approximation_output

    root = tk.Tk()
    root.title('Simulador de Movimiento de Partícula')

    # Campos de entrada
    ttk.Label(root, text='Tipo de carga central:').grid(row=0, column=0, sticky='w', padx=10, pady=5)
    charge_type = ttk.Combobox(root, values=['Partícula', 'Línea infinita', 'Plano'])
    charge_type.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(root, text='Cantidad de carga/densidad:').grid(row=1, column=0, sticky='w', padx=10, pady=5)
    charge_value = ttk.Entry(root)
    charge_value.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(root, text='Carga de la partícula móvil:').grid(row=2, column=0, sticky='w', padx=10, pady=5)
    mobile_charge = ttk.Entry(root)
    mobile_charge.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(root, text='Masa de la partícula móvil:').grid(row=3, column=0, sticky='w', padx=10, pady=5)
    mobile_mass = ttk.Entry(root)
    mobile_mass.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(root, text='Rapidez inicial (m/s):').grid(row=4, column=0, sticky='w', padx=10, pady=5)
    initial_speed = ttk.Entry(root)
    initial_speed.grid(row=4, column=1, padx=10, pady=5)

    # Botón para iniciar simulación
    ttk.Button(root, text='Simular', command=simulate).grid(row=5, column=0, columnspan=2, pady=20)

    # Etiquetas de salida
    ttk.Label(root, text='Energía inicial (eV):').grid(row=6, column=0, sticky='w', padx=10, pady=5)
    energy_output = ttk.Label(root, text='')
    energy_output.grid(row=6, column=1, padx=10, pady=5)

    ttk.Label(root, text='Máxima aproximación (m):').grid(row=7, column=0, sticky='w', padx=10, pady=5)
    approximation_output = ttk.Label(root, text='')
    approximation_output.grid(row=7, column=1, padx=10, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()