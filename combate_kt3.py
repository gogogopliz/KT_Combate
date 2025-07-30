
import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo KT3", layout="wide")
st.title("⚔️ Simulador Cuerpo a Cuerpo - Kill Team 2024")

st.markdown("Ajusta los dados y compara los resultados. Cada éxito puede infligir daño o cancelar un éxito enemigo.")

# --- Inputs compactos ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🟥 Atacante")
    atk_normals = st.number_input("Éxitos normales", 0, 5, 2, key="atk_normals")
    atk_crits = st.number_input("Éxitos críticos", 0, 5, 1, key="atk_crits")
    atk_damage = st.number_input("Daño normal", 1, 10, 3, key="atk_damage")
    atk_crit_damage = st.number_input("Daño crítico", 1, 10, 6, key="atk_crit_damage")
    atk_wounds = st.number_input("Vida", 1, 30, 10, key="atk_wounds")

with col2:
    st.subheader("🟦 Defensor")
    def_normals = st.number_input("Éxitos normales", 0, 5, 2, key="def_normals")
    def_crits = st.number_input("Éxitos críticos", 0, 5, 1, key="def_crits")
    def_damage = st.number_input("Daño normal", 1, 10, 3, key="def_damage")
    def_crit_damage = st.number_input("Daño crítico", 1, 10, 5, key="def_crit_damage")
    def_wounds = st.number_input("Vida", 1, 30, 10, key="def_wounds")

st.markdown("---")

# --- Resolución del combate ---
def resolver_combate(a_n, a_c, d_n, d_c, a_d, a_cd, d_d, d_cd, v_a, v_d):
    secuencia = []
    atk_total = [2] * a_c + [1] * a_n  # 2 = crítico, 1 = normal
    def_total = [2] * d_c + [1] * d_n
    atk_total.sort(reverse=True)
    def_total.sort(reverse=True)

    i, j = 0, 0
    while i < len(atk_total) and j < len(def_total):
        if def_total[j] == 2 and atk_total[i] >= 2:
            secuencia.append("🟦🛡️ Defensor bloquea crítico atacante")
            i += 1; j += 1
        elif def_total[j] >= atk_total[i]:
            secuencia.append("🟦🛡️ Defensor bloquea ataque")
            i += 1; j += 1
        else:
            break

    # Lo que queda hace daño
    dmg_a, dmg_d = 0, 0
    for atk in atk_total[i:]:
        if atk == 2:
            secuencia.append("🟥💥 Atacante golpea con crítico")
            dmg_a += a_cd
        else:
            secuencia.append("🟥💥 Atacante golpea")
            dmg_a += a_d

    for df in def_total[j:]:
        if df == 2:
            secuencia.append("🟦💥 Defensor golpea con crítico")
            dmg_d += d_cd
        else:
            secuencia.append("🟦💥 Defensor golpea")
            dmg_d += d_d

    v_a_final = max(0, v_a - dmg_d)
    v_d_final = max(0, v_d - dmg_a)

    return secuencia, v_a_final, v_d_final, dmg_a, dmg_d

# --- Ejecutar y mostrar resultado ---
seq, v_a_res, v_d_res, dmg_a, dmg_d = resolver_combate(
    atk_normals, atk_crits, def_normals, def_crits,
    atk_damage, atk_crit_damage, def_damage, def_crit_damage,
    atk_wounds, def_wounds
)

st.subheader("🧠 Resolución paso a paso")
for paso in seq:
    st.markdown(f"- {paso}")

colr1, colr2 = st.columns(2)
with colr1:
    st.metric("🟥 Vida restante Atacante", f"{v_a_res} ❤️", delta=-dmg_d)
with colr2:
    st.metric("🟦 Vida restante Defensor", f"{v_d_res} ❤️", delta=-dmg_a)
