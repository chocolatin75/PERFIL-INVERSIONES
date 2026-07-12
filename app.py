import streamlit as st
import json
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import base64

st.set_page_config(
    page_title="Perfil Inversionista - OpcionesMarket",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #1565C0);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #2E8B57;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📈 Tu Perfil de Inversionista Personalizado</h1>
    <p>Reporte Educativo • No es asesoramiento financiero • DYOR</p>
</div>
""", unsafe_allow_html=True)

# Modo Familia
modo_familia = st.checkbox("👨‍👩‍👧‍👦 Modo Familia (generar perfil para un familiar)", value=False)
if modo_familia:
    nombre_familiar = st.text_input("Nombre del familiar (ej: Carla, Kaylan, Carlos)", placeholder="Ej: Mi esposa Carla")
    relacion = st.selectbox("Relación", ["Esposa/Esposo", "Hijo/Hija", "Mamá/Papá", "Hermano/Hermana", "Otro familiar"])
else:
    nombre_familiar = None
    relacion = None

# Disclaimer de data
st.info("""
**⚠️ Aviso de Privacidad y Uso de Datos**  
Al completar este cuestionario, aceptas que las respuestas (sin nombre real ni datos de identificación personal) se guarden de forma anónima en los sistemas de **OpcionesMarket** con fines educativos, de mejora de la herramienta y de creación de contenido.  
No se solicita nombre completo, email, teléfono ni información sensible. Tu privacidad está protegida.
""")

with st.form("cuestionario"):
    st.subheader("Cuestionario Rápido")
    
    edad = st.text_input("1. ¿Cuál es tu edad aproximada?", placeholder="Ej: 42")
    st.caption("ℹ️ La edad nos ayuda a entender tu horizonte de tiempo y nivel de riesgo adecuado.")
    
    genero = st.selectbox("2. ¿Cuál es tu género? (Opcional)", ["Prefiero no decir", "Hombre", "Mujer"])
    st.caption("ℹ️ Esto nos ayuda a personalizar ejemplos y lenguaje.")
    
    situacion = st.multiselect("3. ¿Cuál es tu situación familiar?", 
                               ["Soltero/a", "Casado/a", "Con hijos", "Divorciado/a", "Viudo/a", "Otro"], 
                               default=["Soltero/a"])
    st.caption("ℹ️ Esto influye en tus objetivos y cuánto riesgo puedes tomar.")
    
    capital_inicial = st.text_input("4. ¿Cuánto capital aproximado tienes para empezar a invertir? (en USD)", placeholder="Ej: 500, 2000, 10000")
    st.caption("ℹ️ Esto es clave para recomendar estrategias y activos realistas (precio de acciones, opciones, etc.).")
    
    experiencia = st.selectbox("5. ¿Has invertido en el mercado bursátil anteriormente?",
                               ["No", "Sí, menos de 1 año", "Sí, 1-3 años", "Sí, más de 3 años"])
    st.caption("ℹ️ Nos permite ajustar las recomendaciones según tu experiencia.")
    
    objetivo = st.selectbox("6. ¿Cuál es tu objetivo principal al invertir?", 
                            ["Crecer mi dinero a largo plazo", "Generar ingresos extras mensuales", 
                             "Ahorrar para la jubilación", "Comprar casa o auto", "Educación de hijos", "Otro"])
    st.caption("ℹ️ El objetivo define el tipo de estrategia que más te conviene.")
    
    riesgo = st.select_slider("7. ¿Cuál es tu nivel de atrevimiento y riesgo?",
                              options=["Bajo (prefiero seguridad)", "Medio (acepto algo de subida y bajada)", 
                                       "Alto (busco crecimiento fuerte aunque pueda perder)"])
    st.caption("ℹ️ Esto es clave para no recomendarte algo que te quite el sueño.")
    
    horizonte = st.selectbox("8. ¿Por cuánto tiempo planeas dejar el dinero invertido?",
                             ["Menos de 2 años", "2-5 años", "5-10 años", "Más de 10 años / hasta jubilación"])
    st.caption("ℹ️ Un horizonte largo permite estrategias más agresivas.")
    
    aporte = st.text_input("9. ¿Cuánto dinero mensual puedes destinar a tu plan de inversión? (en USD)",
                           placeholder="Ej: $100 - $500")
    st.caption("ℹ️ Esto nos ayuda a diseñar un plan realista y sostenible.")
    
    miedos_options = ["Miedo a perder dinero", "Volatilidad del mercado", "No entiendo las opciones", 
                      "Prefiero solo inversiones seguras", "Falta de tiempo para monitorear", "Otro"]
    miedos = st.multiselect("10. ¿Qué miedos o preferencias tienes?", miedos_options)
    st.caption("ℹ️ Esto nos ayuda a adaptar el plan a lo que te hace sentir cómodo.")
    
    # Calculadora de Riesgo adicional
    st.subheader("🧮 Calculadora Rápida de Tolerancia al Riesgo")
    st.write("Responde estas 3 preguntas adicionales para refinar tu perfil de riesgo:")
    
    q1 = st.radio("Si tu portafolio cae 20% en un mes, ¿qué haces?", 
                  ["Vendo todo para no perder más", "Espero y no hago nada", "Compro más barato"])
    q2 = st.radio("¿Cuánto tiempo puedes esperar sin necesitar el dinero?", 
                  ["Menos de 1 año", "1-3 años", "Más de 5 años"])
    q3 = st.radio("¿Prefieres un retorno estable del 5-7% o uno que pueda ser 15% pero con caídas grandes?", 
                  ["Estable 5-7%", "Mezcla", "Alto potencial aunque volátil"])
    
    submitted = st.form_submit_button("🚀 Generar mi Reporte Personalizado", use_container_width=True)

if submitted:
    if not edad or not capital_inicial or not aporte:
        st.error("Por favor completa edad, capital inicial y aporte mensual.")
    else:
        st.success("✅ ¡Reporte Generado!")
        
        try:
            capital = int(capital_inicial.replace(",", "").replace("$", "").strip())
            aporte_mensual = int(aporte.replace(",", "").replace("$", "").strip())
        except:
            capital = 500
            aporte_mensual = 200
        
        # Score de riesgo de la calculadora
        score_riesgo = 0
        if q1 == "Compro más barato":
            score_riesgo += 3
        elif q1 == "Espero y no hago nada":
            score_riesgo += 2
        else:
            score_riesgo += 1
            
        if q2 == "Más de 5 años":
            score_riesgo += 3
        elif q2 == "1-3 años":
            score_riesgo += 2
        else:
            score_riesgo += 1
            
        if q3 == "Alto potencial aunque volátil":
            score_riesgo += 3
        elif q3 == "Mezcla":
            score_riesgo += 2
        else:
            score_riesgo += 1
        
        # Perfil combinado
        if score_riesgo <= 4:
            nivel_riesgo_final = "Conservador"
        elif score_riesgo <= 7:
            nivel_riesgo_final = "Moderado"
        else:
            nivel_riesgo_final = "Agresivo"
        
        # Header del reporte
        if modo_familia and nombre_familiar:
            st.subheader(f"👤 Perfil de {nombre_familiar} ({relacion})")
        else:
            st.subheader("👤 Tu Perfil")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Edad:** {edad} años")
            st.write(f"**Situación:** {', '.join(situacion)}")
            st.write(f"**Objetivo:** {objetivo}")
            st.write(f"**Nivel de Riesgo Final:** {nivel_riesgo_final} (score {score_riesgo}/9)")
        with col2:
            st.write(f"**Capital inicial:** ${capital:,}")
            st.write(f"**Aporte mensual:** ${aporte_mensual:,}")
            st.write(f"**Riesgo declarado:** {riesgo}")
            st.write(f"**Horizonte:** {horizonte}")
        
        # Allocation Pie
        st.subheader("📊 Distribución Recomendada")
        fig, ax = plt.subplots(figsize=(6,4))
        if nivel_riesgo_final == "Conservador" or "Bajo" in riesgo:
            sizes = [35, 5, 60]
            labels = ['Acciones/ETFs', 'Opciones', 'Efectivo/Bonos']
        elif nivel_riesgo_final == "Agresivo" or "Alto" in riesgo:
            sizes = [55, 30, 15]
            labels = ['Acciones/ETFs', 'Opciones', 'Efectivo']
        else:
            sizes = [50, 20, 30]
            labels = ['Acciones/ETFs', 'Opciones', 'Efectivo']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#2E8B57', '#1565C0', '#FFC107'])
        ax.axis('equal')
        st.pyplot(fig)
        
        # Proyecciones 3 escenarios
        st.subheader("🚀 Proyección de Crecimiento (3 escenarios)")
        years = 10
        scenarios = {
            "Pesimista (6% anual)": 1.06,
            "Realista (9% anual)": 1.09,
            "Optimista (12% anual)": 1.12
        }
        
        cols = st.columns(3)
        for idx, (name, rate) in enumerate(scenarios.items()):
            fv = capital
            for y in range(years):
                fv = fv * rate + aporte_mensual * 12
            with cols[idx]:
                st.metric(name, f"${int(fv):,}")
        
        # Gráfica de proyección realista
        fig2, ax2 = plt.subplots(figsize=(8,4))
        values = [capital]
        fv = capital
        for y in range(1, years+1):
            fv = fv * 1.09 + aporte_mensual * 12
            values.append(fv)
        ax2.plot(range(0, years+1), values, marker='o', linewidth=2.5, color='#2E8B57')
        ax2.fill_between(range(0, years+1), values, alpha=0.2, color='#2E8B57')
        ax2.set_xlabel("Años")
        ax2.set_ylabel("Valor Estimado (USD)")
        ax2.set_title("Proyección Realista (~9% anual) con aportes mensuales")
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
        
        st.write(f"**En {years} años (escenario realista) podrías estar cerca de: ${int(values[-1]):,}**")
        
        # === RECOMENDACIONES DINÁMICAS POR CAPITAL ===
        st.subheader("🎯 Recomendaciones Personalizadas (basadas en tu capital y perfil)")
        st.markdown("**⚠️ Importante:** Esto es educativo. Consulta a un asesor financiero. No soy tu asesor.")
        
        # Top ETFs / Acciones dinámicos
        if capital < 800:
            st.write("**Capital bajo ($500-$800):** Enfócate en ETFs de bajo precio o fractional shares. Evita opciones por ahora.")
            etfs_recomendados = [
                "VOO (S&P 500) - Fractional shares",
                "SCHD (Dividendos de calidad)",
                "VT (Mercado mundial)",
                "BND (Bonos) para estabilidad",
                "JEPI (Ingresos mensuales - si broker lo permite)"
            ]
            acciones = ["Ninguna por ahora (usa ETFs). Prueba paper trading de opciones."]
            estrategia = "Dollar Cost Averaging mensual en 2-3 ETFs. Paper trading de opciones 3 meses."
        elif capital < 2500:
            st.write("**Capital medio ($800-$2500):** Puedes empezar La Rueda en acciones baratas + ETFs.")
            etfs_recomendados = [
                "VOO o VTI",
                "SCHD",
                "JEPI (ingresos)",
                "QQQ (tecnología)",
                "VXUS (internacional)"
            ]
            acciones = [
                "F (Ford) o SOFI (fintech) para CSP baratos",
                "INTC o AMD si te gusta tech",
                "KO o PG para dividendos estables"
            ]
            estrategia = "La Rueda en 1-2 acciones de bajo precio + 60% en ETFs. Covered Calls cuando te asignen."
        elif capital < 10000:
            st.write("**Capital bueno ($2500-$10k):** Puedes hacer La Rueda completa y LEAPs pequeños.")
            etfs_recomendados = [
                "VOO / SPY",
                "SCHD / JEPI",
                "QQQ",
                "IWM (small caps)",
                "ARKK o SOXX (si agresivo)"
            ]
            acciones = [
                "AAPL, MSFT, NVDA (LEAPs o CSP)",
                "AMZN, META",
                "XOM o CVX (energía + dividendos)"
            ]
            estrategia = "Wheel Strategy + LEAPs en 1-2 nombres de crecimiento. 40-50% ETFs core."
        else:
            st.write("**Capital sólido (>$10k):** Portafolio completo con opciones avanzadas.")
            etfs_recomendados = [
                "VOO + QQQ core",
                "SCHD + JEPI para ingresos",
                "VXUS + EEM",
                "IWM o VB",
                "TQQQ / SQQQ solo si agresivo y con tamaño pequeño"
            ]
            acciones = [
                "NVDA, AVGO, AMD (LEAPs)",
                "AAPL, MSFT, GOOGL",
                "JPM, BAC, GS (financieros)"
            ]
            estrategia = "Core-Satellite: 50% ETFs + 30% Wheel/LEAPs + 20% cash/opciones tácticas."
        
        st.write("**Top 5 ETFs recomendados para ti:**")
        for i, etf in enumerate(etfs_recomendados, 1):
            st.write(f"{i}. {etf}")
        
        st.write("**Acciones / Ideas de opciones:**")
        for acc in acciones:
            st.write(f"• {acc}")
        
        st.write(f"**Estrategia principal recomendada:** {estrategia}")
        
        # Timeline
        st.subheader("📅 Timeline de Acción (próximos 6 meses)")
        st.write("""
        - **Mes 1:** Abre/configura cuenta de brokerage (Robinhood, Fidelity, IBKR). Deposita capital inicial. Compra primeros ETFs.
        - **Mes 2-3:** Establece aportes automáticos mensuales. Practica paper trading de CSP/Covered Calls.
        - **Mes 4:** Revisa performance. Si capital y confianza suben, abre primera posición real de Wheel.
        - **Mes 5-6:** Ajusta allocation según resultados. Revisa miedos y rebalancea si es necesario.
        - **Cada 3 meses:** Revisión completa del plan + actualiza capital y objetivos.
        """)
        
        # Botón de contacto
        st.subheader("🤝 ¿Quieres ayuda personalizada?")
        st.info("Si quieres que te ayude a refinar este plan o armar trades específicos, escríbeme en X: **@chocolatin75** o **@OpcionesMarket**")
        
        # PDF Download - Versión limpia de 1 página
        st.subheader("📄 Descargar Reporte en PDF")
        
        def create_pdf():
            import tempfile
            import os
            
            # Guardar gráficas en temp files
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_pie:
                pie_path = tmp_pie.name
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_growth:
                growth_path = tmp_growth.name
            
            # Pie chart
            fig_pie, ax_pie = plt.subplots(figsize=(4.2, 3.2))
            if nivel_riesgo_final == "Conservador" or "Bajo" in riesgo:
                sizes = [35, 5, 60]
                labels = ['Acciones/ETFs', 'Opciones', 'Efectivo']
            elif nivel_riesgo_final == "Agresivo" or "Alto" in riesgo:
                sizes = [55, 30, 15]
                labels = ['Acciones/ETFs', 'Opciones', 'Efectivo']
            else:
                sizes = [50, 20, 30]
                labels = ['Acciones/ETFs', 'Opciones', 'Efectivo']
            ax_pie.pie(sizes, labels=labels, autopct='%1.0f%%', colors=['#2E8B57', '#1565C0', '#FFC107'], textprops={'fontsize': 8})
            ax_pie.set_title("Distribución", fontsize=10)
            fig_pie.savefig(pie_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close(fig_pie)
            
            # Growth chart
            fig_g, ax_g = plt.subplots(figsize=(4.8, 3.0))
            vals = [capital]
            fv = capital
            for y in range(1, 11):
                fv = fv * 1.09 + aporte_mensual * 12
                vals.append(fv)
            ax_g.plot(range(0, 11), vals, marker='o', markersize=4, linewidth=2, color='#2E8B57')
            ax_g.fill_between(range(0, 11), vals, alpha=0.15, color='#2E8B57')
            ax_g.set_xlabel("Años", fontsize=8)
            ax_g.set_ylabel("USD", fontsize=8)
            ax_g.set_title("Proyección ~9%", fontsize=10)
            ax_g.tick_params(labelsize=7)
            ax_g.grid(True, alpha=0.3)
            fig_g.savefig(growth_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close(fig_g)
            
            # === PDF ===
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.set_auto_page_break(auto=False)  # Control total, 1 página
            pdf.add_page()
            
            # Header
            pdf.set_fill_color(46, 139, 87)
            pdf.rect(0, 0, 210, 22, 'F')
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 16)
            pdf.set_xy(0, 5)
            pdf.cell(210, 8, "OpcionesMarket", align="C")
            pdf.set_font("Arial", "", 8)
            pdf.set_xy(0, 13)
            pdf.cell(210, 5, "Perfil de Inversionista Personalizado  |  Educativo - DYOR", align="C")
            
            # Title
            pdf.set_text_color(0, 0, 0)
            pdf.set_y(26)
            pdf.set_font("Arial", "B", 13)
            if modo_familia and nombre_familiar:
                pdf.cell(0, 7, f"Perfil de: {nombre_familiar} ({relacion})", align="C", ln=True)
            else:
                pdf.cell(0, 7, "Tu Perfil Personalizado", align="C", ln=True)
            
            # Datos Clave
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 6, "Datos Clave", ln=True)
            pdf.set_font("Arial", "", 8)
            y = pdf.get_y()
            pdf.set_xy(10, y)
            pdf.cell(95, 5, f"Edad: {edad} años")
            pdf.cell(95, 5, f"Capital inicial: ${capital:,}", ln=True)
            pdf.cell(95, 5, f"Aporte mensual: ${aporte_mensual:,}")
            pdf.cell(95, 5, f"Riesgo: {nivel_riesgo_final}", ln=True)
            pdf.cell(95, 5, f"Horizonte: {horizonte}")
            pdf.cell(95, 5, f"Objetivo: {objetivo[:28]}", ln=True)
            
            pdf.ln(2)
            
            # Visuales title
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "Visuales", ln=True)
            
            # Images side by side
            y_img = pdf.get_y()
            try:
                pdf.image(pie_path, x=12, y=y_img, w=80)
                pdf.image(growth_path, x=105, y=y_img, w=90)
            except Exception:
                pdf.set_xy(10, y_img)
                pdf.cell(0, 5, "(Graficas no disponibles)", ln=True)
            
            # Move below images
            pdf.set_y(y_img + 58)
            
            # Estrategia
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "Estrategia Recomendada", ln=True)
            pdf.set_font("Arial", "", 8)
            pdf.multi_cell(0, 4, estrategia)
            
            # Top ETFs
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "Top ETFs / Activos Recomendados", ln=True)
            pdf.set_font("Arial", "", 8)
            for etf in etfs_recomendados[:5]:
                pdf.cell(0, 4, f"  - {etf}", ln=True)
            
            # Timeline
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "Timeline de Accion (6 meses)", ln=True)
            pdf.set_font("Arial", "", 7)
            pdf.multi_cell(0, 3.5, "Mes 1: Configura cuenta + primeros ETFs.  |  Mes 2-3: Aportes automaticos + paper trading.  |  Mes 4: Primera posicion real.  |  Cada 3 meses: Revision completa.")
            
            # Footer fijo en la misma página
            pdf.set_fill_color(46, 139, 87)
            pdf.rect(0, 280, 210, 17, 'F')
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 8)
            pdf.set_xy(0, 282)
            pdf.cell(210, 4, "Hecho con @OpcionesMarket  |  X: @chocolatin75  |  Educativo - DYOR", align="C")
            pdf.set_font("Arial", "", 6)
            pdf.set_xy(0, 287)
            pdf.cell(210, 4, "No soy asesor financiero. Este reporte es solo para educacion y entretenimiento. Data pertenece a OpcionesMarket.", align="C")
            
            # Cleanup temp files
            try:
                os.unlink(pie_path)
                os.unlink(growth_path)
            except:
                pass
            
            return bytes(pdf.output())
        
        pdf_bytes = create_pdf()
        st.download_button(
            label="📥 Descargar Reporte PDF Completo (1 página + branding)",
            data=pdf_bytes,
            file_name=f"Perfil_OpcionesMarket_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        
        # JSON download
        respuestas = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "modo_familia": modo_familia,
            "nombre_familiar": nombre_familiar,
            "edad": edad,
            "genero": genero,
            "capital": capital,
            "aporte": aporte_mensual,
            "riesgo_final": nivel_riesgo_final,
            "objetivo": objetivo,
            "horizonte": horizonte,
            "estrategia": estrategia,
            "etfs": etfs_recomendados
        }
        st.download_button(
            label="📥 Descargar datos (JSON)",
            data=json.dumps(respuestas, ensure_ascii=False, indent=2),
            file_name="perfil_respuestas.json",
            mime="application/json"
        )
        
        with st.expander("📢 Versión lista para publicar en X"):
            post = f"""📈 Nuevo Perfil de Inversionista

Edad: {edad} | Capital: ~${capital:,}
Riesgo: {nivel_riesgo_final}
Objetivo: {objetivo}
Horizonte: {horizonte}

Estrategia: {estrategia[:80]}...

¿Te identificas? Comenta tu perfil 👇

#OpcionesMarket #LaRueda"""
            st.code(post, language="markdown")

st.caption("Herramienta educativa de @OpcionesMarket • DYOR • No soy asesor financiero")
