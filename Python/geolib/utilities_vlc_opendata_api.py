
import json
from utilities import utilities

# all catalogue
catalogue = utilities.vlc_opendatasoft_catalogue()
print(json.dumps(catalogue, indent=4))

#dataset
keywork = 'wifi'
dataset = utilities.vlc_opendatasoft_find_dataset(keywork)
print(json.dumps(dataset, indent=4))

# other dataset
dataset_id = 'aparcaments-bicicletes-aparcamientos-bicicletas'
dataset = utilities.get_vlc_opendatasoft_dataset(dataset_id)
print(json.dumps(dataset, indent=4))
