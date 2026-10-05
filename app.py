from datetime import datetime
import base64
import os
import altair as alt
import pandas as pd
import streamlit as st

# Configuración de la página (Modo Oscuro estricto)
st.set_page_config(
    page_title='GREP - Guatuso', page_icon='📊', layout='centered'
)

# Estilos CSS robustos para eliminar barras flotantes y estilizar la app
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ocultar elementos de anclaje y barras de herramientas de Streamlit */
    h1 a, h2 a, h3 a, .stMarkdown a {
        display: none !important;
    }
    [data-testid="stImageToolbar"], .stImageToolbar, button[kind="header"], [data-testid="stImageContainer"] > div:first-child {
        display: none !important;
        visibility: hidden !important;
    }
    
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }

    .stButton>button {
        background-color: #0EA5E9;
        color: #0B0F19;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        width: 100%;
        padding: 0.6rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #38bdf8;
        color: #0B0F19;
    }

    div[data-baseweb="select"] > div, input[type="text"], .stDateInput input, .stNumberInput input {
        background-color: #1A2333 !important;
        color: #E2E8F0 !important;
        border-color: #2D3748 !important;
        border-radius: 8px !important;
    }

    h1, h2, h3, h4, p, label {
        color: #E2E8F0 !important;
    }
    
    .stCaption, small {
        color: #94A3B8 !important;
    }

    .metric-card {
        background-color: #1A2333;
        border: 1px solid #2D3748;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* Cabecera unificada usando HTML puro para evitar bloques fantasma */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background-color: #1A2333;
        border: 1px solid #2D3748;
        padding: 15px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .logo-box-html {
        background-color: #FFFFFF;
        padding: 8px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-width: 90px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

DB_FILE = 'registros_grep.csv'
LOGO_FILE = 'logo_grep.png'

# Verificación y conversión del logo a Base64 para inserción HTML limpia
logo_base64 = ''
logo_disponible = False
if os.path.exists(LOGO_FILE) and os.path.getsize(LOGO_FILE) > 0:
  logo_disponible = True
  try:
    with open(LOGO_FILE, 'rb') as f:
      logo_base64 = base64.b64encode(f.read()).decode('utf-8')
  except Exception:
    logo_disponible = False

ORDEN_DISTRITOS = ['San Rafael', 'Buena Vista', 'Cote', 'Katira']
ABREV_DISTRITOS = {
    'San Rafael': 'DS',
    'Buena Vista': 'DBV',
    'Cote': 'DC',
    'Katira': 'DK',
}
LISTA_EVENTOS = ['DENGUE', 'EDA', 'ETI', 'IRAS', 'MALARIA']

COLORES_DISTRITOS = {
    'San Rafael': '#0EA5E9',
    'Buena Vista': '#10B981',
    'Cote': '#F59E0B',
    'Katira': '#8B5CF6',
}


def cargar_datos():
  if os.path.exists(DB_FILE):
    try:
      df = pd.read_csv(DB_FILE)
      if 'Codigo_Interno' not in df.columns:
        df['Codigo_Interno'] = 'N/D'
      if 'Semana' not in df.columns:
        df['Semana'] = 1
      for col in [
          'Semana',
          'Magnitud',
          'Trascendencia',
          'Vulnerabilidad',
          'Indice_GREP',
      ]:
        if col in df.columns:
          df[col] = pd.to_numeric(df[col], errors='coerce')
      return df
    except Exception:
      return pd.DataFrame(columns=[
          'Fecha',
          'Semana',
          'Codigo_Interno',
          'Evento',
          'Distrito',
          'Magnitud',
          'Trascendencia',
          'Vulnerabilidad',
          'Indice_GREP',
          'Nivel_Alerta',
      ])
  else:
    return pd.DataFrame(columns=[
        'Fecha',
        'Semana',
        'Codigo_Interno',
        'Evento',
        'Distrito',
        'Magnitud',
        'Trascendencia',
        'Vulnerabilidad',
        'Indice_GREP',
        'Nivel_Alerta',
    ])


df_registros = cargar_datos()

# ---------------------------------------------------------
# CABECERA LIMPIA MEDIANTE HTML PURO
# ---------------------------------------------------------
if logo_disponible and logo_base64:
  html_cabecera = f"""
    <div class="header-container">
        <div class="logo-box-html">
            <img src="data:image/png;base64,{logo_base64}" width="85" style="display: block;">
        </div>
        <div>
            <h1 style="margin: 0; color: #E2E8F0; font-size: 30px; font-weight: 800; letter-spacing: -0.5px;">GREP Guatuso</h1>
            <p style="margin: 4px 0 0 0; font-size: 14px; color: #94A3B8; font-weight: 500;">Área Rectora de Salud — Inteligencia Epidemiológica</p>
        </div>
    </div>
    """
else:
  html_cabecera = """
    <div class="header-container">
        <div>
            <h1 style="margin: 0; color: #E2E8F0; font-size: 30px; font-weight: 800; letter-spacing: -0.5px;">GREP Guatuso</h1>
            <p style="margin: 4px 0 0 0; font-size: 14px; color: #94A3B8; font-weight: 500;">Área Rectora de Salud — Inteligencia Epidemiológica</p>
        </div>
    </div>
    """

st.markdown(html_cabecera, unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# ---------------------------------------------------------
# KPIS RÁPIDOS
# ---------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
total_eventos = len(df_registros)
promedio_grep = (
    df_registros['Indice_GREP'].astype(float).mean()
    if not df_registros.empty and 'Indice_GREP' in df_registros.columns
    else 0.0
)
alertas_criticas = (
    len(
        df_registros[
            df_registros['Nivel_Alerta'].str.contains(
                'ROJO|NARANJA', na=False, case=False
            )
        ]
    )
    if not df_registros.empty
    else 0
)

with col_kpi1:
  st.markdown(
      f"""
        <div class="metric-card">
            <small style="color: #94A3B8;">TOTAL REGISTROS</small>
            <h3 style="margin: 5px 0 0 0; color: #0EA5E9;">{total_eventos}</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col_kpi2:
  st.markdown(
      f"""
        <div class="metric-card">
            <small style="color: #94A3B8;">ÍNDICE GREP PROM.</small>
            <h3 style="margin: 5px 0 0 0; color: #10B981;">{promedio_grep:.2f}</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col_kpi3:
  st.markdown(
      f"""
        <div class="metric-card">
            <small style="color: #94A3B8;">ALERTAS ACTIVAS</small>
            <h3 style="margin: 5px 0 0 0; color: #EF4444;">{alertas_criticas}</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown('<br>', unsafe_allow_html=True)

# ---------------------------------------------------------
# NAVEGACIÓN SUPERIOR
# ---------------------------------------------------------
menu = st.radio(
    'Navegación',
    [
        '➕ Registrar Evento',
        '📋 Registros (VS)',
        '📊 Estadísticas',
        'ℹ️ Acerca de',
    ],
    horizontal=True,
    label_visibility='collapsed',
)

st.markdown('---')

# =========================================================
# 1. REGISTRAR EVENTO
# =========================================================
if menu == '➕ Registrar Evento':
  st.subheader('Registrar Nuevo Evento Epidemiológico')

  with st.form('form_grep_movil', clear_on_submit=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
      semana_epi = st.number_input(
          'SEMANA (SE)', min_value=1, max_value=53, value=40
      )
    with col_f2:
      fecha_registro = st.date_input('FECHA', value=datetime.today())

    col_e1, col_e2 = st.columns(2)
    with col_e1:
      evento = st.selectbox(
          'EVENTO', LISTA_EVENTOS, format_func=lambda x: str(x)
      )
    with col_e2:
      distrito = st.selectbox('DISTRITO', ORDEN_DISTRITOS)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
      magnitud = st.selectbox('Magnitud (35%)', [1, 2, 3, 4, 5], index=0)
    with col_m2:
      trascendencia = st.selectbox(
          'Trascendencia (35%)', [1, 2, 3, 4, 5], index=0
      )
    with col_m3:
      vulnerabilidad = st.selectbox(
          'Vulnerabilidad (30%)', [1, 2, 3, 4, 5], index=0
      )

    calc_previo = (magnitud * 0.35) + (trascendencia * 0.35) + (
        vulnerabilidad * 0.30
    )

    if calc_previo <= 2.0:
      nivel_visual = '🟢 VERDE - Bajo'
    elif calc_previo <= 3.2:
      nivel_visual = '🟡 AMARILLO - Moderado'
    elif calc_previo <= 4.0:
      nivel_visual = '🟠 NARANJA - Alto'
    else:
      nivel_visual = '🔴 ROJO - Crítico'

    col_r1, col_r2 = st.columns(2)
    with col_r1:
      st.text_input('Puntaje GREP', value=f'{calc_previo:.2f}', disabled=True)
    with col_r2:
      st.text_input('Nivel Alerta', value=nivel_visual, disabled=True)

    submitted = st.form_submit_button('Guardar Evento')

    if submitted:
      df_existentes = df_registros[
          (df_registros['Semana'] == semana_epi)
          & (df_registros['Distrito'] == distrito)
          & (df_registros['Evento'] == evento)
      ]
      correlativo = len(df_existentes) + 1
      abrev = ABREV_DISTRITOS.get(distrito, 'GEN')
      codigo_interno = f'CASO {evento} {correlativo:03d} SE{semana_epi}{abrev}'

      nuevo_reg = pd.DataFrame({
          'Fecha': [str(fecha_registro)],
          'Semana': [int(semana_epi)],
          'Codigo_Interno': [codigo_interno],
          'Evento': [evento],
          'Distrito': [distrito],
          'Magnitud': [magnitud],
          'Trascendencia': [trascendencia],
          'Vulnerabilidad': [vulnerabilidad],
          'Indice_GREP': [round(calc_previo, 2)],
          'Nivel_Alerta': [nivel_visual],
      })
      df_registros = pd.concat([df_registros, nuevo_reg], ignore_index=True)
      df_registros.to_csv(DB_FILE, index=False)
      st.success(
          f'¡Evento guardado con éxito! Código asignado: {codigo_interno}'
      )

# =========================================================
# 2. REGISTROS (VS)
# =========================================================
elif menu == '📋 Registros (VS)':
  st.subheader('📋 Registros (Ordenados por Territorio)')
  if df_registros.empty:
    st.info('No hay registros activos en este momento.')
  else:
    df_registros['Distrito'] = pd.Categorical(
        df_registros['Distrito'], categories=ORDEN_DISTRITOS, ordered=True
    )
    df_ordenado = df_registros.sort_values(
        by=['Distrito', 'Semana', 'Fecha']
    ).reset_index(drop=True)

    for idx, row in df_ordenado.iterrows():
      codigo_mostrar = (
          row['Codigo_Interno']
          if 'Codigo_Interno' in row and pd.notna(row['Codigo_Interno'])
          else 'CASO N/D'
      )
      semana_mostrar = (
          int(row['Semana'])
          if 'Semana' in row and pd.notna(row['Semana'])
          else 1
      )

      with st.expander(
          f"📌 [{codigo_mostrar}] - {row['Evento']} | Distrito:"
          f" {row['Distrito']} (SE{semana_mostrar}) | Índice:"
          f" {row['Indice_GREP']}"
      ):
        col_det1, col_det2 = st.columns(2)
        with col_det1:
          st.caption('CÓDIGO INTERNO')
          st.write(f'**{codigo_mostrar}**')
          st.caption('EVENTO CLÍNICO')
          st.write(f"**{row['Evento']}**")
          st.caption('DISTRITO')
          st.write(f"**{row['Distrito']}**")
        with col_det2:
          st.caption('MAG | TRAS | VULN')
          st.write(
              f"**{int(row['Magnitud'])} | {int(row['Trascendencia'])}"
              f" | {int(row['Vulnerabilidad'])}**"
          )
          st.caption('INDICE GREP')
          st.write(f"**{row['Indice_GREP']}**")
          st.caption('NIVEL')
          st.write(f"**{row['Nivel_Alerta']}**")

        real_idx = df_registros[
            (df_registros['Codigo_Interno'] == codigo_mostrar)
            & (df_registros['Fecha'] == row['Fecha'])
            & (df_registros['Distrito'] == row['Distrito'])
        ].index
        real_idx = real_idx[0] if len(real_idx) > 0 else idx

        if st.button('🗑 Borrar Registro', key=f'del_exp_{idx}'):
          df_registros = df_registros.drop(real_idx).reset_index(drop=True)
          df_registros.to_csv(DB_FILE, index=False)
          st.success('Registro eliminado con éxito.')
          st.rerun()

# =========================================================
# 3. ESTADÍSTICAS (GRÁFICOS EPIDEMIOLÓGICOS CON BUEN ESPACIADO)
# =========================================================
elif menu == '📊 Estadísticas':
  st.subheader('📊 Panel de Análisis Epidemiológico')
  if df_registros.empty:
    st.info('No hay datos suficientes para mostrar estadísticas.')
  else:
    evento_seleccionado = st.selectbox(
        'Seleccione el Evento Clínico a Visualizar',
        LISTA_EVENTOS,
        format_func=lambda x: str(x),
    )

    df_filtrado_evento = df_registros[
        df_registros['Evento'] == evento_seleccionado
    ]

    st.markdown(
        f'### 📈 Comportamiento y Distribución de: **{evento_seleccionado}**'
    )
    st.markdown('')

    if df_filtrado_evento.empty:
      st.warning(
          f'No hay registros ingresados para el evento {evento_seleccionado}.'
      )
    else:
      # GRÁFICO 1: Casos por Distrito (Ancho completo con excelente espacio)
      conteo_distritos = (
          df_filtrado_evento['Distrito']
          .value_counts()
          .reindex(ORDEN_DISTRITOS, fill_value=0)
      )
      df_chart_dist = conteo_distritos.reset_index()
      df_chart_dist.columns = ['Distrito', 'Casos']

      chart_barras = (
          alt.Chart(df_chart_dist)
          .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, width=50)
          .encode(
              x=alt.X(
                  'Distrito:N',
                  sort=ORDEN_DISTRITOS,
                  title='Distrito de Guatuso',
                  axis=alt.Axis(labelAngle=0),
              ),
              y=alt.Y(
                  'Casos:Q', title='Cantidad de Casos', axis=alt.Axis(format='d')
              ),
              color=alt.Color(
                  'Distrito:N',
                  scale=alt.Scale(
                      domain=list(COLORES_DISTRITOS.keys()),
                      range=list(COLORES_DISTRITOS.values()),
                  ),
                  legend=None,
              ),
              tooltip=[
                  'Distrito',
                  alt.Tooltip('Casos:Q', format='d', title='Casos'),
              ],
          )
          .properties(
              title='Casos Registrados por Distrito (Distribución Territorial)',
              height=280,
          )
          .configure_view(stroke=None)
          .configure(background='#0B0F19')
          .configure_axis(
              labelColor='#E2E8F0',
              titleColor='#E2E8F0',
              gridColor='#2D3748',
              domainColor='#2D3748',
          )
      )
      st.altair_chart(chart_barras, use_container_width=True)

      st.markdown('<br><hr><br>', unsafe_allow_html=True)

      # GRÁFICO 2: Líneas comparativas por Distrito según Semana Epidemiológica (SE)
      st.markdown(
          '### 📉 Comparativa de Eventos por Distrito según Semana'
          ' Epidemiológica (SE)'
      )
      st.markdown('')

      df_tendencia_dist = (
          df_filtrado_evento.groupby(['Semana', 'Distrito'])
          .size()
          .reset_index(name='Casos')
      )

      chart_lineas_distrito = (
          alt.Chart(df_tendencia_dist)
          .mark_line(point=True, strokeWidth=3)
          .encode(
              x=alt.X(
                  'Semana:Q',
                  title='Semana Epidemiológica (SE)',
                  axis=alt.Axis(format='d'),
              ),
              y=alt.Y(
                  'Casos:Q', title='Nº de Casos', axis=alt.Axis(format='d')
              ),
              color=alt.Color(
                  'Distrito:N',
                  scale=alt.Scale(
                      domain=list(COLORES_DISTRITOS.keys()),
                      range=list(COLORES_DISTRITOS.values()),
                  ),
                  legend=alt.Legend(title='Distrito'),
              ),
              tooltip=[
                  alt.Tooltip('Semana:Q', title='Semana'),
                  alt.Tooltip('Distrito:N', title='Distrito'),
                  alt.Tooltip('Casos:Q', title='Casos'),
              ],
          )
          .properties(
              title=(
                  f'Evolución de {evento_seleccionado} por Distrito y Semana'
                  ' Epidemiológica'
              ),
              height=320,
          )
          .configure_view(stroke=None)
          .configure(background='#0B0F19')
          .configure_axis(
              labelColor='#E2E8F0',
              titleColor='#E2E8F0',
              gridColor='#2D3748',
              domainColor='#2D3748',
          )
      )
      st.altair_chart(chart_lineas_distrito, use_container_width=True)

      st.markdown('<br><hr><br>', unsafe_allow_html=True)

      # GRÁFICO 3: Distribución por Nivel de Alerta (Con su propio espacio limpio)
      st.markdown('### 🎯 Análisis de Priorización y Alerta Sanitaria')
      st.markdown('')

      df_alerta = (
          df_filtrado_evento['Nivel_Alerta']
          .value_counts()
          .reset_index(name='Cantidad')
      )
      df_alerta.columns = ['Alerta', 'Cantidad']

      chart_alerta = (
          alt.Chart(df_alerta)
          .mark_arc(innerRadius=60, outerRadius=110)
          .encode(
              theta=alt.Theta('Cantidad:Q'),
              color=alt.Color(
                  'Alerta:N',
                  scale=alt.Scale(
                      domain=[
                          '🟢 VERDE - Bajo',
                          '🟡 AMARILLO - Moderado',
                          '🟠 NARANJA - Alto',
                          '🔴 ROJO - Crítico',
                      ],
                      range=['#10B981', '#F59E0B', '#F97316', '#EF4444'],
                  ),
                  legend=alt.Legend(title='Nivel de Alerta'),
              ),
              tooltip=['Alerta', 'Cantidad'],
          )
          .properties(
              title='Proporción de Casos según Nivel de Alerta GREP',
              height=300,
          )
          .configure_view(stroke=None)
          .configure(background='#0B0F19')
      )
      st.altair_chart(chart_alerta, use_container_width=True)

# =========================================================
# 4. ACERCA DE (CON GUÍA OPERATIVA Y AUTORÍA MÉDICA)
# =========================================================
elif menu == 'ℹ️ Acerca de':
  col_acerca1, col_acerca2 = st.columns([1, 3], vertical_alignment='center')
  with col_acerca1:
    if logo_disponible:
      st.image(LOGO_FILE, width=120)
    else:
      st.markdown('📊')
  with col_acerca2:
    st.subheader('ℹ️ Acerca de la Aplicación GREP')
    st.write(
        '**Gestión de Respuesta Epidemiológica Priorizada (GREP)**'
        '\nÁrea Rectora de Salud - Guatuso.'
    )

  st.markdown('---')
  st.markdown(
      'Esta aplicación permite a los equipos operativos y de salud gestionar,'
      ' clasificar y responder de manera ágil ante eventos epidemiológicos en'
      ' el cantón de Guatuso.'
  )

  st.markdown('### 📖 Guía de Usuario: Protocolo Operativo GREP')
  st.write(
      'Bienvenido al Protocolo Operativo GREP. Esta guía le ayudará a navegar'
      ' por la plataforma oficial de la Coordinación de Vigilancia de la Salud'
      ' para optimizar la respuesta sanitaria en el cantón de Guatuso.'
  )

  st.markdown('#### 1. Inicio de Sesión y Acceso')
  st.write(
      'Para garantizar la seguridad de los datos epidemiológicos, el acceso es'
      ' restringido:'
  )
  st.markdown(
      '- **Credenciales:** Ingrese con su correo institucional y contraseña'
      ' asignada por la Coordinación.'
  )
  st.markdown(
      '- **Permisos:** Su perfil (Administrador, Operativo o Consulta)'
      ' determinará las acciones que puede realizar.'
  )

  st.markdown('#### 2. Registro de Eventos Sanitarios')
  st.write(
      'El núcleo del sistema es la captura oportuna de información.'
  )
  st.markdown(
      '- **Nuevo Reporte:** Haga clic en el botón "+" o "Registrar Evento".'
  )
  st.markdown(
      '- **Datos del Evento:** Complete los campos obligatorios (Ubicación'
      ' exacta en Guatuso, tipo de sospecha, número de afectados).'
  )
  st.markdown(
      '- **Geolocalización:** El sistema permite marcar el punto exacto del'
      ' brote para una mejor respuesta territorial.'
  )

  st.markdown('#### 3. Clasificación y Priorización (Algoritmo GREP)')
  st.write(
      'Una vez ingresado el evento, el sistema le asignará una categoría de'
      ' prioridad:'
  )
  st.markdown(
      '- **Prioridad Alta:** Respuesta Inmediata requerida (Riesgo de'
      ' propagación masiva).'
  )
  st.markdown(
      '- **Prioridad Media:** Seguimiento en un plazo de 24-48 horas.'
  )
  st.markdown(
      '- **Prioridad Baja:** Vigilancia rutinaria y control preventivo.'
  )

  st.markdown('#### 4. Gestión de Respuesta')
  st.write('Dentro de cada evento, usted podrá:')
  st.markdown(
      '- **Actualizar Estado:** Cambiar de "Pendiente" a "En Proceso" o'
      ' "Cerrado".'
  )
  st.markdown(
      '- **Adjuntar Evidencia:** Subir fotos o documentos técnicos relevantes.'
  )
  st.markdown(
      '- **Asignar responsables:** Delegar tareas a equipos específicos de'
      ' campo.'
  )

  st.markdown('#### 5. Consultas y Reportes')
  st.write(
      'Para visualizar el panorama epidemiológico del cantón de Guatuso:'
  )
  st.markdown(
      '- **Panel de Control (Dashboard):** Visualice gráficos en tiempo real'
      ' con la incidencia de casos.'
  )
  st.markdown(
      '- **Exportación:** Puede descargar reportes en formato PDF o Excel para'
      ' reuniones técnicas de la Coordinación.'
  )

  st.markdown('### 💡 Consejos para un uso eficiente')
  st.markdown(
      '- **Sincronización:** Si utiliza la app en zonas con poca señal en'
      ' Guatuso, asegúrese de sincronizar los datos una vez recupere la'
      ' conexión a Internet.'
  )
  st.markdown(
      '- **Precisión:** La calidad de la respuesta depende de la exactitud de'
      ' la clasificación inicial. Revise bien los síntomas reportados antes de'
      ' guardar.'
  )

  st.markdown('---')
  st.markdown('### 🗺️ Territorios Oficiales:')
  st.markdown('1. **San Rafael (DS)**')
  st.markdown('2. **Buena Vista (DBV)**')
  st.markdown('3. **Cote (DC)**')
  st.markdown('4. **Katira (DK)**')

  # --- BLOQUE DE AUTORÍA MÉDICA OFICIAL ---
  st.markdown('---')
  st.markdown(
      """
        <div style="background-color: #1A2333; padding: 20px; border-radius: 12px; border: 1px solid #2D3748; text-align: center;">
            <p style="margin: 0; font-size: 13px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Dirección, Arquitectura y Autoría</p>
            <p style="margin: 8px 0 2px 0; font-size: 18px; font-weight: 800; color: #0EA5E9;">Dr Renzo Iñaki-Sánchez H</p>
            <p style="margin: 0; font-size: 14px; font-weight: 600; color: #10B981;">COD MED 12723</p>
            <p style="margin: 6px 0 0 0; font-size: 12px; color: #64748B;">Área Rectora de Salud de Guatuso — Ministerio de Salud</p>
        </div>
        """,
      unsafe_allow_html=True,
  )
  # ----------------------------------------

# =========================================================
# PIE DE PÁGINA FIJO / MARCA DE AUTORÍA PERMANENTE
# =========================================================
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; padding: 15px; color: #64748B; font-size: 12px; border-top: 1px solid #1A2333;">
        GREP Guatuso v2.0 | Desarrollado y Validado por <b>Dr Renzo Iñaki-Sánchez H COD MED 12723</b> — Área Rectora de Salud
    </div>
    """,
    unsafe_allow_html=True,
)