import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo Kill Team 3", layout="wide")

st.title("⚔️ Simulador de Combate Cuerpo a Cuerpo - Kill Team 3")

col1, col2 = st.columns(2)

with col1:
    st.header("🟥 Atacante")
    atacante_normales = st.number_input("Éxitos normales", min_value=0, value=2, key="a_n")
    atacante_criticos = st.number_input("Éxitos críticos", min_value=0, value=1, key="a_c")
    atacante_vida = st.number_input("Vida restante", min_value=1, value=8, key="a_v")
    atacante_daño_normal = st.number_input("Daño por normal", min_value=1, value=3, key="a_dn")
    atacante_daño_critico = st.number_input("Daño por crítico", min_value=1, value=5, key="a_dc")

with col2:
    st.header("🟦 Defensor")
    defensor_normales = st.number_input("Éxitos normales", min_value=0, value=2, key="d_n")
    defensor_criticos = st.number_input("Éxitos críticos", min_value=0, value=1, key="d_c")
    defensor_vida = st.number_input("Vida restante", min_value=1, value=8, key="d_v")
    defensor_daño_normal = st.number_input("Daño por normal", min_value=1, value=3, key="d_dn")
    defensor_daño_critico = st.number_input("Daño por crítico", min_value=1, value=5, key="d_dc")

estrategia = st.selectbox("🎯 Estrategia", ["Máximo daño", "Defensiva", "Mejor resultado"])

if st.button("💥 Resolver combate"):
    log = []
    vida_atacante = atacante_vida
    vida_defensor = defensor_vida

    pool_atacante = [{"tipo": "critico", "daño": atacante_daño_critico}] * atacante_criticos + \
                    [{"tipo": "normal", "daño": atacante_daño_normal}] * atacante_normales
    pool_defensor = [{"tipo": "critico", "daño": defensor_daño_critico}] * defensor_criticos + \
                    [{"tipo": "normal", "daño": defensor_daño_normal}] * defensor_normales

    pool_atacante.sort(key=lambda x: 0 if x["tipo"] == "critico" else 1)
    pool_defensor.sort(key=lambda x: 0 if x["tipo"] == "critico" else 1)

    turno_atacante = True
    i_a, i_d = 0, 0
    used_a, used_d = set(), set()

    def puede_bloquear(bloqueador, rival, idx_b, tipo_rival):
        for i, d in enumerate(bloqueador):
            if i in used_d: continue
            if d["tipo"] == "critico" or (d["tipo"] == "normal" and tipo_rival == "normal"):
                used_d.add(i)
                log.append(f"🟦🛡️ Defensor bloquea {tipo_rival} del atacante.")
                return True
        return False

    def bloquear(pool_self, pool_rival, used_self, tipo):
        for i, dado in enumerate(pool_self):
            if i in used_self: continue
            if dado["tipo"] == tipo:
                used_self.add(i)
                return True
        return False

    while len(used_a) < len(pool_atacante) or len(used_d) < len(pool_defensor):
        if turno_atacante:
            for i, dado in enumerate(pool_atacante):
                if i in used_a: continue
                bloqueado = False
                if estrategia == "Defensiva":
                    bloqueado = puede_bloquear(pool_defensor, pool_atacante, i, dado["tipo"])
                elif estrategia == "Máximo daño":
                    vida_defensor -= dado["daño"]
                    used_a.add(i)
                    log.append(f"🟥💥 Atacante golpea con {dado['tipo']} ({dado['daño']} daño). Vida defensor: {max(0, vida_defensor)}")
                    if vida_defensor <= 0:
                        log.append("☠️ ¡El defensor ha muerto!")
                        break
                elif estrategia == "Mejor resultado":
                    # Bloquea si tiene críticos disponibles y el defensor aún tiene éxitos
                    if vida_defensor - dado["daño"] > 0 and puede_bloquear(pool_defensor, pool_atacante, i, dado["tipo"]):
                        bloqueado = True
                    else:
                        vida_defensor -= dado["daño"]
                        log.append(f"🟥💥 Atacante golpea con {dado['tipo']} ({dado['daño']} daño). Vida defensor: {max(0, vida_defensor)}")
                    used_a.add(i)
                    if vida_defensor <= 0:
                        log.append("☠️ ¡El defensor ha muerto!")
                        break
                if not bloqueado and estrategia == "Defensiva":
                    vida_defensor -= dado["daño"]
                    used_a.add(i)
                    log.append(f"🟥💥 Atacante golpea con {dado['tipo']} ({dado['daño']} daño). Vida defensor: {max(0, vida_defensor)}")
                    if vida_defensor <= 0:
                        log.append("☠️ ¡El defensor ha muerto!")
                        break
            turno_atacante = False
        else:
            for i, dado in enumerate(pool_defensor):
                if i in used_d: continue
                bloqueado = False
                if estrategia == "Máximo daño":
                    bloqueado = puede_bloquear(pool_atacante, pool_defensor, i, dado["tipo"])
                elif estrategia == "Defensiva":
                    vida_atacante -= dado["daño"]
                    used_d.add(i)
                    log.append(f"🟦💥 Defensor golpea con {dado['tipo']} ({dado['daño']} daño). Vida atacante: {max(0, vida_atacante)}")
                    if vida_atacante <= 0:
                        log.append("☠️ ¡El atacante ha muerto!")
                        break
                elif estrategia == "Mejor resultado":
                    if vida_atacante - dado["daño"] > 0 and puede_bloquear(pool_atacante, pool_defensor, i, dado["tipo"]):
                        bloqueado = True
                    else:
                        vida_atacante -= dado["daño"]
                        used_d.add(i)
                        log.append(f"🟦💥 Defensor golpea con {dado['tipo']} ({dado['daño']} daño). Vida atacante: {max(0, vida_atacante)}")
                        if vida_atacante <= 0:
                            log.append("☠️ ¡El atacante ha muerto!")
                            break
                if not bloqueado and estrategia == "Máximo daño":
                    vida_atacante -= dado["daño"]
                    used_d.add(i)
                    log.append(f"🟦💥 Defensor golpea con {dado['tipo']} ({dado['daño']} daño). Vida atacante: {max(0, vida_atacante)}")
                    if vida_atacante <= 0:
                        log.append("☠️ ¡El atacante ha muerto!")
                        break
            turno_atacante = True

        if vida_atacante <= 0 or vida_defensor <= 0:
            break

    st.subheader("🔎 Resultado del combate:")
    for linea in log:
        st.markdown(linea)
        