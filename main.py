from utils import get_lat_long, list_to_json_file, calcul_distance, read_json
from dataprocessing import clean_df
from os.path import dirname, abspath
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

data_folder = dirname(abspath(__file__)) + "/data"
filename = data_folder + "/intermediate_file.json"
output_file = dirname(abspath(__file__)) + "/classes.json"


def main(entrepot_address):
    entrepot_coordinates = get_lat_long(entrepot_address)
    if os.path.exists(filename):
        logging.info("Le fichier demandé est en cours de création ...")
        companies_coordinates = read_json(filename)
    else:
        logging.info("Merci de patienter quelques instants ... ")
        companies_coordinates = clean_df()
        list_to_json_file(companies_coordinates, filename)
    classes = []
    for item in companies_coordinates:
        coor = (item['latitude'], item['longitude'])
        class_n = calcul_distance(coor, entrepot_coordinates)
        classes.append({'company_id': item['company_id'],
                        'class': class_n
                        })
    list_to_json_file(classes, output_file)


if __name__ == '__main__':
    main(" ".join(sys.argv[1:]))
