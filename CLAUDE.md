# Hotel Neptuno — Revenue Management App

> Documento vivo. Se actualiza en cada decisión o cambio de alcance.
> Última actualización: 2026-10-15.

## Objetivo

App local (no nube) que centraliza los Excel semanales de pickup/ADR del
Hotel Neptuno (Costa Adeje, Tenerife), los acumula en un histórico y genera
dashboards para el seguimiento de ocupación, ADR, RevPAR, pickup por ventana
y comparativas con el año anterior.

## Alcance actual (v0)

- Ingesta de **un Excel semanal** (los lunes) llamado `Planning de PickUpADR`.
- El Excel trae **un snapshot** con 184 días de estancia (≈ 6 meses) y 149 columnas
  con todos los KPIs del hotel ya calculados por el PMS.
- Archivado automático en `Excel-Lunes/<mes>/<semana>/`.
- Acumulación de snapshots en un Excel histórico maestro (`data/historico/`).
- Dashboards con los 4 gráficos de referencia (ver [docs/formato-excel.md](docs/formato-excel.md)).

## Fuera de alcance

- Integración directa con PMS / channel manager.
- Multi-usuario / multi-hotel.
- Despliegue en nube.
- Pricing dinámico / forecasting automático.

## Datos de entrada

Ver [docs/formato-excel.md](docs/formato-excel.md) para el esquema completo.
Resumen:

- **Fuente:** Excel exportado del PMS del hotel.
- **Frecuencia:** semanal (lunes).
- **Contenido:** un snapshot con una fila por día de estancia (6 meses hacia adelante)
  y 149 columnas con: ocupación, pickup a 1/7/14/28 días, ADR, RevPAR y producción
  por segmento (Alojamiento, Pensión, F&B, Otros, Total), más comparativa año anterior.
- **Formato fechas:** serial date de Excel.

## Histórico

- **Formato:** Excel maestro acumulado en `data/historico/historico_finca.xlsx`
  (en la nube, dentro del repo privado `revenue-finca-datos`).
- **Granularidad mínima:** una fila por (fecha_snapshot, fecha_estancia).
- **Justificación:** el usuario trabaja cómodo con Excel y quiere inspeccionar el
  histórico directamente con su herramienta habitual. Se descartó SQLite por esto.

## Stack técnico (propuesta)

| Capa | Elección | Por qué |
|---|---|---|
| Lenguaje | Python 3.11+ | Estándar para trabajar con Excel y análisis de datos, mucha documentación. |
| Lectura/escritura Excel | pandas + openpyxl | Combinación probada para `.xlsx`. |
| UI / dashboards | Streamlit | Se escribe como un script Python y corre local en el navegador. |
| Gráficos | Plotly | Interactivos, integración nativa con Streamlit. |
| Entorno | venv | Aislar dependencias del Python del sistema. |
| Hosting | Streamlit Community Cloud | Gratis, publica desde GitHub. |
| Almacén | Repo privado de GitHub | Gratis, persistente y versionado. |

(PyYAML se descartó el 2026-10-15 al borrar `config/settings.yaml`, que nadie leía.)

## Estructura de carpetas

```
revenue-finca/
├── CLAUDE.md              ← este archivo
├── AGENTS.md              Puntero a CLAUDE.md
├── README.md              Puesta en marcha y uso semanal
├── app.py                 Dashboard: lee del almacén, sube Excel, descarga histórico
├── requirements.txt       Versiones FIJADAS (la nube instala exactamente estas)
├── .gitignore             Ignora *.xlsx en cualquier carpeta + secrets
├── Finca.bat              Doble clic en Windows (respaldo local)
├── .streamlit/
│   ├── config.toml        Tema y límite de subida
│   └── secrets.toml       Token de GitHub. IGNORADO POR GIT. Plantilla: .ejemplo
├── Excel-Lunes/           Excel semanales archivados por mes/semana
│   └── BUZON/             Drop zone del respaldo local
├── data/historico/
│   └── historico_finca.xlsx         (local; en la nube vive en el repo de datos)
├── src/
│   ├── inventario.py      Fuente única del 17 y de R+L+Bloqueadas
│   ├── ingest/            excel_reader.py (validación) + pipeline.py (ingesta)
│   ├── storage/           almacen.py (local/GitHub) + historico.py (fusión)
│   ├── analysis/          series.py — KPIs y DataFrames. Sin I/O.
│   └── ui/                graficos.py + tema.py. Sin I/O.
├── scripts/               procesar_buzon.py, cargar_semana.py, lanzadores
└── docs/
    └── formato-excel.md
```

## Flujo de trabajo

**Vía normal (desde cualquier dispositivo, desde 2026-10-15):**
1. Abrir la URL del dashboard. Si lleva >12 h sin visitas, despertarlo (~30 s).
2. **📥 Cargar el Excel del lunes** → soltar el `Planning de PickUpADR` → *Cargar*.
3. Se valida, se añade al histórico del repo de datos y se archiva en
   `Excel-Lunes/<YYYY-MM-Mes>/Semana-XX_<fecha-snapshot>/`. Todo queda como un
   commit, así que hay copia de seguridad versionada de cada semana.

**Respaldo local en este PC (sigue funcionando igual):**
- Setup una vez: `powershell -File scripts\crear_accesos_directos.ps1` → crea
  "Finca" y "BUZON Finca" en el escritorio.
- Arrastrar el Excel a **"BUZON Finca"** y doble clic en **"Finca"**.
- `Finca.bat` ejecuta `scripts/procesar_buzon.py`, que ahora delega en
  `src/ingest/pipeline.py` (misma lógica que la web) y escribe en la nube si hay
  credenciales, o en local si no.
- Los Excel inválidos se quedan en BUZON con el motivo visible.

Las dos vías son equivalentes y cargar dos veces el mismo Excel es inocuo.

## Decisiones pendientes

- [ ] ¿Importar también snapshots previos al 2026-04-23 si existen, o empezar
      el histórico desde la primera semana nueva?
- [ ] Patrón del nombre del archivo Excel para reconocerlo automáticamente.
- [ ] Formato de exportación de informes: ¿PDF, Excel, solo pantalla?
- [ ] Confirmar HEX exactos del logo Vistabonita (paleta actual deducida de la web).

## Notas de archivos existentes en la raíz

- `Planning de PickUp_ADR (2).xlsx` — **Datos reales del Neptuno**, snapshot 2026-04-23,
  184 filas, 17 habitaciones. Este es el formato canónico.
- `PLANNING PICKUP-ADR NEPTUNO.xlsx` — **Plantilla / referencia visual**, 268 filas,
  79–95 habitaciones, rango hasta 2026-12-31. **No son datos del Neptuno**; se usó
  como referencia de los 4 gráficos que hay que reproducir. La ingesta lo rechaza
  automáticamente porque su inventario (95 hab) queda fuera del rango 15–19, lo cual
  es el comportamiento correcto. Ojo: tiene 149 columnas y `Tipo de Filtro=Allotment`,
  así que esa validación de capacidad es lo **único** que lo mantiene fuera.

## Decisiones tomadas

- **2026-04-23** — El histórico se guarda como Excel maestro, no SQLite. _Razón:_
  el usuario quiere poder abrir y revisar el histórico directamente con Excel.
- **2026-04-23** — `Excel-Lunes/` se mantiene en la raíz del proyecto (no dentro
  de `data/raw/`). _Razón:_ ya estaba creada con la estructura por mes/semana
  y es la carpeta a la que el usuario arrastra los Excel cada lunes.
- **2026-04-23** — Capacidad del hotel: **17 habitaciones**. Verificado con los
  datos del Excel (3 reservas + 14 libres = 17, coincide con `%Ocup = 17.65%`).
  _Matizado el 2026-09-15:_ la invariante completa incluye `Bloqueadas`.
- **2026-04-23** — El formato del Excel fuente será **siempre** el del archivo
  `Planning de PickUp_ADR (2).xlsx`: hoja `Planning de PickUpADR`, tabla `Table1`
  con 149 columnas, filtrado por `Tipo de Filtro = Allotment`. La ingesta puede
  validar rígidamente el esquema sin preocuparse por variantes.
- **2026-04-23** — Stack instalado y validado:
  - Python 3.12.10 (vía `winget install Python.Python.3.12` en scope user).
  - Entorno virtual en `.venv/` (decisión: **venv**, no `uv`; más estándar y
    con cero dependencias externas).
  - Librerías: pandas 3.0.2, openpyxl 3.1.5, streamlit 1.56.0, plotly 6.7.0, pyyaml 6.0.3.
  - Confirmado end-to-end leyendo el Excel: 184 filas × 149 columnas, rango
    2026-04-23 → 2026-10-23, `Tipo de Filtro=Allotment`, 3 reservas + 14 libres = 17 hab.
  - Pandas interpreta las fechas automáticamente (no hacen falta conversiones
    de serial date).
  - La consola de Windows (CP1252) **no soporta caracteres Unicode**. Los scripts
    que impriman deben usar `PYTHONIOENCODING=utf-8` o evitar símbolos tipo `→`/`%`.
- **2026-04-25** — Pipeline de ingesta + histórico operativo:
  - `src/ingest/excel_reader.py` valida (149 cols, `Tipo de Filtro=Allotment`,
    Reservas+Libres=17) y añade `Snapshot` + `Archivo Origen`.
  - `src/storage/historico.py` deduplica por `(Snapshot, Fecha)` y reescribe
    `data/historico/historico_neptuno.xlsx` (hoja `Historico`).
  - CLI: `python scripts/cargar_semana.py "ruta/al/Excel.xlsx"`.
- **2026-04-25** — Stack del dashboard Streamlit + Plotly montado:
  - `app.py` arranca con `streamlit run app.py` (config en `.streamlit/config.toml`).
  - Lanzador con doble clic: `scripts/abrir_dashboard.bat`.
  - `src/analysis/series.py` produce los DataFrames; `src/ui/graficos.py` los
    pinta; `src/ui/tema.py` define paleta + plantilla Plotly.
- **2026-04-25** — Marca **Finca Vistabonita / Hotel Neptuno** (verde botánico
  `#3D6E47` + azul océano `#2E5C7E` + dorado arena `#C9A66B`, Inter font, deducido
  del logo verde+azul de finca-vistabonita.com). Verde = CY/positivo,
  rojo terracota = LY/negativo, gris = referencia.
- **2026-04-25** — Estructura del dashboard (orden definitivo aprobado):
  1. KPIs cabecera (8 métricas CY vs LY).
  2. 🚨 Disponibilidad próximos 30 días (línea con marcadores por umbral
     0-4/5-8/9-11/12-17 libres + sombras de finde).
  3. 📈 Pickup neto por mes (barras + selector ventana en sidebar).
  4. 💰 Producción mensual CY vs LY.
  5. 🛏️ **Combinado** Libres CY/LY + Pickup diario por mes (un único plot
     con doble eje Y; default "Horizonte completo" muestra solo libres anual,
     al elegir mes muestra ambos juntos con sombras de finde).
  6. 🌊 Pickup por ventana (área spline 3 series).
  7. 💶 ADR diario (línea CY + LY punteada + media).
  8. 📅 Reservas mensuales CY vs LY.
  9. 📊 Tabla mensual estilizada (Producción CY en negrita, Δ% en verde/rojo).
- **2026-04-25** — Eje X de gráficos categóricos por día: `DD/MM` en negrita
  solo en día 1 y cambios de mes; resto solo `DD`. Inicial del día semana
  (L M X J V S D) en gris pequeño debajo. Lunes en negrita. Sombras azules
  verticales (`AZUL_OCEANO` con opacidad 0.07) en bloques Vie-Sáb-Dom.
- **2026-04-25** — `add_vrect` no funciona en `make_subplots` con
  `secondary_y=True`; usar `add_shape(type="rect", xref="x", yref="y domain")`.
- **2026-04-28** — Workflow semanal de "un gesto":
  - `Excel-Lunes/BUZON/` es la única drop zone. El usuario suelta el Excel ahí
    (vía acceso directo "BUZON Neptuno" en el escritorio).
  - `scripts/procesar_buzon.py` recorre el buzón, valida cada Excel, añade al
    histórico y archiva en `Excel-Lunes/<mes>/Semana-XX_<fecha>/`. Si el
    formato es inválido, deja el archivo en BUZON y muestra el motivo.
  - `Neptuno.bat` (raíz) procesa el buzón y arranca Streamlit con
    `start "" http://localhost:8501` que abre el navegador automáticamente.
  - `scripts/crear_accesos_directos.ps1` crea los dos `.lnk` en el escritorio
    (Neptuno + BUZON Neptuno) con iconos del shell de Windows.
  - El nombre de mes/semana se deriva de la fecha del **snapshot** del Excel
    (no del sistema), robusto si se procesa con retraso. Semana ISO.
  - Entry point único: `Neptuno.bat`. El antiguo `scripts/abrir_dashboard.bat`
    queda como lanzador "solo dashboard" sin procesar buzón.
- **2026-09-15** — **Apartamentos bloqueados (fuera de venta).** La invariante real
  del hotel es `Reservas + Libres + Bloqueadas = 17`, no `Reservas + Libres = 17`.
  `Bloqueadas` ya venía entre las 149 columnas, pero el código la ignoraba.
  - _Síntoma:_ al bloquear 1 apartamento, `Reservas + Libres` daba 16 y la ingesta
    rechazaba el Excel entero. Además solo se miraba **la fila 0**, así que el
    snapshot del 2026-08-26 había entrado con 7 días bloqueados sin avisar.
  - `src/inventario.py` (nuevo) es ahora la **fuente única** de `HABITACIONES_TOTALES`,
    con `bloqueadas()`, `total_inventario()` y `descuadre()`. `excel_reader.py` y
    `series.py` lo importan (antes cada uno tenía su propio `17`).
  - La validación recorre **todas las filas** y solo rechaza si el total sale del
    rango **15–19** (`TOLERANCIA = 2`). Motivo del tope: la plantilla ajena
    `PLANNING PICKUP-ADR NEPTUNO.xlsx` tiene 149 columnas y `Allotment`, así que
    esta validación es lo **único** que la mantiene fuera del histórico.
  - Un descuadre inexplicado (`R+L+B ≠ 17`) **no bloquea la carga**: entra marcado.
    Prioridad: no quedarse sin dashboard un lunes.
  - **Ocupación y RevPAR siguen sobre 17 fijo**, igual que el PMS (el 15/09:
    9/17 = 52,94 % aunque solo hubiera 16 vendibles). Verificado contra
    `%Ocup.Habitaciones` del Excel. Ningún KPI cambió de valor.
  - **Sin cambios de esquema** en el histórico (sigue en 151 columnas): el descuadre
    se deriva al vuelo, y los días del 26/08 quedaron marcados retroactivamente.
  - Visible como `*` dorado en el eje X de los gráficos diarios (+ detalle en el
    hover) y como aviso naranja bajo los KPIs. `procesar_buzon.py` también lo avisa
    por consola.
- **2026-09-15** — `Etiqueta multilinea` **es la clave de categoría** del eje X
  (`type="category"`). El gráfico combinado alinea las barras de `pickup_diario_mes`
  con las líneas de `libres_cy_vs_ly_mes` comparando esas cadenas HTML. Por eso la
  genera un único helper `_etiqueta_dia_mes()` en `series.py`: si las dos funciones
  produjeran cadenas distintas para el mismo día, el eje se duplicaría y el gráfico
  se partiría. **Cualquier cambio en esa etiqueta debe hacerse en el helper.**
- **2026-10-15** — **Despliegue en la nube** (acceso desde el MacBook y carga del
  Excel desde cualquier dispositivo).
  - **Plataforma:** Streamlit Community Cloud, plan gratuito.
    _Supabase descartado:_ su plan gratuito **pausa el proyecto a los 7 días de
    inactividad** y esta app se usa una vez por semana; cada lunes habría que
    despertarlo a mano desde su panel.
  - **DOS repos, y la separación es obligatoria:**
    - `revenue-finca` — **pública**, solo código.
    - `revenue-finca-datos` — **privada**, histórico + Excel semanales.

    _Razón:_ Streamlit **reinicia la app en cada push al repo desde el que
    publica**. Con los datos en ese mismo repo, cada carga de Excel reiniciaría la
    app a media operación. **No unificar nunca los dos repos.**
  - **Código público / datos privados.** Publicar desde un repo privado exige a
    Streamlit el scope `repo` de GitHub, que da lectura y escritura sobre *todos*
    los repos de la cuenta y no tiene variante de solo lectura. Con el código
    público ese permiso no hace falta y los datos se tocan con un fine-grained
    token limitado al repo de datos. La visibilidad de la app es independiente de
    la del repo: el dashboard es privado por lista de invitados.
  - **`src/storage/almacen.py`** (nuevo) es la pieza central: `AlmacenLocal` y
    `AlmacenGitHub` tras la misma interfaz. `crear_almacen()` elige según haya
    credenciales. El mismo código corre en los dos sitios.
  - **El histórico (1,84 MB) supera el límite de 1 MB de lectura de la API de
    GitHub.** El `GET /contents` normal devuelve el contenido **vacío** por encima
    de 1 MB, *sin dar error*. Hay que leerlo con
    `Accept: application/vnd.github.raw`. `AlmacenGitHub.leer_historico()` además
    rompe explícitamente si recibe vacío, para no sobrescribir el histórico bueno
    con un solo snapshot. Escribir con `PUT` sí admite ese tamaño.
  - **`src/ingest/pipeline.py`** (nuevo): `procesar_excel(datos, nombre, almacen)`
    es la **única** ruta de ingesta. La usan la web y el buzón local, así que no
    pueden divergir.
  - `leer_snapshot()` acepta ahora ruta **o** bytes (un Excel subido llega en
    memoria). `_validar()` recibe el nombre, no la ruta.
  - **Escritura local ahora atómica** (fichero temporal + `replace`). Antes
    `ExcelWriter(mode="w")` truncaba el histórico bueno antes de tener el nuevo,
    sin ninguna copia de seguridad.
  - **El flujo local se mantiene como respaldo.** Si este PC tiene credenciales,
    el doble clic escribe en la nube y todo va sincronizado; sin ellas, trabaja en
    local. La deduplicación por `(Snapshot, Fecha)` con `keep="last"` hace que
    **recargar el mismo Excel sea inocuo**, así que cualquier desincronización se
    arregla volviendo a subir el fichero.
  - **La app se duerme a las 12 h sin visitas.** Al usarse semanalmente, cada lunes
    estará dormida: un botón y ~30 s. Es el plan gratuito, no es un fallo.
  - `.gitignore` reescrito: ignora `*.xlsx` en **cualquier** carpeta,
    `.streamlit/secrets.toml`, `.claude/` e imágenes. Verificado fichero a fichero
    con `git check-ignore` antes de publicar nada.
  - `requirements.txt` con versiones **fijadas** (antes todo `>=`, así que la nube
    habría instalado versiones distintas a las probadas).
  - Borrado `config/settings.yaml`: nadie lo leía y contradecía al código (decía
    `historico_neptuno.xlsx`; el real es `historico_finca.xlsx`).

## Gráficos de referencia

Los 4 gráficos del Excel `PLANNING PICKUP-ADR NEPTUNO.xlsx` definen el v0
del dashboard:

1. **Ocupación CY vs LY** — área diaria de habitaciones libres actual vs año anterior.
2. **Reservas CY vs LY** — barras por mes.
3. **Pickup por ventana** — área con series día / semana / 2 semanas. **Gráfico clave.**
4. **Resumen mensual** — barras por mes (12 meses).

## Glosario

- **Pickup:** reservas netas captadas en una ventana (1/7/14/28 días).
- **On-the-books:** reservas confirmadas en el snapshot.
- **CY / LY:** Current Year / Last Year.
- **ADR:** Average Daily Rate — precio medio por habitación ocupada.
- **RevPAR:** Revenue Per Available Room.
- **Pax:** personas alojadas.
