
import streamlit as st

st.set_page_config(layout="wide")

st.title("Simulador de Combate - Kill Team 3")

# Utilidades
def mostrar_exitos(nombre, n_normales, n_criticos):
    st.markdown(f"**{nombre}** 🎯")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Normales:")
        st.write(" ".join(["🎯"] * n_normales))
    with col2:
        st.write("Críticos:")
        st.write(" ".join(["💥"] * n_criticos))

def mostrar_accion(turno, quien, accion, tipo):
    simbolo = "💥" if accion == "golpea" else "🛡️"
    color = "🟥" if quien == "Atacante" else "🟦"
    texto = f"{turno+1}. {color} {quien} {simbolo} ({tipo})"
    st.markdown(texto)

# Entrada de datos
col1, col2 = st.columns(2)

with col1:
    st.header("🤺 Atacante")
    vida_atacante = st.number_input("Vida Atacante", 1, 20, 10, key="va")
    daño_normal_a = st.number_input("Daño normal", 1, 10, 3, key="dna")
    daño_critico_a = st.number_input("Daño crítico", 1, 10, 5, key="dca")
    st.markdown("**Éxitos**")
    an, ac = st.columns(2)
    with an:
        normales_a = st.number_input("🎯 Normales", 0, 5, 2, key="na")
    with ac:
        criticos_a = st.number_input("💥 Críticos", 0, 5, 1, key="ca")

with col2:
    st.header("🛡️ Defensor")
    vida_defensor = st.number_input("Vida Defensor", 1, 20, 10, key="vd")
    daño_normal_d = st.number_input("Daño normal", 1, 10, 3, key="dnd")
    daño_critico_d = st.number_input("Daño crítico", 1, 10, 5, key="dcd")
    st.markdown("**Éxitos**")
    dn, dc = st.columns(2)
    with dn:
        normales_d = st.number_input("🎯 Normales", 0, 5, 2, key="nd")
    with dc:
        criticos_d = st.number_input("💥 Críticos", 0, 5, 1, key="cd")

estrategia = st.selectbox("Estrategia", ["Máximo daño", "Defensiva", "Mejor resultado"])

if st.button("Simular combate"):
    acciones = []
    turno = 0

    # Inicializar estructuras de datos
    pool = {
        "Atacante": {"n": int(normales_a), "c": int(criticos_a), "vida": int(vida_atacante),
                     "d_n": int(daño_normal_a), "d_c": int(daño_critico_a)},
        "Defensor": {"n": int(normales_d), "c": int(criticos_d), "vida": int(vida_defensor),
                     "d_n": int(daño_normal_d), "d_c": int(daño_critico_d)}
    }

    orden = ["Atacante", "Defensor"]
    i = 0  # índice de alternancia

    while (pool["Atacante"]["n"] + pool["Atacante"]["c"] > 0 or pool["Defensor"]["n"] + pool["Defensor"]["c"] > 0) and pool["Atacante"]["vida"] > 0 and pool["Defensor"]["vida"] > 0:
        actual = orden[i % 2]
        rival = orden[(i + 1) % 2]
        golpeado = False
        bloqueado = False

        # Seleccionar qué éxito usar
        tipo = None
        if pool[actual]["c"] > 0:
            tipo = "c"
        elif pool[actual]["n"] > 0:
            tipo = "n"
        else:
            i += 1
            continue

        # Según estrategia decidir qué hacer
        bloquear = False

        if estrategia == "Defensiva":
            if pool[rival]["c"] > 0:
                pool[rival]["c"] -= 1
                bloqueado = True
            elif pool[rival]["n"] > 0:
                pool[rival]["n"] -= 1
                bloqueado = True
        elif estrategia == "Máximo daño":
            bloquear = False
        elif estrategia == "Mejor resultado":
            # Prioriza bloquear si puede sobrevivir para pegar más
            daño_total_rival = pool[rival]["c"] * pool[rival]["d_c"] + pool[rival]["n"] * pool[rival]["d_n"]
            daño_total_actual = pool[actual]["c"] * pool[actual]["d_c"] + pool[actual]["n"] * pool[actual]["d_n"]

            if daño_total_rival >= pool[actual]["vida"] and (pool[rival]["c"] > 0 or pool[rival]["n"] > 0):
                bloquear = True
                if pool[rival]["c"] > 0:
                    pool[rival]["c"] -= 1
                    bloqueado = True
                elif pool[rival]["n"] > 0:
                    pool[rival]["n"] -= 1
                    bloqueado = True

        if not bloqueado:
            dmg = pool[actual]["d_c"] if tipo == "c" else pool[actual]["d_n"]
            pool[rival]["vida"] -= dmg
            golpeado = True

        pool[actual][tipo] -= 1

        if golpeado:
            mostrar_accion(turno, actual, "golpea", "💥" if tipo == "c" else "🎯")
        elif bloqueado:
            mostrar_accion(turno, actual, "bloquea", "💥" if tipo == "c" else "🎯")

        turno += 1
        i += 1

        # Si muere uno, termina
        if pool["Atacante"]["vida"] <= 0 or pool["Defensor"]["vida"] <= 0:
            break

    # Mostrar resultado final
    st.markdown("---")
    if pool["Atacante"]["vida"] <= 0 and pool["Defensor"]["vida"] <= 0:
        st.error("💀 Ambos combatientes han muerto.")
    elif pool["Atacante"]["vida"] <= 0:
        st.error("💀 El Atacante ha muerto.")
    elif pool["Defensor"]["vida"] <= 0:
        st.success("🎯 ¡El Atacante ha matado al Defensor!")
    else:
        st.info("⚔️ Ambos sobreviven.")
