# -*- coding: utf-8 -*-
"""
Script ETL Final: Limpieza Profunda + Carga a SQL (XAMPP)
Proyecto: Violencia Intrafamiliar Colombia
"""

import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

def clean_data_full(df):
    print("[1/4] Iniciando limpieza profunda de categorías (Modo Pesado)...")
    
    # 1. Eliminar columnas innecesarias
    cols_to_drop = [
        'id', 'identidad de género', 'transgénero', 'grupo de edad quinquenal', 
        'localidad del hecho', 'pertenencia grupal', 'código dane municipio', 
        'código dane departamento', 'codigo dane municipio', 'codigo dane departamento'
    ]
    col_lower = {c.lower(): c for c in df.columns}
    for c in cols_to_drop:
        if c in col_lower:
            df = df.drop(columns=[col_lower[c]])

    def clean_text_series(series):
        return series.astype(str).str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)

    # --- 2. Limpieza específica por columnas ---

    # 2.1 Grupo de edad
    col_edad = 'Grupo Mayor Menor de Edad'
    if col_edad in df.columns:
        df[col_edad] = clean_text_series(df[col_edad])
        df[col_edad] = df[col_edad].replace({
            'b) mayores de edad (>18 años)': 'Mayores de edad',
            'a) menores de edad (<18 años)': 'Menores de edad'
        })
        df[col_edad] = df[col_edad].str.replace(r'^[a-z]\)\s*mayor(es)? de edad.*', 'Mayores de edad', regex=True)
        df[col_edad] = df[col_edad].str.replace(r'^[a-z]\)\s*menor(es)? de edad.*', 'Menores de edad', regex=True)
        df[col_edad] = df[col_edad].str.replace(r'.*sin información.*', 'Sin información', regex=True)
        df[col_edad] = df[col_edad].str.capitalize()
        
    # 2.2 Escolaridad
    col_escolaridad = 'Escolaridad'
    if col_escolaridad in df.columns:
        df[col_escolaridad] = clean_text_series(df[col_escolaridad])
        df[col_escolaridad] = df[col_escolaridad].replace({
            'educación básica primaria': 'Básica primaria',
            'maestría': 'Especialización, maestría o doctorado',
            'doctorado o equivalente': 'Especialización, maestría o doctorado',
            'especialización, maestría o equivalente': 'Especialización, maestría o doctorado',
            'ninguna': 'Sin escolaridad',
            'educación básica secundaria': 'Básica secundaria',
            'educación básica secundaria o secundaria baja': 'Básica secundaria',
            'educación inicial y educación preescolar': 'Preescolar',
            'educación media o secundaria alta': 'Educación media',
            'tecnológica': 'Educación técnica y tecnológica',
            'técnica profesional': 'Educación técnica y tecnológica',
            'educación técnica profesional y tecnológica': 'Educación técnica y tecnológica',
            'profesional': 'Universitario'
        })
        df[col_escolaridad] = df[col_escolaridad].str.capitalize()

    # 2.3 Discapacidad
    col_disc = 'Tipo de Discapacidad'
    if col_disc in df.columns:
        df[col_disc] = df[col_disc].fillna('Sin información')
        temp_disc = clean_text_series(df[col_disc])
        condiciones = [
            temp_disc.str.contains('ninguna', na=False),
            temp_disc.str.contains('sin información', na=False)
        ]
        elecciones = ['No', 'Sin información']
        df['Discapacidad'] = np.select(condiciones, elecciones, default='Si')
        df = df.drop(columns=[col_disc])

    # 2.4 Municipio
    col_mun = 'Municipio del hecho DANE'
    if col_mun in df.columns:
        df[col_mun] = clean_text_series(df[col_mun]).str.capitalize()
        df[col_mun] = df[col_mun].str.replace(r'd\.c\.', 'D.C.', regex=True)

    # 2.5 Escenario del hecho (Mapeos Detallados)
    col_esc = 'Escenario del Hecho'
    if col_esc in df.columns:
        df[col_esc] = clean_text_series(df[col_esc])
        df[col_esc] = df[col_esc].str.replace(r'\s*,\s*', ', ', regex=True)
        df[col_esc] = df[col_esc].str.replace(r'\s*\(\s*', ' (', regex=True)
        df[col_esc] = df[col_esc].str.replace(r'\s*\)\s*', ')', regex=True)
        df[col_esc] = df[col_esc].str.replace(r'\.+$', '', regex=True)
        df[col_esc] = df[col_esc].str.replace(r'\.\)', ')', regex=True)
        df[col_esc] = df[col_esc].str.replace(r'almacen', 'almacén', regex=True)
        df[col_esc] = df[col_esc].replace({
            'calle (autopista, avenida, dentro de la ciudad)': 'vía pública y transporte',
            'vía pública': 'vía pública y transporte',
            'carretera (fuera de la ciudad)': 'vía pública y transporte',
            'parqueaderos, estacionamientos': 'vía pública y transporte',
            'vehículo servicio particular': 'vía pública y transporte',
            'vehículo de servicio particular': 'vía pública y transporte',
            'terminales de pasajeros': 'vía pública y transporte',
            'estaciones de servicio (bombas de gasolina)': 'vía pública y transporte',
            'vehículo de transporte': 'vía pública y transporte',
            'transporte masivo': 'vía pública y transporte',
            'ambulancia - transporte sanitario': 'vía pública y transporte',
            'establecimiento comercial (tienda, centro comercial, almacén, plaza de mercado)': 'establecimientos comerciales y de esparcimiento',
            'establecimiento comercial (tienda, centro comercial, almacén)': 'establecimientos comerciales y de esparcimiento',
            'establecimiento comercial (plaza de mercado, gallery)': 'establecimientos comerciales y de esparcimiento',
            'lugares de esparcimiento con expendio de alcohol': 'establecimientos comerciales y de esparcimiento',
            'establecimientos de expendio de comidas (restaurantes, asaderos, salsamentarias, etc)': 'establecimientos comerciales y de esparcimiento',
            'lugares de hospedaje (hoteles, campamentos y otros tipos de hospedaje no permanente, moteles, etc)': 'establecimientos comerciales y de esparcimiento',
            'taller': 'establecimientos comerciales y de esparcimiento',
            'establecimientos financieros y relacionados (bancos, fiduciarias, etc)': 'establecimientos comerciales y de esparcimiento',
            'espacios terrestres al aire libre (bosque, potrero, montaña, playa, etc)': 'zonas al aire libre y agropecuarias',
            'zonas de actividades agropecuarias': 'zonas al aire libre y agropecuarias',
            'terreno baldío': 'zonas al aire libre y agropecuarias',
            'espacios acuáticos al aire libre (mar, río, arroyo, humedal, lago, etc)': 'zonas al aire libre y agropecuarias',
            'espacios acuáticos al aire libre (mar, rio, arroyo, humedal, lago, etc)': 'zonas al aire libre y agropecuarias',
            'centros educativos': 'instituciones y servicios',
            'centro de atención médica (hospital, clínica, consultorio, etc)': 'instituciones y servicios',
            'oficinas y/o edificios de oficinas': 'instituciones y servicios',
            'centros de reclusión': 'instituciones y servicios',
            'establecimientos dedicados a la administración pública (cortes, juzgados, ministerios, etc)': 'instituciones y servicios',
            'lugares de cuidado de personas (hospicios, orfelinatos, hogares geriatricos, etc)': 'instituciones y servicios',
            'lugares de cuidado de personas (hospicios, orfelinatos, hogares geriátricos, etc)': 'instituciones y servicios',
            'guarniciones militares y/o de policía': 'instituciones y servicios',
            'áreas deportivas y/o recreativas': 'espacios culturales y recreativos',
            'lugares de actividades culturales (cines, teatros, museos, bibliotecas, etc)': 'espacios culturales y recreativos',
            'sitio de culto (capilla, iglesia, templo, etc)': 'espacios culturales y recreativos',
            'piscina y jacuzzi (establecimientos turísticos, recreativos, deportivos)': 'espacios culturales y recreativos',
            'piscina y jacuzzi (vivienda)': 'vivienda',
            'establecimiento industrial (fábrica, planta)y/o obras en construcción': 'establecimientos industriales y de construcción'
        })
        df[col_esc] = df[col_esc].str.capitalize()

    # 2.6 Actividad Durante el Hecho
    col_act = 'Actividad Durante el Hecho'
    if col_act in df.columns:
        df[col_act] = clean_text_series(df[col_act])
        df[col_act] = df[col_act].str.replace(r'\.+$', '', regex=True)
        df[col_act] = df[col_act].str.replace(r'\.\)', ')', regex=True)
        df[col_act] = df[col_act].replace({
            'actividades relacionadas con el aprendizaje': 'actividades relacionadas con el estudio y el aprendizaje'
        })
        df[col_act] = df[col_act].str.capitalize()
    
    # 2.7 Presunto Agresor Detallado
    col_agre = 'Presunto Agresor Detallado'
    if col_agre in df.columns:
        df[col_agre] = clean_text_series(df[col_agre])
        df[col_agre] = df[col_agre].str.replace(r'\s*\(\s*a\s*\)\s*', '(a)', regex=True)
        df[col_agre] = df[col_agre].str.replace(r'consanguineos', 'consanguíneos', regex=True)
        df[col_agre] = df[col_agre].str.replace(r'tio\(a\)', 'tío(a)', regex=True)
        df[col_agre] = df[col_agre].str.capitalize()

    # 2.8 Factor Desencadenante
    col_fact = 'Factor Desencadenante de la Agresión'
    if col_fact in df.columns:
        df[col_fact] = clean_text_series(df[col_fact])
        df[col_fact] = df[col_fact].replace({
            'alcoholismo / drogadicción': 'consumo de alcohol y/o sustancias psicoactivas',
            'enfermedad fisica o mental': 'enfermedad física o mental',
            'otras razones': 'otras'
        })
        df[col_fact] = df[col_fact].str.capitalize()

    # 2.9 Días de Incapacidad
    col_inc = 'Días de Incapacidad Medicolegal'
    if col_inc in df.columns:
        df[col_inc] = clean_text_series(df[col_inc])
        df[col_inc] = df[col_inc].replace({
            'cero días y sin información': '0',
            'cero días': '0',
            'cero': '0',
            'sin días de incapacidad': '0',
            'sin información': 'Sin información'
        })
        df[col_inc] = df[col_inc].str.capitalize()

    # 2.10 Zona del Hecho
    col_zona = 'Zona del Hecho'
    if col_zona in df.columns:
        df[col_zona] = clean_text_series(df[col_zona])
        df[col_zona] = df[col_zona].str.replace(r'\s*\(\s*', ' (', regex=True)
        df[col_zona] = df[col_zona].str.replace(r'\s*\)\s*', ')', regex=True)
        df[col_zona] = df[col_zona].str.capitalize()

    return df

def main():
    # 1. EXTRACT
    filepath = r'd:\OneDrive\Desktop\prydefi\Violencia_intrafamiliar._Colombia,_años_2015_a_2024._Cifras_definitivas_20260424.csv'
    print(f"--- INICIANDO PROCESO ETL A SQL ---")
    
    try:
        # Intentamos UTF-8 primero ya que es el estándar para caracteres especiales
        df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    except:
        # Si falla, usamos latin-1 como respaldo
        df = pd.read_csv(filepath, encoding='latin-1', low_memory=False)

    # 2. TRANSFORM
    df = clean_data_full(df)
    df = df.loc[:, ~df.columns.duplicated()]

    # 3. LOAD (SQL)
    print("[3/4] Conectando a MySQL (XAMPP - DB: 'limpios')...")
    try:
        # Agregamos charset=utf8mb4 para asegurar que las tildes viajen bien a la base de datos
        engine = create_engine('mysql+mysqlconnector://root:@localhost/limpios?charset=utf8mb4')
        
        print("[4/4] Exportando datos limpios a la tabla 'reporte_violencia'...")
        df.to_sql(
            name='reporte_violencia', 
            con=engine, 
            if_exists='replace', 
            index=False,
            chunksize=10000
        )
        
        print("\n--- CARGA EXITOSA ---")
        print("Ahora puedes usar esta tabla en Power BI conectandote a MySQL.")
        
        engine.dispose()
        
    except Exception as e:
        print("\n--- ERROR DE CARGA ---")
        print(f"Detalle del error: {str(e)}")
        print("Verifica que XAMPP este activo y que la base de datos 'limpios' haya sido creada.")

if __name__ == "__main__":
    main()
