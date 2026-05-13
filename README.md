# analisis-violencia-intrafamiliar-colombia
Análisis de datos y dashboard en Power BI sobre la violencia intrafamiliar en Colombia (2015-2024).
# 📊 Análisis de Violencia Intrafamiliar en Colombia (2015-2024)

## 📝 Descripción del Proyecto
Este proyecto es un análisis integral de los datos de violencia intrafamiliar en Colombia, utilizando registros del Instituto Nacional de Medicina Legal y Ciencias Forenses. El objetivo principal es identificar patrones demográficos, temporales y geográficos para entender el comportamiento de este fenómeno, transformando datos en bruto en insights accionables mediante visualizaciones de alto impacto.

## 🛠️ Herramientas y Tecnologías Utilizadas
* **Python (Pandas, Regex):** Limpieza profunda de datos, normalización de variables categóricas, extracción y estandarización de campos complejos.
* **SQL:** Estructuración de datos y consultas de validación preparatorias.
* **Power BI & DAX:** Modelado de datos, creación de medidas analíticas y diseño del dashboard interactivo.

## ⚙️ Proceso de Datos (ETL)
La base de datos original contenía más de cientos de miles de registros con inconsistencias. El proceso abordó:
1. **Extracción y Limpieza:** Uso del script `limpieza_pesada_sql.py` para corregir problemas de codificación (UTF-8), caracteres especiales y valores nulos.
2. **Transformación:** Creación de nuevas categorías (Ej. agrupaciones por "Momento del Día", consolidación del perfil del agresor).
3. **Carga:** Conexión del dataset limpio a Power BI.
*(Nota: Por cuestiones de peso y políticas de GitHub, los archivos CSV originales de >100MB no están en este repositorio).*

## 📈 Dashboard y Resultados Clave
*<img width="899" height="484" alt="1_ed" src="https://github.com/user-attachments/assets/2d4b963f-88d6-464a-9783-a2f1f8f5f4e1" />*

### 🔍 Hallazgos Principales:
* **Perfil de las Víctimas y Agresores:** La gran mayoría de las víctimas son mayores de edad (154.162 casos) y concentran un nivel educativo de básica primaria o preescolar.
<img width="867" height="314" alt="6_ed" src="https://github.com/user-attachments/assets/db6276bf-7cb6-4aae-81a9-02fe100c0a05" />

A nivel de agresores, el círculo íntimo familiar es el más riesgoso: los **hermanos/as (42.203)** y los **padres (34.408)** son los principales victimarios. <img width="874" height="486" alt="5_ed" src="https://github.com/user-attachments/assets/602c4b7b-6739-4992-965a-2cecbb421618" />


La "Intolerancia y el machismo" es el detonante abrumador en más del 70% de las agresiones.
<img width="903" height="398" alt="4_ed" src="https://github.com/user-attachments/assets/886a2171-1bcc-49e8-b2f5-9e480d1b474d" />


* **Escenarios y Patrones de Riesgo:** La **vivienda** es el escenario más peligroso por un margen crítico (179.222 reportes, casi el 80% del total). Además, los picos de violencia ocurren irónicamente mientras las víctimas realizan actividades cotidianas en el hogar (cuidado personal, desplazamiento rutinario o trabajo doméstico no remunerado).
* **Zonas Críticas:** El fenómeno es altamente urbano. Las **cabeceras municipales** concentran más de 206.000 casos (frente a 16.267 rurales). Las tres ciudades con mayor volumen de alertas históricas son **Bogotá, D.C. (61.428)**, **Medellín (16.239)** y **Cali (8.015)**.

## 📁 Estructura del Repositorio
* `limpieza_pesada_sql.py`: Código en Python con el proceso completo de limpieza y ETL.
* `Reporte_violencia.pbix`: Archivo fuente del dashboard interactivo en Power BI.
.

## 👤 Autor
* **Daniel Martinez Leon** - Analista de Datos 
(https://www.linkedin.com/in/daniel-martínez-leon-tech/)
