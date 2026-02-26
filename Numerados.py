import random
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# window
window = ttkb.Window(themename="morph")
window.geometry("1440x767")
window.title("Numerados")

# grid configuration
for col in range(30):
    window.columnconfigure(col, weight=1)

for row in range(16):
    window.rowconfigure(row, weight=1)

# validaciones 
def solo_numeros(txt):
    return txt.isdigit() or txt == ""

def solo_simbolos(txt):
    permitidos = "+*"
    return txt == "" or (len(txt) <= 1 and txt in permitidos)

vcmd_num = (window.register(solo_numeros), "%P")
vcmd_sym = (window.register(solo_simbolos), "%P")

# almacenamiento 
inputs_numeros = {}
inputs_simbolos = {}
respuestas_inputs_numeros = {}
respuestas_inputs_simbolos = {}

# helpers 
def crear_num(row, col, key, disabled=False):
    var = ttkb.StringVar()
    e = ttkb.Entry(
        window,
        width=4,
        justify="center",
        textvariable=var,
        validate="key",
        validatecommand=vcmd_num,
        bootstyle=SECONDARY,
        state="readonly" if disabled else "normal"
    )
    e.grid(row=row, column=col, padx=4, pady=6)
    inputs_numeros[key] = var

def crear_sym(row, col, key):
    var = ttkb.StringVar()
    e = ttkb.Entry(
        window,
        width=2,
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
filas = [2, 4, 6, 8, 10]
bloques = [2, 9, 16, 23]
#r{fila}_b{bloque}_{tipo}
for r_i, row in enumerate(filas):
    for b_i, base in enumerate(bloques):
        k = f"r{r_i}_b{b_i}"
        crear_num(row, base + 0, k + "_n1")
        crear_sym(row, base + 1, k + "_op")
        crear_num(row, base + 2, k + "_n2")
        crear_equal(row, base + 3)
        crear_num(row, base + 4, k + "_res", disabled=True)

# operadores
respuestas_operadores = []
for i in range(20):
    crear_num(11, 4 + i, f"bottom_{i}")

#crerar numeros
def calcular(a, b, op):
    if op == "+":
        return a + b
    if op == "*":
        return a * b

def generar_datos():
    numeros = random.sample(range(2, 70, 2), 20)

    chicos = [n for n in numeros if n <= 50]
    grandes = [n for n in numeros if n > 50]

    random.shuffle(chicos)
    random.shuffle(grandes)

    pares = []

    # grandes con chicos
    while grandes and chicos:
        intentos = 0
        while True:
            intentos += 1
            if intentos > 50:
                a = grandes.pop()
                b = chicos.pop()
                break

            a = grandes.pop()
            b = chicos.pop()

            if a * b > 999:
                grandes.append(a)
                chicos.append(b)
                random.shuffle(grandes)
                random.shuffle(chicos)
                continue
            break

        signos = ["+", "*"]
        random.shuffle(signos)
        pares.append((a, b, signos[0]))
        pares.append((a, b, signos[1]))

    resto = chicos[:]
    random.shuffle(resto)

    while len(resto) >= 2:
        intentos = 0
        while True:
            intentos += 1
            if intentos > 50:
                a = resto.pop()
                b = resto.pop()
                break

            a = resto.pop()
            b = resto.pop()

            if a * b > 999:
                resto.extend([a, b])
                random.shuffle(resto)
                continue
            break

        signos = ["+", "*"]
        random.shuffle(signos)
        pares.append((a, b, signos[0]))
        pares.append((a, b, signos[1]))

    random.shuffle(pares)
    respuestas_operadores = sorted(numeros)
    return pares, respuestas_operadores

def cargar_en_tablero():
    pares, respuestas_operadores = generar_datos()

    respuestas_inputs_numeros.clear()
    respuestas_inputs_simbolos.clear()

    i = 0
    for r_i, row in enumerate(filas):
        for b_i, base in enumerate(bloques):
            if i >= len(pares):
                break

            a, b, op = pares[i]
            k = f"r{r_i}_b{b_i}"

            # guardar respuestas correctas
            respuestas_inputs_numeros[k + "_n1"] = a
            respuestas_inputs_numeros[k + "_n2"] = b
            respuestas_inputs_simbolos[k + "_op"] = op

            # limpiar inputs del usuario
            inputs_numeros[k + "_n1"].set("")
            inputs_numeros[k + "_n2"].set("")
            inputs_simbolos[k + "_op"].set("")

            # resultado visible (queda como lo tenías)
            res = calcular(a, b, op)
            inputs_numeros[k + "_res"].set(str(res))
            respuestas_inputs_numeros[k + "_res"] = res

            i += 1

    return respuestas_operadores

respuestas_operadores = cargar_en_tablero()
# chequear
# funciones
def checking():
    errores = 0

    for key, var in inputs_numeros.items():
        if key.endswith("_res"):
            continue

        valor_usuario = var.get().strip()
        valor_correcto = str(respuestas_inputs_numeros.get(key, "")).strip()

        if valor_usuario != valor_correcto:
            errores += 1

    if errores > 0:
        check_label.config(
            text=f"Te equivocaste {errores} veces",
            bootstyle="danger"
        )
    else:
        check_label.config(
            text="LO LOGRASTE",
            bootstyle="success"
        )

    return errores == 0


# boton
check_btn = ttkb.Button(
    window,
    text="Finished",
    bootstyle="success",
    command=checking  # ✅ sin lambda
)
check_btn.grid(column=13, columnspan=4, row=13, sticky="wes")

check_label = ttkb.Label(window, text="", bootstyle="danger")
check_label.grid(column=13, columnspan=4, row=0, sticky="wes")


#agregados esteticos
# estado del switch
style = ttkb.Style()
tema_var = ttkb.BooleanVar(value=False)

def cambiar_tema():
    if tema_var.get():
        style.theme_use("solar")
    else:
        style.theme_use("morph")

# switch
theme_switch = ttkb.Checkbutton(
    window,
    text="Mode",
    variable=tema_var,
    command=cambiar_tema,
    bootstyle="round-toggle"
)

theme_switch.grid(row=0, column=26, columnspan=2, sticky="e", padx=10, pady=10)

window.mainloop()