
import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo KT3", layout="wide")
st.title("⚔️ Simulador Cuerpo a Cuerpo - Kill Team 2024")

st.markdown("Ajusta los dados y compara los resultados. Cada éxito puede infligir daño o cancelar un éxito enemigo.")

estrategia = st.radio("🧭 Estrategia de resolución", ["Mejor resultado", "Maximizar daño", "Defensiva"], horizontal=True)

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

def usar_éxito_para_cancelar(lista_ataques, lista_oponente):
    # Un crítico puede cancelar crítico o normal. Normal solo puede cancelar normal.
    for i, x in enumerate(lista_ataques):
        for j, y in enumerate(lista_oponente):
            if x == 2 and y >= 1:
                return i, j
            elif x == 1 and y == 1:
                return i, j
    return None, None

def resolver_combate(a_n, a_c, d_n, d_c, a_d, a_cd, d_d, d_cd, v_a, v_d, modo):
    secuencia = []
    atk_total = [2] * a_c + [1] * a_n  # 2 = crítico, 1 = normal
    def_total = [2] * d_c + [1] * d_n
    atk_total.sort(reverse=True)
    def_total.sort(reverse=True)

    atk_restantes = atk_total[:]
    def_restantes = def_total[:]
    turnos = [("🟥", atk_restantes, def_restantes), ("🟦", def_restantes, atk_restantes)]
    i = 0

    while atk_restantes or def_restantes:
        jugador, propios, enemigos = turnos[i % 2]
        if not propios:
            i += 1
            continue

        idx_p, idx_e = usar_éxito_para_cancelar(propios, enemigos)

        if idx_p is not None and idx_e is not None and modo != "Maximizar daño":
            tipo = "crítico" if propios[idx_p] == 2 else "normal"
            tipo_e = "crítico" if enemigos[idx_e] == 2 else "normal"
            secuencia.append(f"{jugador}🛡️ Bloquea un {tipo_e} enemigo usando un {tipo}")
            propios.pop(idx_p)
            enemigos.pop(idx_e)
        else:
            tipo = "crítico" if propios[0] == 2 else "normal"
            accion = "💥 Golpea con crítico" if tipo == "crítico" else "💥 Golpea"
            secuencia.append(f"{jugador}{accion}")
            propios.pop(0)
        i += 1

    dmg_a = sum([a_cd if x == 2 else a_d for x in atk_restantes])
    dmg_d = sum([d_cd if x == 2 else d_d for x in def_restantes])
    v_a_final = max(0, v_a - dmg_d)
    v_d_final = max(0, v_d - dmg_a)
    return secuencia, v_a_final, v_d_final, dmg_a, dmg_d

# --- Ejecutar y mostrar resultado ---
seq, v_a_res, v_d_res, dmg_a, dmg_d = resolver_combate(
    atk_normals, atk_crits, def_normals, def_crits,
    atk_damage, atk_crit_damage, def_damage, def_crit_damage,
    atk_wounds, def_wounds, estrategia
)

st.subheader("🧠 Resolución paso a paso")
for paso in seq:
    st.markdown(f"- {paso}")

colr1, colr2 = st.columns(2)
with colr1:
    st.metric("🟥 Vida restante Atacante", f"{v_a_res} ❤️", delta=-dmg_d)
with colr2:
    st.metric("🟦 Vida restante Defensor", f"{v_d_res} ❤️", delta=-dmg_a)
def decidir_accion(agente, crits, norms, crit_dano, dano, rival_crits, rival_norms, estrategia):
    acciones = []
    while crits + norms > 0 or rival_crits + rival_norms > 0:
        # Si ya no quedan dados del agente, el rival actúa
        if crits + norms == 0 and rival_crits + rival_norms > 0:
            break
        if estrategia == "Máximo daño":
            # Prioriza atacar con críticos, luego normales
            if crits > 0:
                acciones.append(f"{agente} 💥 Crítico ({crit_dano})")
                crits -= 1
            elif norms > 0:
                acciones.append(f"{agente} 💥 Normal ({dano})")
                norms -= 1
            else:
                break
        elif estrategia == "Defensiva":
            # Prioriza bloquear críticos, luego normales
            if rival_crits > 0 and crits > 0:
                acciones.append(f"{agente} 🛡️ Bloquea Crítico")
                crits -= 1
                rival_crits -= 1
            elif rival_norms > 0 and norms > 0:
                acciones.append(f"{agente} 🛡️ Bloquea Normal")
                norms -= 1
                rival_norms -= 1
            elif rival_norms > 0 and crits > 0:
                acciones.append(f"{agente} 🛡️ Crítico bloquea Normal")
                crits -= 1
                rival_norms -= 1
            elif rival_crits > 0 and norms > 0:
                acciones.append(f"{agente} 🛡️ Normal bloquea Crítico")
                norms -= 1
                rival_crits -= 1
            else:
                # Si no puede bloquear, ataca
                if crits > 0:
                    acciones.append(f"{agente} 💥 Crítico ({crit_dano})")
                    crits -= 1
                elif norms > 0:
                    acciones.append(f"{agente} 💥 Normal ({dano})")
                    norms -= 1
        else:
            # Mejor resultado: mezcla equilibrada
            if rival_crits > 0 and crits > 0:
                acciones.append(f"{agente} 🛡️ Bloquea Crítico")
                crits -= 1
                rival_crits -= 1
            elif rival_norms > 0 and norms > 0:
                acciones.append(f"{agente} 🛡️ Bloquea Normal")
                norms -= 1
                rival_norms -= 1
            elif crits > 0:
                acciones.append(f"{agente} 💥 Crítico ({crit_dano})")
                crits -= 1
            elif norms > 0:
                acciones.append(f"{agente} 💥 Normal ({dano})")
                norms -= 1
            else:
                break
    return acciones



