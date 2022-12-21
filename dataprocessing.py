"""
Handles the DataProcessing class
"""

import pandas as pd
import json
from os.path import dirname, abspath
from utils import add_lat_long

data_folder = dirname(abspath(__file__)) + "/data"
companies_file = data_folder + "/companies.csv"
locations_file = data_folder + "/locations.csv"
country_file = data_folder + "/country.json"
city_file = data_folder + "/city.json"


def load_companies_data(csv_file):
    """
    Loads content of csv file into a dataframe. The supported file header which format is:
    "company_id, employees_total, founding_date,industry_id"
    :param csv_file:
    :return: a dataframe
    """
    companies = pd.read_csv(csv_file, sep=";")
    return companies


def load_locations_data(csv_file):
    """
    Loads content of csv file into a dataframe. The supported file header which format is:
    "company_id, country_id, city_id, address, is_headquarter"
    Keep only headquarter's locations
    :param csv_file:
    :return: a dataframe
    """
    locations = pd.read_csv(csv_file, sep=";")
    locations = locations[
        locations["is_headquarter"] == 1 & (locations["address"].notnull()) | (locations["city_id"].notnull())]
    return locations


def json_to_dict(json_file):
    """
    Loads content of json file into a dictionary.
    :param json_file:
    :return: a dictionary
    """
    new_dict = dict()
    with open(json_file) as f:
        data = json.load(f)
    for item in data:
        new_dict[item['id']] = item['name']
    return new_dict


def clean_df():
    """
    Create a clean list of companies by merging companies and locations
    :return: a list of companies ("company_id", "latitude", "longitude")
    """
    df = load_companies_data(companies_file).merge(load_locations_data(locations_file), how='left',
                                                   on='company_id')
    df = df[['company_id', 'country_id', 'city_id', 'address']]
    df = df.fillna(0)
    df[['country_id', 'city_id']] = df[['country_id', 'city_id']].astype(int)
    df = df.replace({"country_id": json_to_dict(country_file)})
    df = df.replace({"city_id": json_to_dict(city_file)})
    clean_l = df.to_dict('records')
    return add_lat_long(clean_l)
