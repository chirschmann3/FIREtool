"""Pulls data from online source that returns SP500 info on monthly basis since 1870"""

import datapackage
import pandas as pd

class SPYdata():

    def __init__(self):

        return

    def get_data(self):
        # code from https://datahub.io/core/s-and-p-500#pandas
        data_url = 'https://datahub.io/core/s-and-p-500/datapackage.json'

        # to load Data Package into storage
        package = datapackage.Package(data_url)

        # to load only tabular data
        resources = package.resources
        for resource in resources:
            if resource.tabular:
                data = pd.read_csv(resource.descriptor['path'])

        # change Date column to datetime
        data['Date'] = pd.to_datetime(data['Date'])

        return data
