from spyre import server
import pandas as pd
import os
import numpy as np

class SetData(server.App):
    title = "Візуалізація Даних"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'NOAA',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": [{"label": "Vinnytsya", "value": "Вінницька"},
                        {"label": "Volyn", "value": "Волинська"},
                        {"label": "Dnipropetrovs'k", "value": "Дніпропетровська"},
                        {"label": "Donets'k", "value": "Донецька"},
                        {"label": "Zhytomyr", "value": "Житомирська"},
                        {"label": "Transcarpathia", "value": "Закарпатська"},
                        {"label": "Zaporizhzhya", "value": "Запорізька"},
                        {"label": "Ivano-Frankivs'k", "value": "Івано-Франківська"},
                        {"label": "Kiev", "value": "Київська"},
                        {"label": "Kirovohrad", "value": "Кіровоградська"},
                        {"label": "Luhans'k", "value": "Луганська"},
                        {"label": "L'viv", "value": "Львівська"},
                        {"label": "Mykolayiv", "value": "Миколаївська"},
                        {"label": "Odessa", "value": "Одеська"},
                        {"label": "Poltava", "value": "Полтавська"},
                        {"label": "Rivne", "value": "Рівенська"},
                        {"label": "Sumy", "value": "Сумська"},
                        {"label": "Ternopil'", "value": "Тернопільська"},
                        {"label": "Kharkiv", "value": "Харківська"},
                        {"label": "Kherson", "value": "Херсонська"},
                        {"label": "Khmel'nyts'kyy", "value": "Хмельницька"},
                        {"label": "Cherkasy", "value": "Черкаська"},
                        {"label": "Chernivtsi", "value": "Чернівецька"},
                        {"label": "Chernihiv", "value": "Чернігівська"},
                        {"label": "Crimea", "value": "Республіка Крим"}],
            "key": 'region',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Year min',  
            "key": 'year_min',  
            "value": '',  
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Year max',  
            "key": 'year_max',  
            "value": '',  
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Week min',
            "key": 'week_min',
            "value": '',
            "min_value": 1,
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Week max',
            "key": 'week_max',
            "value": '',
            "max_value": 52,
            "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        current_directory = os.getcwd()
        filename = "all.csv"
        full_path = os.path.join(current_directory, filename)
        df = pd.read_csv(full_path)
        return df

    def getTable(self, params):
        df = self.getData(params)
        region = params['region']
        year_min = int(params['year_min'])
        year_max = int(params['year_max'])
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        if week_max < week_min or year_max < year_min:  
            return pd.DataFrame({'message': ['Будь ласка, введіть правильні дані для Week min і Week max або Year min і Year max.']})
        data = df[(df['area'] == region) & (df['Year'].between(year_min, year_max)) & (df['Week'].between(week_min, week_max))]
        columns = ['Year', 'Week', params['NOAA'], 'area']
        return data.loc[:, columns]

    def getPlot(self, params):
        region = params['region']
        year_min = int(params['year_min'])
        year_max = int(params['year_max'])
        ticker = params['NOAA']
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        df = self.getData(params)
        data = df[(df['area'] == region) & (df['Year'].between(year_min, year_max)) & (df['Week'].between(week_min, week_max))]
        plt_obj = data.pivot(index='Week', columns='Year', values=ticker).plot()
        plt_obj.set_ylabel("NOAA дані")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для регіону {region} у {year_min}-{year_max} роках для вказаних тижнів")
        plt_obj.set_xticks(np.arange(week_min, week_max + 1, 1))
        plot = plt_obj.get_figure()
        return plot
    
if __name__ == '__main__':
    app = SetData()
    app.launch(port=8080)
