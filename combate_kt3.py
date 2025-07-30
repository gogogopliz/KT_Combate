
import streamlit as st

st.set_page_config(page_title="Kill Team 3 - Cuerpo a Cuerpo", layout="centered")

st.title("⚔️ Kill Team 3 - Simulador de Combate Cuerpo a Cuerpo")

st.markdown("Marca los éxitos de cada combatiente y define tus prioridades estratégicas. El sistema te recomendará la mejor resolución.")

st.header("🎲 Resultados de Dados")

def contador(label, key):
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("➖", key=key + "_menos"):
            st.session_state[key] = max(0, st.session_state.get(key, 0) - 1)
    with col2:
        if st.button("➕", key=key + "_mas"):
            st.session_state[key] = st.session_state.get(key, 0) + 1
    with col3:
        st.markdown(f"**{label}:** {st.session_state.get(key, 0)}")
    return st.session_state.get(key, 0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Atacante")
    atk_normals = contador("Éxitos normales", "atk_normals")
    atk_crits = contador("Éxitos críticos", "atk_crits")
    atk_dmg = st.number_input("Daño normal", 1, 10, 3, key="atk_dmg")
    atk_critdmg = st.number_input("Daño crítico", 1, 12, 5, key="atk_crit")
    atk_wounds = st.number_input("Vida restante", 1, 30, 10, key="atk_w")

with col2:
    st.subheader("Defensor")
    def_normals = contador("Éxitos normales", "def_normals")
    def_crits = contador("Éxitos críticos", "def_crits")
    def_dmg = st.number_input("Daño normal (def)", 1, 10, 3, key="def_dmg")
    def_critdmg = st.number_input("Daño crítico (def)", 1, 12, 5, key="def_crit")
    def_wounds = st.number_input("Vida restante (def)", 1, 30, 10, key="def_w")

st.header("🎯 Objetivo de la resolución")
objective = st.radio("¿Qué quieres priorizar?", [
    "🩸 Maximizar daño infligido",
    "🛡️ Sobrevivir",
    "☠️ Matar al otro primero"
])

st.divider()

def resolve_combat(a_crits, a_normals, d_crits, d_normals, atk_dmg, atk_crit, def_dmg, def_crit, atk_w, def_w, priority):
    a_pool = ['C']*a_crits + ['N']*a_normals
    d_pool = ['C']*d_crits + ['N']*d_normals

    results = []
    used_states = set()

    def simulate(seq):
        a = a_pool.copy()
        d = d_pool.copy()
        atk_hp = atk_w
        def_hp = def_w
        actions = []
        turn = 'A'

        for action in seq:
            if turn == 'A' and a:
                chosen = None
                if 'C' in a:
                    chosen = 'C'
                elif 'N' in a:
                    chosen = 'N'
                if chosen:
                    if chosen == 'C' and 'C' in d:
                        d.remove('C')
                        actions.append("El atacante elimina un crítico enemigo")
                    elif chosen == 'C' and 'N' in d:
                        d.remove('N')
                        actions.append("El atacante elimina un normal enemigo")
                    else:
                        def_hp -= atk_crit if chosen == 'C' else atk_dmg
                        actions.append(f"El atacante inflige daño ({atk_crit if chosen == 'C' else atk_dmg})")
                    a.remove(chosen)
            elif turn == 'D' and d:
                chosen = None
                if 'C' in d:
                    chosen = 'C'
                elif 'N' in d:
                    chosen = 'N'
                if chosen:
                    if chosen == 'C' and 'C' in a:
                        a.remove('C')
                        actions.append("El defensor elimina un crítico enemigo")
                    elif chosen == 'C' and 'N' in a:
                        a.remove('N')
                        actions.append("El defensor elimina un normal enemigo")
                    else:
                        atk_hp -= def_crit if chosen == 'C' else def_dmg
                        actions.append(f"El defensor inflige daño ({def_crit if chosen == 'C' else def_dmg})")
                    d.remove(chosen)
            turn = 'D' if turn == 'A' else 'A'
        return (atk_hp, def_hp, actions)

    turn_sequence = ['A', 'D'] * 5
    for i in range(len(a_pool) + len(d_pool)):
        path = turn_sequence[:i+1]
        key = tuple(path)
        if key not in used_states:
            used_states.add(key)
            res = simulate(path)
            results.append(res)

    best = None
    if priority == "🩸 Maximizar daño infligido":
        best = max(results, key=lambda x: def_w - x[1])
    elif priority == "🛡️ Sobrevivir":
        best = max(results, key=lambda x: x[0])
    elif priority == "☠️ Matar al otro primero":
        best = max(results, key=lambda x: (def_w - x[1]) - (atk_w - x[0]))

    return best

if st.button("⚔️ Calcular resolución óptima"):
    outcome = resolve_combat(
        atk_crits, atk_normals, def_crits, def_normals,
        atk_dmg, atk_critdmg, def_dmg, def_critdmg,
        atk_wounds, def_wounds, objective
    )
    st.success("✅ Resolución recomendada:")
    st.markdown("**🧠 Acciones sugeridas (por orden de ejecución):**")
    for act in outcome[2]:
        st.markdown(f"- {act}")
    st.markdown(f"🩸 Vida del atacante al final: **{outcome[0]}**")
    st.markdown(f"🛡️ Vida del defensor al final: **{outcome[1]}**")
