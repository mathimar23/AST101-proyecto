"""EstrellaLab: simulador didáctico de propiedades estelares.

Ejecutar:
    pip install streamlit matplotlib
    python -m streamlit run app.py

Proyecto educativo: el diagrama incluye una secuencia principal ESQUEMÁTICA,
no una base de datos observacional ni un modelo completo de evolución estelar.
"""

import math

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import FuncFormatter


# Constantes y ejemplos educativos
TEMPERATURA_SOL = 5772  # K
EJEMPLOS = {
    "Parecida al Sol": (5800, 1.0),
    "Estrella fría y tenue (hipotética)": (3200, 0.01),
    "Gigante roja (hipotética)": (3600, 1000.0),
    "Estrella azul luminosa (hipotética)": (15000, 10000.0),
}


def radio_en_radios_solares(temperatura_k, luminosidad_solar):
    """L = 4*pi*R^2*sigma*T^4, expresada respecto del Sol."""
    return math.sqrt(luminosidad_solar) * (TEMPERATURA_SOL / temperatura_k) ** 2


def color_aproximado(temperatura_k):
    """Color solo ilustrativo: interpolación entre tonos, NO fotometría real."""
    puntos = [
        (2500, (255, 112, 76)),
        (3500, (255, 164, 100)),
        (4800, (255, 213, 167)),
        (5800, (255, 242, 218)),
        (7500, (242, 246, 255)),
        (12000, (193, 218, 255)),
        (30000, (151, 190, 255)),
    ]
    for i in range(len(puntos) - 1):
        t0, c0 = puntos[i]
        t1, c1 = puntos[i + 1]
        if temperatura_k <= t1:
            f = max(0.0, min(1.0, (temperatura_k - t0) / (t1 - t0)))
            rgb = [round(a + (b - a) * f) for a, b in zip(c0, c1)]
            return "#{:02x}{:02x}{:02x}".format(*rgb)
    return "#97beff"


def dibujar_diagrama_hr(temperatura, luminosidad, color):
    """Diagrama HR con una curva de referencia meramente esquemática."""
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    fig.patch.set_facecolor("#101827")
    ax.set_facecolor("#101827")

    # Valores ilustrativos para dar contexto a la secuencia principal.
    # NO representan un catálogo astronómico de estrellas medidas.
    temperaturas_ref = [3000, 3500, 4000, 5000, 5772, 6500,
                        7500, 10000, 15000, 20000, 30000]
    luminosidades_ref = [0.001, 0.018, 0.08, 0.4, 1, 3,
                         12, 70, 1000, 10000, 100000]
    ax.plot(
        temperaturas_ref, luminosidades_ref,
        color="#7f9fcf", linewidth=3, alpha=0.8,
        label="Secuencia principal (esquemática)",
    )
    ax.scatter(
        [TEMPERATURA_SOL], [1], s=65, color="#ffdc7c",
        edgecolors="white", linewidths=0.8, zorder=4, label="Sol",
    )
    ax.scatter(
        [temperatura], [luminosidad], s=270, color=color,
        edgecolors="white", linewidths=2, zorder=6, label="Tu estrella",
    )

    # En un diagrama HR convencional las estrellas más calientes van a la izquierda.
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(32000, 2500)
    ax.set_ylim(0.0008, 200000)
    ax.set_xticks([30000, 15000, 10000, 6000, 4000, 3000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:,.0f}"))
    ax.tick_params(axis="both", colors="#e1e8f5", labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#7183a0")
    ax.grid(which="major", color="white", alpha=0.12, linestyle="--")
    ax.set_xlabel("Temperatura superficial (K)  |  más caliente a la izquierda",
                  color="#e1e8f5", labelpad=10)
    ax.set_ylabel("Luminosidad (L / L☉)", color="#e1e8f5", labelpad=10)
    legend = ax.legend(loc="lower left", facecolor="#1d2b41",
                       edgecolor="#526784", fontsize=9)
    for texto in legend.get_texts():
        texto.set_color("white")
    fig.tight_layout()
    return fig


def cargar_ejemplo(nombre):
    temperatura, luminosidad = EJEMPLOS[nombre]
    st.session_state.temperatura_k = temperatura
    st.session_state.log_luminosidad = math.log10(luminosidad)


def main():
    st.set_page_config(page_title="EstrellaLab", page_icon="⭐", layout="wide")
    st.title("⭐ EstrellaLab")
    st.write(
        "**Explora cómo la temperatura y la luminosidad se relacionan con el "
        "radio y la posición de una estrella en el diagrama Hertzsprung–Russell.**"
    )

    if "temperatura_k" not in st.session_state:
        st.session_state.temperatura_k = 5800
    if "log_luminosidad" not in st.session_state:
        st.session_state.log_luminosidad = 0.0

    with st.sidebar:
        st.header("🎛️ Laboratorio")
        st.slider(
            "Temperatura superficial (K)",
            min_value=2500, max_value=30000, step=100,
            key="temperatura_k",
            help="Temperatura efectiva de la superficie estelar.",
        )
        st.slider(
            "Logaritmo de luminosidad (L / L☉)",
            min_value=-3.0, max_value=5.0, step=0.1,
            key="log_luminosidad",
            help="0 = luminosidad solar; 1 = 10 veces; 2 = 100 veces; -1 = 0,1 veces.",
        )
        st.caption("La escala logarítmica permite comparar estrellas muy distintas.")
        st.divider()
        st.subheader("Cargar un ejemplo")
        ejemplo = st.selectbox("Selecciona un escenario", list(EJEMPLOS))
        st.button("Aplicar ejemplo", on_click=cargar_ejemplo,
                  args=(ejemplo,), use_container_width=True)
        st.info("Los ejemplos, excepto la referencia solar, son escenarios educativos hipotéticos.")

    temperatura = st.session_state.temperatura_k
    luminosidad = 10 ** st.session_state.log_luminosidad
    radio = radio_en_radios_solares(temperatura, luminosidad)
    color = color_aproximado(temperatura)

    m1, m2, m3 = st.columns(3)
    m1.metric("🌡️ Temperatura", f"{temperatura:,} K")
    m2.metric("✨ Luminosidad", f"{luminosidad:.3g} L☉")
    m3.metric("📏 Radio estimado", f"{radio:.2f} R☉")

    columna_estrella, columna_diagrama = st.columns([1, 1.65], gap="large")
    with columna_estrella:
        st.subheader("Tu estrella")
        # Tamaño de dibujo limitado para que pueda verse toda estrella en pantalla.
        tamano = round(max(55, min(165, 90 + 28 * math.log10(max(radio, 0.01)))))
        st.markdown(
            f"""
            <div style="height:290px; display:flex; align-items:center;
                        justify-content:center; background:#101827;
                        border-radius:16px; overflow:hidden;">
              <div style="width:{tamano}px; height:{tamano}px;
                          border-radius:50%;
                          background:radial-gradient(circle at 37% 32%,
                                     #fff 0%, {color} 45%, {color} 88%, #c77556 100%);
                          box-shadow:0 0 30px 9px {color}77,
                                     0 0 90px 25px {color}33;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Ilustración aproximada: el color y el tamaño dibujados no son una "
            "simulación física exacta ni están a escala."
        )
        st.write(
            f"Esta estrella emitiría unas **{luminosidad:.3g} veces** la "
            f"luminosidad del Sol y tendría un radio aproximado de "
            f"**{radio:.2f} radios solares** si se comporta como un cuerpo "
            "que cumple la ley de Stefan–Boltzmann."
        )

    with columna_diagrama:
        st.subheader("Diagrama Hertzsprung–Russell")
        figura = dibujar_diagrama_hr(temperatura, luminosidad, color)
        st.pyplot(figura, use_container_width=True)
        plt.close(figura)
        st.caption(
            "La línea azul es una guía didáctica aproximada de la secuencia "
            "principal, no datos de observaciones reales."
        )

    st.divider()
    st.subheader("🔬 ¿De dónde sale el radio?")
    st.write(
        "La **ley de Stefan–Boltzmann** relaciona luminosidad (L), radio (R) "
        "y temperatura efectiva (T) de una estrella:"
    )
    st.latex(r"L = 4\pi R^2 \sigma T^4")
    st.write("Al dividir por la misma ecuación para el Sol, obtenemos:")
    st.latex(r"\frac{R}{R_\odot} = \sqrt{\frac{L}{L_\odot}}"
             r"\left(\frac{T_\odot}{T}\right)^2")
    st.write(
        f"Con T☉ = {TEMPERATURA_SOL} K, T = {temperatura:,} K y "
        f"L = {luminosidad:.3g} L☉, resulta R ≈ {radio:.2f} R☉."
    )

    with st.expander("💡 Mini desafío: cambia solo la temperatura"):
        st.write(
            "Si mantienes fija la luminosidad y **duplicas la temperatura**, "
            "¿cómo cambia el radio calculado?"
        )
        respuesta = st.radio(
            "Elige una respuesta", ["Se duplica", "Se reduce a la mitad",
                                  "Se reduce a la cuarta parte"],
            index=None,
        )
        if respuesta:
            if respuesta == "Se reduce a la cuarta parte":
                st.success("¡Correcto! A luminosidad fija, R es proporcional a 1/T².")
            else:
                st.warning("Revisa el término (T☉/T)² de la ecuación.")

    with st.expander("📚 Interpretación y límites del simulador"):
        st.markdown(
            """
            - **Temperatura efectiva:** se expresa en kelvin (K) y se relaciona
              con la distribución espectral de radiación.
            - **Luminosidad:** energía total emitida por unidad de tiempo;
              aquí se expresa en unidades solares (L☉).
            - **Diagrama HR:** relaciona temperatura y luminosidad; por
              convención, la temperatura suele aumentar hacia la izquierda.
            - **Secuencia principal:** zona donde se ubican estrellas que
              fusionan hidrógeno en sus núcleos.
            - **Limitaciones:** no todas las combinaciones de temperatura y
              luminosidad corresponden a estrellas estables; el programa no
              determina masa, edad, composición química ni fase evolutiva.
              Tampoco reemplaza datos astronómicos observacionales.
            """
        )

    st.caption(
        "EstrellaLab | Prototipo educativo de Ciencias de la Computación + "
        "Astronomía | Todo el programa está contenido en app.py"
    )


if __name__ == "__main__":
    main()
