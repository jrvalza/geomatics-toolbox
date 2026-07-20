
proyecto = QgsProject.instance()
capa_prov = proyecto.mapLayersByName('PROVINCIA')[0]
capa_est = proyecto.mapLayersByName('ESTACIONES')[0]

for reg in capa_prov.getFeatures():
    if reg.attribute('NOMBRE') == 'SORIA':
        geom_prov = reg.geometry()
        break
ids = []
for reg in capa_est.getFeatures():
    geom_est = reg.geometry()
    if geom_prov.contains(geom_est):
        ids.append(reg.id())
capa_est.select(ids)
