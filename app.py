import streamlit as st
import json
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Perfil Inversionista - OpcionesMarket", layout="centered")

st.title("📈 Tu Perfil de Inversionista Personalizado")
st.markdown("**Reporte Educativo** • Contenido educativo y de entretenimiento. No es asesoramiento financiero. DYOR.")

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
    
    capital_inicial = st.text_input("4. ¿Cuánto capital aproximado tienes para empezar a invertir? (en USD)", placeholder="Ej: 1000")
    st.caption("ℹ️ Esto es clave para recomendar estrategias realistas.")
    
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
                           placeholder="Ej: $200 - $500")
    st.caption("ℹ️ Esto nos ayuda a diseñar un plan realista y sostenible.")
    
    miedos_options = ["Miedo a perder dinero", "Volatilidad del mercado", "No entiendo las opciones", 
                      "Prefiero solo inversiones seguras", "Falta de tiempo para monitorear", "Otro"]
    miedos = st.multiselect("10. ¿Qué miedos o preferencias tienes?", miedos_options)
    st.caption("ℹ️ Esto nos ayuda a adaptar el plan a lo que te hace sentir cómodo.")
    
    submitted = st.form_submit_button("🚀 Generar mi Reporte Personalizado", use_container_width=True)

if submitted:
    if not edad or not capital_inicial or not aporte:
        st.error("Por favor completa edad, capital inicial y aporte mensual.")
    else:
        st.success("✅ ¡Reporte Generado!")
        
        try:
            capital = int(capital_inicial)
            aporte_mensual = int(aporte)
        except:
            capital = 500
            aporte_mensual = 200
        
        st.subheader("👤 Tu Perfil")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Edad:** {edad} años")
            st.write(f"**Situación:** {', '.join(situacion)}")
            st.write(f"**Objetivo:** {objetivo}")
        with col2:
            st.write(f"**Capital inicial:** ${capital:,}")
            st.write(f"**Aporte mensual:** ${aporte_mensual:,}")
            st.write(f"**Riesgo:** {riesgo}")
            st.write(f"**Horizonte:** {horizonte}")
        
        # Allocation
        st.subheader("📊 Distribución Recomendada")
        fig, ax = plt.subplots()
        if "Bajo" in riesgo:
            sizes = [40, 10, 50]
        elif "Alto" in riesgo:
            sizes = [60, 25, 15]
        else:
            sizes = [50, 20, 30]
        ax.pie(sizes, labels=['Acciones/ETFs', 'Opciones', 'Efectivo'], autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
        
        # Proyección Avanzada (3 escenarios)
        st.subheader("🚀 Proyección de Crecimiento (3 escenarios)")
        years = 10
        scenarios = {"Pesimista (6%)": 1.06, "Realista (9%)": 1.09, "Optimista (12%)": 1.12}
        
        for name, rate in scenarios.items():
            fv = capital
            for y in range(years):
                fv = fv * rate + aporte_mensual * 12
            st.write(f"**{name}:** ~${int(fv):,} en {years} años")
        
        # Recomendaciones dinámicas
        st.subheader("🎯 Recomendaciones Personalizadas")
        st.markdown("**Importante:** Esto es educativo. Consulta a un asesor financiero.")
        
        if capital < 1000:
            st.write("**Inicio recomendado:** Paper trading + ETFs baratos")
            etfs = "VOO, SPY, SCHD"
        elif "Bajo" in riesgo:
            st.write("**Enfoque conservador:** Dividendos y estabilidad")
            etfs = "SCHD, JEPI, VOO"
        elif "Alto" in riesgo:
            st.write("**Enfoque agresivo:** Crecimiento y opciones")
            etfs = "QQQ, VGT, SOXX"
        else:
            st.write("**Enfoque equilibrado:** La Rueda + dividendos")
            etfs = "VOO, SCHD, JEPI"
        
        st.write(f"**Top ETFs recomendados:** {etfs}")
        
        st.write("**Timeline sugerido:**")
        st.write("• Mes 1-3: Configura cuenta y empieza aportes")
        st.write("• Mes 4-6: Revisa y ajusta")
        st.write("• Cada 3 meses: Evalúa progreso")
        
        with st.expander("📢 Versión para publicar en X"):
            st.code(f"Perfil: {edad} años | Capital ~${capital} | Horizonte: {horizonte}\n#OpcionesMarket", language="markdown")
        
        st.button("Quiero que Alex me ayude a refinar esto", help="Escríbeme por X @chocolatin75 o WhatsApp")

st.caption("Herramienta educativa de @OpcionesMarket • DYOR")
