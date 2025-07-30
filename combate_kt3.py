
import streamlit as st

st.set_page_config(page_title="Kill Team Cuerpo a Cuerpo", layout="centered")

st.title("⚔️ Kill Team - Cuerpo a Cuerpo")

st.markdown("Cada éxito puede 💥 golpear o 🛡️ bloquear. Elige dados, prioridades y obtén la mejor secuencia.")

def contador(label, key):
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("-", key=key+"_menos"):
            st.session_state[key] = max(0, st.session_state.get(key, 0) - 1)
    with c2:
        if st.button("+", key=key+"_mas"):
            st.session_state[key] = st.session_state.get(key, 0) + 1
    with c3:
        st.markdown(f"{label}: **{st.session_state.get(key, 0)}**")
    return st.session_state.get(key, 0)

# Compact layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("Atacante")
    atk_c = contador("Críticos", "atk_c")
    atk_n = contador("Normales", "atk_n")
    atk_d = st.number_input("Daño", 1, 10, 3, key="atk_d")
    atk_cd = st.number_input("Crítico", 1, 12, 5, key="atk_cd")
    atk_hp = st.number_input("Vida", 1, 30, 10, key="atk_hp")

with col2:
    st.subheader("Defensor")
    def_c = contador("Críticos", "def_c")
    def_n = contador("Normales", "def_n")
    def_d = st.number_input("Daño", 1, 10, 3, key="def_d")
    def_cd = st.number_input("Crítico", 1, 12, 5, key="def_cd")
    def_hp = st.number_input("Vida", 1, 30, 10, key="def_hp")

st.radio("🎯 Prioridad:", [
    "🩸 Maximizar daño infligido",
    "🛡️ Sobrevivir",
    "☠️ Matar al otro primero"
], key="objetivo", horizontal=True)

# Acción posible: (personaje, dado usado, acción: "hit"/"block", objetivo tipo)
class Accion:
    def __init__(self, quien, dado, acc, objetivo=None):
        self.q = quien
        self.d = dado  # "C" o "N"
        self.a = acc   # "hit" o "block"
        self.o = objetivo  # "C" o "N"

    def icono(self):
        if self.a == "hit":
            return f"{self.q} 💥 ({'⚡️' if self.d=='C' else '•'})"
        else:
            return f"{self.q} 🛡️ contra {'⚡️' if self.o=='C' else '•'}"

def simular_combate(ac, an, dc, dn, ad, acd, dd, dcd, ahp, dhp, prioridad):
    from itertools import permutations
    from copy import deepcopy

    a_pool = ['C']*ac + ['N']*an
    d_pool = ['C']*dc + ['N']*dn

    acciones_posibles = []

    def aplicar_combate(a_list, d_list):
        a = deepcopy(a_list)
        d = deepcopy(d_list)
        atk = ahp
        deff = dhp
        acciones = []
        turno = [('A', x) for x in a] + [('D', x) for x in d]
        for q, d_val in turno:
            pool_ally = a if q == 'A' else d
            pool_enemy = d if q == 'A' else a
            if d_val not in pool_ally:
                continue
            accion = None
            if 'C' in pool_enemy:
                pool_enemy.remove('C')
                accion = Accion(q, d_val, 'block', 'C')
            elif 'N' in pool_enemy and d_val == 'C':
                pool_enemy.remove('N')
                accion = Accion(q, d_val, 'block', 'N')
            else:
                dmg = acd if q == 'A' and d_val == 'C' else ad if q == 'A' else dcd if d_val == 'C' else dd
                if q == 'A':
                    deff -= dmg
                else:
                    atk -= dmg
                accion = Accion(q, d_val, 'hit')
            pool_ally.remove(d_val)
            acciones.append(accion)
        return acciones, atk, deff

    mejor = None
    mejor_valor = float('-inf')
    for orden_a in permutations(a_pool):
        for orden_d in permutations(d_pool):
            acciones, va, vd = aplicar_combate(list(orden_a), list(orden_d))
            if prioridad == "🩸 Maximizar daño infligido":
                valor = dhp - vd
            elif prioridad == "🛡️ Sobrevivir":
                valor = va
            else:
                valor = (dhp - vd) - (ahp - va)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor = acciones, va, vd
    return mejor

if st.button("⚔️ Resolver combate"):
    resultado = simular_combate(
        st.session_state.get("atk_c", 0), st.session_state.get("atk_n", 0),
        st.session_state.get("def_c", 0), st.session_state.get("def_n", 0),
        st.session_state["atk_d"], st.session_state["atk_cd"],
        st.session_state["def_d"], st.session_state["def_cd"],
        st.session_state["atk_hp"], st.session_state["def_hp"],
        st.session_state["objetivo"]
    )
    acciones, vida_a, vida_d = resultado
    st.subheader("🧠 Mejor secuencia:")
    for acc in acciones:
        st.markdown(f"- {acc.icono()}")
    st.markdown(f"🩸 Vida Atacante: **{vida_a}**")
    st.markdown(f"🛡️ Vida Defensor: **{vida_d}**")
