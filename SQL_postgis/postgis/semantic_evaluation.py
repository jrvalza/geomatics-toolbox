import json
import psycopg2

#conection toDB
conn = psycopg2.connect(database="proyectoPostGIS",
                        user="postgres",
                        password="pg",
                        host="localhost",
                        port=5432)
cur = conn.cursor()

# List of tables and columns
tablas_campos ={"jr2.building": ["gml_id", "currentuse", "numberofbuildingunits", "value"],
                "jr2.buildingpart": ["gml_id", "numberoffloorsaboveground", "numberoffloorsbelowground"],
                "jr2.cadastralparcel": ["gml_id", "areavalue", "localid"],
                "jr2.tramovial": ["id_tramo", "id_vial", "clased", "nombre", "firmed"],
                "jr2.portalpk": ["id_tramo", "id_vial", "id_porpk", "numero"],
                "jr2.tramocurso": ["id_curso", "nombre", "tipo_curso"],
                "jr2.siose_pol": ["id_polygon", "codiige", "hilucs"],
                "jr2.siose_codiige": ["descripcion", "color_html"],
                "jr2.siose_hilucs": ["descripcion", "color_html"],
                }

################################################################################
#iteration to find fields with null or non-null values
################################################################################
#Init
result = {}
for tabla, campos in tablas_campos.items():
    if tabla not in result.keys():
        result[tabla]={'Nulls':[], 'Not Nulls':[]}
    for campo in campos:
        # SQL query
        cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {campo} IS NULL")
        # get result
        nulos = cur.fetchone()[0]
        if nulos > 0:
            result[tabla]['Nulls'].append(campo)
        else:
            result[tabla]['Not Nulls'].append(campo)

for key, values in result.items():
    print("="*10, f"Tabla {key}", "="*10)
    print(json.dumps(values["Not Nulls"]), '\n')



################################################################################
# Iteration to find fields with unique values
################################################################################
#Init
result = {}

for tabla, campos in tablas_campos.items():
    cur.execute(f"SELECT COUNT(*) FROM {tabla}")
    total_rows = cur.fetchall()[0][0]

    if tabla not in result.keys():
        result[tabla]={'Unique':[], 'Not Unique':[]}

    for campo in campos:
        # SQL query
        cur.execute(f"SELECT COUNT(DISTINCT({campo})) FROM {tabla}")
        # get result
        distinct_values = cur.fetchone()[0]
        if distinct_values == total_rows:
            result[tabla]['Unique'].append(campo)
        else:
            result[tabla]['Not Unique'].append(campo)

for key, values in result.items():
    if len(values["Unique"]) == 0:
        continue
    print("="*10, f"Tabla {key}", "="*10)
    print(json.dumps(values["Unique"]))



################################################################################
# Iteration to identify positive values
################################################################################
# List of tables and columns
tablas_campos ={"jr2.building": ["numberofbuildingunits", "value"],
                "jr2.buildingpart": ["numberoffloorsaboveground", "numberoffloorsbelowground"],
                "jr2.cadastralparcel": ["areavalue"],
                "jr2.tramovial": ["id_tramo", "id_vial"],
                "jr2.portalpk": ["id_tramo", "id_vial", "id_porpk", "numero"],
                }
#Init
result = {}
for tabla, campos in tablas_campos.items():
    if tabla not in result.keys():
        result[tabla]={'Values_Negatives':[], 'Values_Positives':[]}
    for campo in campos:
        # SQL query
        cur.execute(f"SELECT MIN({campo}) FROM {tabla}")
        # get result
        value = cur.fetchone()[0]
        if value >= 0:
            result[tabla]['Values_Positives'].append(campo)
        else:
            result[tabla]['Values_Negatives'].append(campo)

for key, values in result.items():
    print("="*10, f"Tabla {key}", "="*10)
    print(json.dumps(values["Values_Positives"]), '\n')



################################################################################
# Iteration to find bounded fields
################################################################################

# List of tables and columns
tablas_campos ={"jr2.building": ["currentuse"],
                "jr2.tramovial": ["clased", "firmed"],
                "jr2.tramocurso": ["tipo_curso"],
                }
#Init
result = {}

for tabla, campos in tablas_campos.items():
    if tabla not in result.keys():
        result[tabla]={}
    for campo in campos:
        # SQL query
        cur.execute(f"SELECT DISTINCT({campo}) FROM {tabla}")
        # get result
        values = [aux[0] for aux in cur.fetchall()]
        if campo not in result[tabla].keys():
            result[tabla][campo]=values

for key, values in result.items():
    print("="*10, f"Tabla {key}", "="*10)
    print(json.dumps(values), '\n')

# close conection
cur.close()
conn.close()


