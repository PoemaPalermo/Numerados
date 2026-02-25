import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

'''
themes:
light
- minty
- flatly
- yeti

dark
- superhero
- solar
- darkly
'''
# window
window = ttkb.Window(themename="flatly")
window.geometry("1440x767")
window.title("Numerados")

# grid configuration
for col in range(28):
    window.columnconfigure(col, weight=1)

for row in range(15):
    window.rowconfigure(row, weight=1)

# validaciones 
def solo_numeros(txt):
    return txt.isdigit() or txt == ""

def solo_simbolos(txt):
    permitidos = "+-*/:"
    return all(c in permitidos for c in txt) or txt == ""

vcmd_num = (window.register(solo_numeros), "%P")
vcmd_sym = (window.register(solo_simbolos), "%P")

# almacenamiento 
inputs_numeros = {}
inputs_simbolos = {}
respuestas_inputs_numeros = {}
respuestas_inputs_simbolos = {}

# helpers 
def crear_num(row, col, key):
    var = ttkb.StringVar()
    e = ttkb.Entry(
        window,
        width=4,
        justify="center",
        textvariable=var,
        validate="key",
        validatecommand=vcmd_num,
        bootstyle=SECONDARY
    )
    e.grid(row=row, column=col, padx=4, pady=6)
    inputs_numeros[key] = var

def crear_sym(row, col, key):
    var = ttkb.StringVar()
    e = ttkb.Entry(
        window,
        width=3,
        justify="center",
        textvariable=var,
        validate="key",
        validatecommand=vcmd_sym,
        bootstyle="danger"
    )
    e.grid(row=row, column=col, padx=2, pady=6)
    inputs_simbolos[key] = var

def crear_equal(row, col):
    ttkb.Label(window, text="=", font=("Segoe UI", 16)).grid(
        row=row, column=col, padx=2
    )

# cuentas
filas = [1, 3, 5, 7, 9]
bloques = [1, 8, 15, 22]
#r{fila}_b{bloque}_{tipo}
for r_i, row in enumerate(filas):
    for b_i, base in enumerate(bloques):
        k = f"r{r_i}_b{b_i}"
        crear_num(row, base + 0, k + "_n1")
        crear_sym(row, base + 1, k + "_op")
        crear_num(row, base + 2, k + "_n2")
        crear_equal(row, base + 3)
        crear_num(row, base + 4, k + "_res")

# operadores
respuestas_operadores = []
for i in range(20):
    crear_num(11, 4 + i, f"bottom_{i}")


# chequear
# funciones

# boton
check_btn = ttkb.Button(window, text="Finished", style="succes")
check_btn.grid(column=12, columnspan=4, row=13, sticky="nswe")

window.mainloop()