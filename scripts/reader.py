import mailbox
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import re

class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif self.file_path.endswith('.gpx'):
            self.read_gpx()

    def get_data(self):
        return self.data

    def get_columns(self):
        return self.data.columns

    def get_rows(self):
        return self.data.shape[0]

    def get_row(self, row_index):
        return self.data.iloc[row_index]

    def get_row_by_id(self, id):
        return self.data.loc[self.data['id'] == id]
    
    def read_gpx(self):
        gpx_data = open(self.file_path, 'r').read()
        lat = pd.Series(re.findall(r'lat="([^"]+)',gpx_data), name='lat', dtype=float)
        lon = pd.Series(re.findall(r'lon="([^"]+)',gpx_data), name='lon', dtype=float)
        time = pd.Series(re.findall(r'<time>([^\<]+)',gpx_data), name='time')
        for i in range(len(time)):
            time[i] = pd.to_datetime(time[i])
        ele = pd.Series(re.findall(r'<ele>([^\<]+)',gpx_data), name='ele', dtype=int)
        hr = pd.Series(re.findall(r'<gpxtpx:hr>([^\<]+)',gpx_data), name='hr', dtype=int)
        self.data = pd.concat([lat,lon,time,ele,hr],axis=1)
    
    def build_gpx_plot(self):

        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.6, 0.4],
            # row_heights=[0.4, 0.6],
            specs=[[{"type": "scattermapbox"}, {"type": "surface"}]]
            )

        fig.add_trace(
                go.Scattermapbox(
                    mode = 'markers+lines',
                    lon=self.data['lon'],
                    lat=self.data['lat'],
                    marker={'size':10}
                )
            ,
            row=1, col=1
        )

        # fig.add_trace(
        #     #go.Surface(
        #     go.Mesh3d(
        #         x=self.data['time'],
        #         z=self.data['hr'],
        #         y=self.data['ele'],
        #         ),
        #     row=1, col=2,
        # )

        fig.add_trace(
            # go.Scatter(
            #     x=self.data['time'],
            #     y=self.data['ele']
            # ),
            go.Scatter3d(x=self.data['time'], z=self.data['ele'],
                           y=self.data['hr'], mode="lines"),
            row = 1,
            col = 2
        )

        fig.update_layout(
            mapbox={
                'zoom':11,
                'center':{
                    'lon':(self.data['lon'].min()+self.data['lon'].max())/2,
                    'lat':(self.data['lat'].min()+self.data['lat'].max())/2
                    },
                'style': 'stamen-terrain'
            }
        )
        fig.show()

if __name__ == "__main__":
    reader = Reader('res/07-08-2022.gpx')
    print(reader.data)
    reader.build_gpx_plot()
        

