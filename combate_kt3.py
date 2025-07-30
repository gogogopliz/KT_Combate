
import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo - Kill Team 3", layout="wide")

# Función para determinar la mejor jugada en cada turno según estrategia
def resolver_combate(exitos_a, exitos_c_a, exitos_d, exitos_c_d, vida_a, vida_d, danyo_normal, danyo_critico, estrategia):
    acciones = []
    a_pool = ["C"] * exitos_c_a + ["N"] * exitos_a
    d_pool = ["C"] * exitos_c_d + ["N"] * exitos_d

    turno_atacante = True
    while (a_pool or d_pool) and vida_a > 0 and vida_d > 0:
        if turno_atacante and a_pool:
            actual = a_pool.pop(0)
            if estrategia == "Defensiva":
                if actual == "C" and "C" in d_pool:
                    d_pool.remove("C")
                    acciones.append(f"🛡️🟥 Atacante bloqueado por crítico 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif actual == "C" and "N" in d_pool:
                    d_pool.remove("N")
                    acciones.append(f"🛡️🟥 Atacante bloqueado por normal 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif actual == "N" and "N" in d_pool:
                    d_pool.remove("N")
                    acciones.append(f"🛡️🟥 Atacante bloqueado por normal 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                else:
                    daño = danyo_critico if actual == "C" else danyo_normal
                    vida_d -= daño
                    acciones.append(f"💣🟥 Atacante golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
            elif estrategia == "Máximo daño":
                daño = danyo_critico if actual == "C" else danyo_normal
                vida_d -= daño
                acciones.append(f"💣🟥 Atacante golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
            else:  # Mejor resultado
                # Si puedo matar sin morir, golpeo
                daño = danyo_critico if actual == "C" else danyo_normal
                if vida_d - daño <= 0:
                    vida_d -= daño
                    acciones.append(f"💣🟥 Atacante golpea ({actual}) causa {daño} (letal) | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif (actual == "C" and "C" in d_pool) or (actual == "C" and "N" in d_pool) or (actual == "N" and "N" in d_pool):
                    if actual == "C" and "C" in d_pool:
                        d_pool.remove("C")
                    elif actual == "C":
                        d_pool.remove("N")
                    else:
                        d_pool.remove("N")
                    acciones.append(f"🛡️🟥 Atacante bloqueado ({actual}) | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                else:
                    vida_d -= daño
                    acciones.append(f"💣🟥 Atacante golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
        elif not turno_atacante and d_pool:
            actual = d_pool.pop(0)
            if estrategia == "Defensiva":
                if actual == "C" and "C" in a_pool:
                    a_pool.remove("C")
                    acciones.append(f"🛡️🟦 Defensor bloquea crítico 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif actual == "C" and "N" in a_pool:
                    a_pool.remove("N")
                    acciones.append(f"🛡️🟦 Defensor bloquea normal 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif actual == "N" and "N" in a_pool:
                    a_pool.remove("N")
                    acciones.append(f"🛡️🟦 Defensor bloquea normal 🛡️ | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                else:
                    daño = danyo_critico if actual == "C" else danyo_normal
                    vida_a -= daño
                    acciones.append(f"💣🟦 Defensor golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
            elif estrategia == "Máximo daño":
                daño = danyo_critico if actual == "C" else danyo_normal
                vida_a -= daño
                acciones.append(f"💣🟦 Defensor golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
            else:  # Mejor resultado
                daño = danyo_critico if actual == "C" else danyo_normal
                if vida_a - daño <= 0:
                    vida_a -= daño
                    acciones.append(f"💣🟦 Defensor golpea ({actual}) causa {daño} (letal) | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                elif (actual == "C" and "C" in a_pool) or (actual == "C" and "N" in a_pool) or (actual == "N" and "N" in a_pool):
                    if actual == "C" and "C" in a_pool:
                        a_pool.remove("C")
                    elif actual == "C":
                        a_pool.remove("N")
                    else:
                        a_pool.remove("N")
                    acciones.append(f"🛡️🟦 Defensor bloquea ({actual}) | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
                else:
                    vida_a -= daño
                    acciones.append(f"💣🟦 Defensor golpea ({actual}) causa {daño} | Vida Atacante: {vida_a} | Vida Defensor: {vida_d}")
        turno_atacante = not turno_atacante

    resultado = "🤕 El Atacante muere" if vida_a <= 0 else "🤕 El Defensor muere" if vida_d <= 0 else "🏁 Nadie muere"
    return acciones, resultado


st.title("⚔️ Simulador Combate Cuerpo a Cuerpo - Kill Team 3")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🟥 Atacante")
    vida_atacante = st.number_input("Vida Atacante", min_value=1, value=10, key="vida_a")
    normales_a = st.number_input("Éxitos normales", min_value=0, value=2, key="n_a")
    criticos_a = st.number_input("Éxitos críticos", min_value=0, value=1, key="c_a")

with col2:
    st.subheader("🟦 Defensor")
    vida_defensor = st.number_input("Vida Defensor", min_value=1, value=10, key="vida_d")
    normales_d = st.number_input("Éxitos normales", min_value=0, value=2, key="n_d")
    criticos_d = st.number_input("Éxitos críticos", min_value=0, value=1, key="c_d")

st.subheader("⚙️ Configuración")
estrategia = st.selectbox("Estrategia", ["Máximo daño", "Defensiva", "Mejor resultado"])
danyo_normal = st.number_input("Daño por éxito normal", value=3, min_value=1)
danyo_critico = st.number_input("Daño por éxito crítico", value=5, min_value=1)

if st.button("Simular combate"):
    acciones, resultado = resolver_combate(
        normales_a, criticos_a, normales_d, criticos_d,
        vida_atacante, vida_defensor, danyo_normal, danyo_critico, estrategia
    )
    st.markdown("---")
    for act in acciones:
        st.write(act)
    st.subheader(f"✅ Resultado: {resultado}")
