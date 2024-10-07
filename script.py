import json
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots


# Definimos los colores que usaremos para todas las gráficas.
PLOT_COLOR = "#0F0F0F"
PAPER_COLOR = "#232D3F"
HEADER_COLOR = "#5c6bc0"


ENTIDADES = {
    1: "Aguascalientes",
    2: "Baja California",
    3: "Baja California Sur",
    4: "Campeche",
    5: "Coahuila",
    6: "Colima",
    7: "Chiapas",
    8: "Chihuahua",
    9: "Ciudad de México",
    10: "Durango",
    11: "Guanajuato",
    12: "Guerrero",
    13: "Hidalgo",
    14: "Jalisco",
    15: "Estado de México",
    16: "Michoacán",
    17: "Morelos",
    18: "Nayarit",
    19: "Nuevo León",
    20: "Oaxaca",
    21: "Puebla",
    22: "Querétaro",
    23: "Quintana Roo",
    24: "San Luis Potosí",
    25: "Sinaloa",
    26: "Sonora",
    27: "Tabasco",
    28: "Tamaulipas",
    29: "Tlaxcala",
    30: "Veracruz",
    31: "Yucatán",
    32: "Zacatecas",
}


def tendencia():
    """
    Crea una gráfica de barras con la evolución de matrimonios entre parejas del mismo sexo.
    """

    # Cargamos la población adulta de hombres.
    pop_hombres = pd.read_csv(
        "./assets/poblacion_adulta/hombres.csv",
        index_col=0,
    )

    # Seleccionamos la primera fila (nacional).
    pop_hombres = pop_hombres.iloc[0]
    pop_hombres.index = pop_hombres.index.astype(int)

    # Cargamos la población adulta de mujeres.
    pop_mujers = pd.read_csv(
        "./assets/poblacion_adulta/mujeres.csv",
        index_col=0,
    )

    # Seleccionamos la primera fila (nacional).
    pop_mujers = pop_mujers.iloc[0]
    pop_mujers.index = pop_mujers.index.astype(int)

    # Cargamos el dataset de nupcialidad.
    df = pd.read_csv("./data.csv")

    # Seleccionamos matrimonios entre parejas del mismo sexo.
    df = df[df["SEXO_CON1"] == df["SEXO_CON2"]]

    # Creamos un DataFrame con los registros de hombres.
    hombres = (
        df[df["SEXO_CON1"] == 1]["ANIO_REGIS"]
        .value_counts()
        .sort_index()
        .to_frame("total")
    )

    # Creamos un DataFrame con los registros de mujeres.
    mujeres = (
        df[df["SEXO_CON1"] == 2]["ANIO_REGIS"]
        .value_counts()
        .sort_index()
        .to_frame("total")
    )

    # Agregamos la población al DataFrame de hombres y calculamos la tasa por cada 100,000.
    hombres["poblacion"] = pop_hombres
    hombres["tasa"] = hombres["total"] / hombres["poblacion"] * 100000

    # Le damos formato a los textos que irán arriba de cada barra.
    hombres["texto"] = hombres.apply(
        lambda x: f"{x['tasa']:,.2f}<br>({x['total']:,.0f})", axis=1
    )

    # Agregamos la población al DataFrame de mujeres y calculamos la tasa por cada 100,000.
    mujeres["poblacion"] = pop_mujers
    mujeres["tasa"] = mujeres["total"] / mujeres["poblacion"] * 100000

    # Le damos formato a los textos que irán arriba de cada barra.
    mujeres["texto"] = mujeres.apply(
        lambda x: f"{x['tasa']:,.2f}<br>({x['total']:,.0f})", axis=1
    )

    # Preparamos los textos para la anotación.
    hombres_total = (
        f"Total de matrimonios entre hombres: <b>{hombres['total'].sum():,.0f}</b>"
    )
    mujeres_total = (
        f"Total de matrimonios entre mujeres: <b>{mujeres['total'].sum():,.0f}</b>"
    )
    gran_total = f"Total de matrimonios igualitarios: <b>{len(df):,.0f}</b>"

    nota = f"<b>Notas:</b><br>Las tasas se calcularon con la población estimada de<br>hombres y mujeres mayores de edad para cada año.<br><br>{hombres_total}<br>{mujeres_total}<br>{gran_total}"

    # Vamos a crear dos gráficas de barras paralelas, una para hombres
    # y la otra para mujeres.
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=hombres.index,
            y=hombres["tasa"],
            text=hombres["texto"],
            textposition="outside",
            textfont_family="Oswald",
            name="Hombre-Hombre",
            marker_color="#009688",
            marker_opacity=1.0,
            marker_line_width=0,
            textfont_size=13,
        )
    )

    fig.add_trace(
        go.Bar(
            x=mujeres.index,
            y=mujeres["tasa"],
            text=mujeres["texto"],
            textposition="outside",
            textfont_family="Oswald",
            name="Mujer-Mujer",
            marker_color="#ffa726",
            marker_opacity=1.0,
            marker_line_width=0,
            textfont_size=13,
        )
    )

    fig.update_xaxes(
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        range=[0, 9],
        title="Tasa por cada 100,000 hombres/mujeres mayores de edad",
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        legend_title="Tipo de contrayentes",
        legend_title_side="top center",
        legend_itemsizing="constant",
        legend_orientation="h",
        legend_bordercolor="#FFFFFF",
        legend_borderwidth=1,
        showlegend=True,
        legend_x=0.5,
        legend_y=0.98,
        legend_xanchor="center",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Evolución de las tasas de matrimonio igualitario en México según tipo de contrayentes",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.02,
                y=0.7,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                align="left",
                text=nota,
                bgcolor="#0F0F0F",
                borderpad=7,
                bordercolor="#FFFFFF",
                borderwidth=1.5,
                font_size=16,
            ),
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: INEGI (EMAT, 2010-2023)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año de registro del matrimonio",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./tendencia.png")


def tendencia_mismo_sexo():
    """
    Crea una gráfica de linea mostrando la evolución de la tasa
    de matrimonios entre parejas del mismo sexo.
    """

    # Cargamos la población adulta total.
    pop = pd.read_csv(
        "./assets/poblacion_adulta/total.csv",
        index_col=0,
    )

    # Seleccionamos la primera fila (nacional).
    pop = pop.iloc[0]
    pop.index = pop.index.astype(int)

    # Cargamos el dataset de nupcilaidad.
    df = pd.read_csv("./data.csv")

    # Filtramos por matrimonios del mismo sexo y calculmos
    # los registros por año.
    df = (
        df[df["SEXO_CON1"] == df["SEXO_CON2"]]["ANIO_REGIS"]
        .value_counts()
        .sort_index()
        .to_frame("total")
    )

    # Agregamos la población y calculamos la tasa por cada 100,000 habitantes.
    df["pop"] = pop
    df["tasa"] = df["total"] / df["pop"] * 100000

    # Calculamos el cambio porcentual.
    df["change"] = df["total"].pct_change() * 100
    df["change2"] = df["change"].apply(convert_change)

    # Le damos format al texto que irá arriba de cada punto.
    df["texto"] = df.apply(
        lambda x: f"<b><span style='color:#c6ff00'>{x['tasa']:,.2f}</span></b><br>({x['total']/1000:,.1f}k)"
        if x["total"] > 1000
        else f"<b><span style='color:#c6ff00'>{x['tasa']:,.2f}</span></b><br>({x['total']:,.0f})",
        axis=1,
    )

    # Calculamos el total de registros y el cambio porcentual desde el comienzo.
    total = df["total"].sum()
    cambio = (df["tasa"].iloc[-1] - df["tasa"].iloc[0]) / df["tasa"].iloc[0] * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["tasa"],
            text=df["texto"],
            textposition="top center",
            mode="markers+lines+text",
            name=f"Total acumulado: <b>{total:,.0f}</b><br>Crecimiento de la tasa: <b>{cambio:,.0f}%</b>",
            line_color="#c6ff00",
            marker_opacity=1.0,
            line_width=7,
            line_shape="spline",
            line_smoothing=1.0,
            marker_size=30,
            textfont_size=20,
        )
    )

    fig.update_xaxes(
        range=[df.index.min() - 0.4, df.index.max() + 0.4],
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        title="Tasa por cada 100,000 habitantes mayores de edad",
        range=[None, df["tasa"].max() * 1.17],
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        legend_itemsizing="constant",
        legend_borderwidth=1,
        legend_bordercolor="#FFFFFF",
        showlegend=True,
        legend_x=0.01,
        legend_y=0.98,
        legend_xanchor="left",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Evolución de la tasa de matrimonio entre parejas del <b>mismo sexo</b> en México (2010-2023)",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: INEGI (EMAT, 2010-2023)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año de registro del matrimonio",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./tendencia_mismo_sexo.png")


def tendencia_sexo_opuesto():
    """
    Crea una gráfica de linea mostrando la evolución de la tasa
    de matrimonios entre parejas del sexo opuesto.
    """

    # Cargamos la población adulta total.
    pop = pd.read_csv(
        "./assets/poblacion_adulta/total.csv",
        index_col=0,
    )

    # Seleccionamos la primera fila (nacional).
    pop = pop.iloc[0]
    pop.index = pop.index.astype(int)

    # Cargamos el dataset de nupcilaidad.
    df = pd.read_csv("./data.csv")

    # Filtramos por matrimonios del sexo opuesto y calculmos
    # los registros por año.
    df = (
        df[df["SEXO_CON1"] != df["SEXO_CON2"]]["ANIO_REGIS"]
        .value_counts()
        .sort_index()
        .to_frame("total")
    )

    # Agregamos la población y calculamos la tasa por cada 100,000 habitantes.
    df["pop"] = pop
    df["tasa"] = df["total"] / df["pop"] * 100000

    # Calculamos el cambio porcentual.
    df["change"] = df["total"].pct_change() * 100
    df["change2"] = df["change"].apply(convert_change)

    # Le damos format al texto que irá arriba de cada punto.
    df["texto"] = df.apply(
        lambda x: f"<b><span style='color:#69caff'>{x['tasa']:,.0f}</span></b><br>({x['total']/1000:,.0f}k)",
        axis=1,
    )

    # Calculamos el total de registros y el cambio porcentual desde el comienzo.
    total = df["total"].sum()
    cambio = (df["tasa"].iloc[-1] - df["tasa"].iloc[0]) / df["tasa"].iloc[0] * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["tasa"],
            text=df["texto"],
            textposition="top center",
            mode="markers+lines+text",
            name=f"Total acumulado: <b>{total:,.0f}</b><br>Crecimiento de la tasa: <b>{cambio:,.0f}%</b>",
            line_color="#69caff",
            marker_opacity=1.0,
            line_width=7,
            line_shape="spline",
            line_smoothing=1.0,
            marker_size=30,
            textfont_size=20,
        )
    )

    fig.update_xaxes(
        range=[df.index.min() - 0.5, df.index.max() + 0.5],
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        title="Tasa por cada 100,000 habitantes mayores de edad",
        range=[None, df["tasa"].max() * 1.12],
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        legend_itemsizing="constant",
        legend_borderwidth=1,
        legend_bordercolor="#FFFFFF",
        showlegend=True,
        legend_x=0.99,
        legend_y=0.98,
        legend_xanchor="right",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Evolución de la tasa de matrimonio entre parejas del <b>sexo opuesto</b> en México (2010-2023)",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: INEGI (EMAT, 2010-2023)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año de registro del matrimonio",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./tendencia_sexo_opuesto.png")


def convert_change(change):
    """
    Le da formato al cambio porcentual.
    """

    if change >= 0:
        return f"+{change:,.2f}%"
    elif change < 0:
        return f"{change:,.2f}%"

    return "---"


def edades_hombres():
    """
    Crea gráficas de linea con la evolución de la edad promedio
    de hombres al momento de casarse.
    """

    # Cargamos el dataset de nupcialidad.
    df = pd.read_csv("./data.csv")

    # Quitamos registros inválidos.
    df = df[df["EDAD_CON1"] != 99]
    df = df[df["EDAD_CON2"] != 99]

    # Creamos dos DataFrame para cada tipo de matrimonio.
    opuesto = df[(df["SEXO_CON1"] == 1) & (df["SEXO_CON2"] == 2)]
    igualitario = df[(df["SEXO_CON1"] == 1) & (df["SEXO_CON2"] == 1)]

    # Calcularemos datos para cada año y los guardaremos aquí.
    data = list()

    # Iteramos para cada año.
    for año in df["ANIO_REGIS"].unique():
        temp_opuesto = opuesto[opuesto["ANIO_REGIS"] == año]

        # Calculamos la edad promedio de hombres en matrimonios del sexo opuesto.
        edad_opuesto = temp_opuesto["EDAD_CON1"].mean()

        temp_igualitario = igualitario[igualitario["ANIO_REGIS"] == año]

        # Para calcular la edad promedio en matrimonios del mismo sexo debemos
        # tomar las edades de ambos contrayentes.
        edad_igualitario = np.concatenate(
            [temp_igualitario["EDAD_CON1"], temp_igualitario["EDAD_CON2"]]
        ).mean()

        # Agregamos los valores calculados a nuestra lista de datos.
        data.append(
            {
                "año": año,
                "edad_opuesto": edad_opuesto,
                "edad_igualitario": edad_igualitario,
            }
        )

    # COnvertimos la lista a un DataFrame.
    df = pd.DataFrame.from_records(data, index="año")

    # Vamos a crear dos gráficas de líneas pero solo mostrando los puntos.
    # Así mismo, agregaremos los textos por nuestra cuenta para poder ajustar
    # # mejor su posición vertical.
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_opuesto"],
            mode="markers",
            name="Matrimonio con pareja del sexo opuesto",
            marker_color="#33691e",
            marker_symbol="circle",
            marker_size=50,
            marker_line_width=3,
            marker_line_color="#FFFFFF",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_opuesto"] * 0.996,
            text=df["edad_opuesto"],
            texttemplate="%{text:,.1f}",
            mode="text",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=22,
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_igualitario"],
            mode="markers",
            name="Matrimonio con pareja del mismo sexo",
            marker_color="#1565c0",
            marker_symbol="diamond",
            marker_size=50,
            marker_line_width=3,
            marker_line_color="#FFFFFF",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_igualitario"] * 0.996,
            text=df["edad_igualitario"],
            texttemplate="%{text:,.1f}",
            mode="text",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=22,
            showlegend=False,
        )
    )

    fig.update_xaxes(
        range=[df.index.min() - 0.6, df.index.max() + 0.6],
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        title="Edad promedio al momento de contraer matrimonio",
        range=[df["edad_opuesto"].min() - 5, df["edad_igualitario"].max() + 5],
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        legend_itemsizing="constant",
        legend_borderwidth=1,
        legend_bordercolor="#FFFFFF",
        showlegend=True,
        legend_x=0.5,
        legend_y=0.98,
        legend_xanchor="center",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Evolución de la edad promedio de <b>hombres</b> al momento de contraer matrimonio en México",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: INEGI (EMAT, 2010-2023)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año de registro del matrimonio",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./edades_hombres.png")


def edades_mujeres():
    """
    Crea gráficas de linea con la evolución de la edad promedio
    de mujeres al momento de casarse.
    """

    # Cargamos el dataset de nupcialidad.
    df = pd.read_csv("./data.csv")

    # Quitamos registros inválidos.
    df = df[df["EDAD_CON1"] != 99]
    df = df[df["EDAD_CON2"] != 99]

    # Creamos dos DataFrame para cada tipo de matrimonio.
    opuesto = df[(df["SEXO_CON1"] == 1) & (df["SEXO_CON2"] == 2)]
    igualitario = df[(df["SEXO_CON1"] == 2) & (df["SEXO_CON2"] == 2)]

    # Calcularemos datos para cada año y los guardaremos aquí.
    data = list()

    # Iteramos para cada año.
    for año in df["ANIO_REGIS"].unique():
        temp_opuesto = opuesto[opuesto["ANIO_REGIS"] == año]

        # Calculamos la edad promedio de mujeres en matrimonios del sexo opuesto.
        edad_opuesto = temp_opuesto["EDAD_CON2"].mean()

        temp_igualitario = igualitario[igualitario["ANIO_REGIS"] == año]

        # Para calcular la edad promedio en matrimonios del mismo sexo debemos
        # tomar las edades de ambos contrayentes.
        edad_igualitario = np.concatenate(
            [temp_igualitario["EDAD_CON1"], temp_igualitario["EDAD_CON2"]]
        ).mean()

        # Agregamos los valores calculados a nuestra lista de datos.
        data.append(
            {
                "año": año,
                "edad_opuesto": edad_opuesto,
                "edad_igualitario": edad_igualitario,
            }
        )

    # COnvertimos la lista a un DataFrame.
    df = pd.DataFrame.from_records(data, index="año")

    # Vamos a crear dos gráficas de líneas pero solo mostrando los puntos.
    # Así mismo, agregaremos los textos por nuestra cuenta para poder ajustar
    # # mejor su posición vertical.
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_opuesto"],
            mode="markers",
            name="Matrimonio con pareja del sexo opuesto",
            marker_color="#f50057",
            marker_symbol="circle",
            marker_size=50,
            marker_line_width=3,
            marker_line_color="#FFFFFF",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_opuesto"] * 0.996,
            text=df["edad_opuesto"],
            texttemplate="%{text:,.1f}",
            mode="text",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=22,
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_igualitario"],
            mode="markers",
            name="Matrimonio con pareja del mismo sexo",
            marker_color="#7b1fa2",
            marker_symbol="diamond",
            marker_size=50,
            marker_line_width=3,
            marker_line_color="#FFFFFF",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["edad_igualitario"] * 0.996,
            text=df["edad_igualitario"],
            texttemplate="%{text:,.1f}",
            mode="text",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=22,
            showlegend=False,
        )
    )

    fig.update_xaxes(
        range=[df.index.min() - 0.6, df.index.max() + 0.6],
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        title="Edad promedio al momento de contraer matrimonio",
        range=[df["edad_opuesto"].min() - 5, df["edad_igualitario"].max() + 5],
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        legend_itemsizing="constant",
        legend_borderwidth=1,
        legend_bordercolor="#FFFFFF",
        showlegend=True,
        legend_x=0.5,
        legend_y=0.98,
        legend_xanchor="center",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Evolución de la edad promedio de <b>mujeres</b> al momento de contraer matrimonio en México",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        plot_bgcolor=PLOT_COLOR,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: INEGI (EMAT, 2010-2023)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año de registro del matrimonio",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./edades_mujeres.png")


def mapa_entidades(año):
    """
    Crea un mapa con los registros de matrimonios igualitarios por entidad.

    Parameters
    ----------
    año : int
        El año que se desea graficar.

    """

    # Cargamos la población adulta total.
    pop = pd.read_csv(
        "./assets/poblacion_adulta/total.csv",
        index_col=0,
    )

    # Seleccionamos la población del año de nuestro interés.
    pop = pop[str(año)]

    # Ajustamos el nombre del Estado de México.
    pop.index = pop.index.map(lambda x: x if x != "México" else "Estado de México")

    # Cargamos el dataset de nupcialidad.
    df = pd.read_csv("./data.csv")

    # Filtramos por el año de nuestro interés.
    df = df[df["ANIO_REGIS"] == año]

    # Creamos un DataFrame con los registros de hombres.
    hombres = (
        df[(df["SEXO_CON1"] == 1) & (df["SEXO_CON2"] == 1)]["ENT_REGIS"]
        .value_counts()
        .to_frame("hombres")
    )

    # Creamos un DataFrame con los registros de mujeres.
    mujeres = (
        df[(df["SEXO_CON1"] == 2) & (df["SEXO_CON2"] == 2)]["ENT_REGIS"]
        .value_counts()
        .to_frame("mujeres")
    )

    # Hay estados sin registros, lo cual puede causar ambigüedad.
    # Creamos un DataFrame con valores en cero para arreglar esto.
    dummy = pd.DataFrame(index=list(ENTIDADES.keys()), columns=["total"], data=0)

    # Unimos ambos DataFrames.
    df = pd.concat([hombres, mujeres, dummy], axis=1).fillna(0)

    # Asignamos el nombre de la entidad.
    df.index = df.index.map(ENTIDADES)

    # Calculamos el total por entidad.
    df["total"] = df.sum(axis=1)

    # Agregamos la población y calculamos la tasa por cada 100,000 habitantes.
    df["poblacion"] = pop
    df["tasa"] = df["total"] / df["poblacion"] * 100000

    # ORdenamos por tasa, de mayor a menor.
    df = df.sort_values("tasa", ascending=False)

    # Preparamos nuestro subtítulo calculando los valores a nivel naciconal.
    total_nacional = df["total"].sum()
    tasa_nacional = total_nacional / pop.iloc[0] * 100000

    subtitulo = f"Tasa nacional: <b>{tasa_nacional:,.1f}</b> (con <b>{total_nacional:,.0f}</b> registros)"

    # Determinamos los valores mínimos y máximos para nuestra escala.
    # Para el valor máximo usamos el 97.5 percentil para mitigar los
    # efectos de valores atípicos.
    valor_min = df[df["tasa"] != 0]["tasa"].min()

    # En un caso muy aislado el valor mínimo es igual al máximo.
    if valor_min == df["tasa"].max():
        valor_min = 0

    valor_max = df["tasa"].quantile(0.975)

    # Vamos a crear nuestra escala con 11 intervalos.
    marcas = np.linspace(valor_min, valor_max, 11)
    etiquetas = list()

    for marca in marcas:
        etiquetas.append(f"{marca:,.1f}")

    # A la última etiqueta le agregamos el símbolo de 'mayor o igual que'.
    etiquetas[-1] = f"≥{etiquetas[-1]}"

    # Cargamos el GeoJSON de México.
    geojson = json.load(open("./assets/mexico.json", "r", encoding="utf-8"))

    # Estas listas serán usadas para configurar el mapa Choropleth.    ubicaciones = list()
    valores = list()
    ubicaciones = list()

    # Iteramos sobre las entidades dentro del GeoJSON.
    for item in geojson["features"]:
        # Extraemos el nombre de la entidad.
        geo = item["properties"]["NOMGEO"]

        # Agregamos el objeto de la entidad y su valor a las listas correspondientes.
        ubicaciones.append(geo)
        valores.append(df.loc[geo, "tasa"])

    fig = go.Figure()

    fig.add_traces(
        go.Choropleth(
            geojson=geojson,
            locations=ubicaciones,
            z=valores,
            featureidkey="properties.NOMGEO",
            colorscale="deep_r",
            colorbar=dict(
                x=0.03,
                y=0.5,
                ypad=50,
                ticks="outside",
                outlinewidth=2,
                outlinecolor="#FFFFFF",
                tickvals=marcas,
                ticktext=etiquetas,
                tickwidth=3,
                tickcolor="#FFFFFF",
                ticklen=10,
                tickfont_size=20,
            ),
            marker_line_color="#FFFFFF",
            marker_line_width=1.0,
            zmin=valor_min,
            zmax=valor_max,
        )
    )

    fig.update_geos(
        fitbounds="geojson",
        showocean=True,
        oceancolor=PLOT_COLOR,
        showcountries=False,
        framecolor="#FFFFFF",
        framewidth=2,
        showlakes=False,
        coastlinewidth=0,
        landcolor="#1C0A00",
    )

    fig.update_layout(
        showlegend=False,
        font_family="Lato",
        font_color="#FFFFFF",
        margin_t=50,
        margin_r=40,
        margin_b=30,
        margin_l=40,
        width=1280,
        height=720,
        paper_bgcolor=PAPER_COLOR,
        annotations=[
            dict(
                x=0.5,
                y=1.0,
                xanchor="center",
                yanchor="top",
                text=f"Tasas de matrimonio igualitario en México durante el {año} por entidad de registro",
                font_size=28,
            ),
            dict(
                x=0.0275,
                y=0.45,
                textangle=-90,
                xanchor="center",
                yanchor="middle",
                text="Tasa por cada 100,000 habitantes mayores de edad",
                font_size=16,
            ),
            dict(
                x=0.58,
                y=-0.04,
                xanchor="center",
                yanchor="top",
                text=subtitulo,
                font_size=22,
            ),
            dict(
                x=0.01,
                y=-0.04,
                xanchor="left",
                yanchor="top",
                text=f"Fuente: INEGI (EMAT, {año})",
                font_size=22,
            ),
            dict(
                x=1.01,
                y=-0.04,
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
                font_size=22,
            ),
        ],
    )

    fig.write_image("./1.png")

    # Vamos a crear dos tablas, cada una con la información de 16 entidades.
    fig = make_subplots(
        rows=1,
        cols=2,
        horizontal_spacing=0.03,
        specs=[[{"type": "table"}, {"type": "table"}]],
    )

    fig.add_trace(
        go.Table(
            columnwidth=[160, 90],
            header=dict(
                values=[
                    "<b>Entidad</b>",
                    "<b>♂-♂</b>",
                    "<b>♀-♀</b>",
                    "<b>Total</b>",
                    "<b>Tasa ↓</b>",
                ],
                font_color="#FFFFFF",
                fill_color=HEADER_COLOR,
                align="center",
                height=29,
                line_width=0.8,
            ),
            cells=dict(
                values=[
                    df.index[:16],
                    df["hombres"][:16],
                    df["mujeres"][:16],
                    df["total"][:16],
                    df["tasa"][:16],
                ],
                fill_color=PLOT_COLOR,
                height=29,
                format=["", ",.0f", ",.0f", ",.0f", ",.2f"],
                line_width=0.8,
                align=["left", "center"],
            ),
        ),
        col=1,
        row=1,
    )

    fig.add_trace(
        go.Table(
            columnwidth=[160, 90],
            header=dict(
                values=[
                    "<b>Entidad</b>",
                    "<b>♂-♂</b>",
                    "<b>♀-♀</b>",
                    "<b>Total</b>",
                    "<b>Tasa ↓</b>",
                ],
                font_color="#FFFFFF",
                fill_color=HEADER_COLOR,
                align="center",
                height=29,
                line_width=0.8,
            ),
            cells=dict(
                values=[
                    df.index[16:],
                    df["hombres"][16:],
                    df["mujeres"][16:],
                    df["total"][16:],
                    df["tasa"][16:],
                ],
                fill_color=PLOT_COLOR,
                height=29,
                format=["", ",.0f", ",.0f", ",.0f", ",.2f"],
                line_width=0.8,
                align=["left", "center"],
            ),
        ),
        col=2,
        row=1,
    )

    fig.update_layout(
        showlegend=False,
        legend_borderwidth=1.5,
        xaxis_rangeslider_visible=False,
        width=1280,
        height=560,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title="",
        title_x=0.5,
        title_y=0.95,
        margin_t=20,
        margin_l=40,
        margin_r=40,
        margin_b=0,
        title_font_size=26,
        paper_bgcolor=PAPER_COLOR,
    )

    fig.write_image("./2.png")

    # Unimos el mapa y las tablas en una sola imagen.
    image1 = Image.open("./1.png")
    image2 = Image.open("./2.png")

    result_width = 1280
    result_height = image1.height + image2.height

    result = Image.new("RGB", (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, image1.height))

    result.save(f"./mapa_{año}.png")

    # Borramos las imágenes originales.
    os.remove("./1.png")
    os.remove("./2.png")


def residencia(año):
    """
    Compara la entidad de residencia contra la entidad de registro.

    Parameters
    ----------
    año : int
        El año que nos interesa analizar.

    """

    # Cargamos el dataset de nupcialidad.
    df = pd.read_csv("./data.csv")

    # Filtramos por el año de nuestro interés.
    df = df[df["ANIO_REGIS"] == año]

    # Seleccionamos solo matrimonios del mismo sexo.
    df = df[df["SEXO_CON1"] == df["SEXO_CON2"]]

    # Limitamos por entidad de registro.
    df = df[df["ENT_REGIS"] == 9]

    # Nuestro índice sera la entidad de registro.
    df.set_index("ENT_REGIS", inplace=True)

    # Apilamos los datos de residencia de ambos contrayentes.
    df = pd.concat([df["ENTRH_CON1"], df["ENTRH_CON2"]], axis=0)

    # Calculamos la frecuencia de registros y sus porcentajes.
    df = df.value_counts().to_frame("total")
    df["perc"] = df["total"] / df["total"].sum() * 100
    df.index = df.index.map(ENTIDADES)

    print(df)
    print(df["total"].sum())


if __name__ == "__main__":
    tendencia()
    tendencia_mismo_sexo()
    tendencia_sexo_opuesto()

    edades_hombres()
    edades_mujeres()

    mapa_entidades(2010)
    mapa_entidades(2017)
    mapa_entidades(2023)

    residencia(2017)
