"""Forja Estelar: simulador didáctico de propiedades estelares.

Ejecutar:
    pip install streamlit matplotlib
    python -m streamlit run hola.py

Proyecto educativo: el diagrama incluye una secuencia principal ESQUEMÁTICA,
no una base de datos observacional ni un modelo completo de evolución estelar.
"""

import math

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter


# Constante de referencia solar
TEMPERATURA_SOL = 5772  # K


def formatear_numero(valor, decimales=3):
    """Representa números sin notación científica, con formato chileno.

    Ejemplos: 20000 -> 20.000; 1.259 -> 1,259; 0.001 -> 0,001.
    """
    numero = f"{valor:,.{decimales}f}"
    if decimales > 0:
        numero = numero.rstrip("0").rstrip(".")
    return numero.replace(",", "#").replace(".", ",").replace("#", ".")


def formatear_luminosidad(luminosidad):
    """Evita redondear estrellas poco luminosas a 0,002 o 0,000."""
    return formatear_numero(luminosidad, 5 if luminosidad < 0.01 else 3)


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


def dibujar_diagrama_hr(temperatura, luminosidad, color, nombre="Tu estrella"):
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
        edgecolors="white", linewidths=2, zorder=6, label=nombre,
    )

    # En un diagrama HR convencional las estrellas más calientes van a la izquierda.
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(32000, 2500)
    ax.set_ylim(0.0008, 200000)
    # Mostrar 20.000 (y demás cifras) en lugar de 2 × 10^4.
    ax.xaxis.set_major_locator(FixedLocator([30000, 20000, 15000, 10000, 6000, 4000, 3000]))
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda val, pos: formatear_numero(val, 0))
    )
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_major_locator(
        FixedLocator([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000])
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda val, pos: formatear_numero(val))
    )
    ax.yaxis.set_minor_formatter(NullFormatter())
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


# Ejemplos orientativos. Temperatura efectiva en K y luminosidad bolométrica
# en unidades solares. Los datos están aproximados y varían entre publicaciones.
# Referencias accesibles en los enlaces de cada ejemplo.
ESTRELLAS_FAMOSAS = {
    "Sol": {
        "temperatura": 5772,
        "luminosidad": 1.0,
        "descripcion": "Nuestra estrella, referencia de la luminosidad y del radio solares.",
        "fuente": "https://www.iau.org/static/resolutions/IAU2015_English.pdf",
    },
    "Próxima Centauri": {
        "temperatura": 2980,
        "luminosidad": 0.00151,
        "descripcion": "Enana roja muy cercana al sistema solar; fría y poco luminosa.",
        "fuente": "https://doi.org/10.1051/0004-6361/201730582",
    },
    "Sirio A": {
        "temperatura": 9845,
        "luminosidad": 24.7,
        "descripcion": "Estrella caliente y muy luminosa del sistema de Sirio.",
        "fuente": "https://doi.org/10.1071/AS10010",
    },
    "Vega": {
        "temperatura": 9600,
        "luminosidad": 40.0,
        "descripcion": "Estrella blanca de la constelación de Lira, más caliente que el Sol.",
        "fuente": "https://onlineobservatory.eu/wp-content/uploads/2020/12/StudentGuide_StarEvolution6.pdf",
    },
    "Arturo (Arcturus)": {
        "temperatura": 4300,
        "luminosidad": 170.0,
        "descripcion": "Gigante anaranjada: menos caliente que el Sol, pero mucho más luminosa.",
        "fuente": "https://onlineobservatory.eu/wp-content/uploads/2020/12/StudentGuide_StarEvolution6.pdf",
    },
    "Betelgeuse": {
        "temperatura": 3500,
        "luminosidad": 100000.0,
        "descripcion": "Supergigante roja con luminosidad variable y parámetros inciertos.",
        "fuente": "https://academic.oup.com/mnras/article/526/2/2765/7286655",
    },
}


def aplicar_ejemplo():
    """Actualiza los controles ANTES de que Streamlit reconstruya los widgets."""
    nombre = st.session_state.ejemplo_seleccionado
    datos = ESTRELLAS_FAMOSAS[nombre]

    # Los controles originales usan pasos de 100 K y 0,1 en log10(L/L☉).
    temperatura = 2500 + 100 * round((datos["temperatura"] - 2500) / 100)
    log_lum = round(math.log10(datos["luminosidad"]), 1)
    st.session_state.temperatura_k = int(max(2500, min(30000, temperatura)))
    st.session_state.log_luminosidad = float(max(-3.0, min(5.0, log_lum)))
    st.session_state.ejemplo_aplicado = nombre


def editar_manualmente():
    """Al mover un deslizador, vuelve al modo de estrella personalizada."""
    st.session_state.ejemplo_aplicado = None


def main():
    st.set_page_config(page_title="Forja Estelar", page_icon="⭐", layout="wide")
    st.title("⭐ Forja Estelar")
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
        st.subheader("⭐ Estrellas conocidas")
        st.selectbox(
            "Selecciona un ejemplo",
            options=list(ESTRELLAS_FAMOSAS),
            key="ejemplo_seleccionado",
        )
        st.button(
            "Aplicar ejemplo",
            on_click=aplicar_ejemplo,
            use_container_width=True,
        )
        if st.session_state.get("ejemplo_aplicado"):
            st.success(f"Ejemplo aplicado: {st.session_state.ejemplo_aplicado}")
        ejemplo = ESTRELLAS_FAMOSAS[st.session_state.ejemplo_seleccionado]
        st.caption(ejemplo["descripcion"])
        st.caption(
            "Valores astronómicos orientativos; los deslizadores aproximan "
            "la temperatura a 100 K y log₁₀(L/L☉) a 0,1."
        )

        st.divider()
        st.subheader("Ajustes manuales")
        st.slider(
            "Temperatura superficial (K)",
            min_value=2500, max_value=30000, step=100,
            key="temperatura_k",
            on_change=editar_manualmente,
            help="Temperatura efectiva de la superficie estelar.",
        )
        st.slider(
            "Logaritmo de luminosidad (L / L☉)",
            min_value=-3.0, max_value=5.0, step=0.1,
            key="log_luminosidad",
            on_change=editar_manualmente,
            help="0 = luminosidad solar; 1 = 10 veces; 2 = 100 veces; -1 = 0,1 veces.",
        )
        st.caption("La escala logarítmica permite comparar estrellas muy distintas.")

    temperatura = st.session_state.temperatura_k
    luminosidad = 10 ** st.session_state.log_luminosidad
    radio = radio_en_radios_solares(temperatura, luminosidad)
    color = color_aproximado(temperatura)

    m1, m2, m3 = st.columns(3)
    m1.metric("🌡️ Temperatura", f"{formatear_numero(temperatura, 0)} K")
    m2.metric("✨ Luminosidad", f"{formatear_luminosidad(luminosidad)} L☉")
    m3.metric("📏 Radio estimado", f"{formatear_numero(radio, 2)} R☉")

    columna_estrella, columna_diagrama = st.columns([1, 1.65], gap="large")
    nombre_estrella = st.session_state.get("ejemplo_aplicado") or "Tu estrella"
    with columna_estrella:
        st.subheader(nombre_estrella)
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
            f"Esta estrella emitiría unas **{formatear_luminosidad(luminosidad)} veces** la "
            f"luminosidad del Sol y tendría un radio aproximado de "
            f"**{formatear_numero(radio, 2)} radios solares** si se comporta como un cuerpo "
            "que cumple la ley de Stefan–Boltzmann."
        )

    with columna_diagrama:
        st.subheader("Diagrama Hertzsprung–Russell")
        figura = dibujar_diagrama_hr(temperatura, luminosidad, color, nombre_estrella)
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
        f"Con T☉ = {TEMPERATURA_SOL} K, T = {formatear_numero(temperatura, 0)} K y "
        f"L = {formatear_luminosidad(luminosidad)} L☉, resulta R ≈ {formatear_numero(radio, 2)} R☉."
    )

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



if __name__ == "__main__":
    main()
