import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import datetime as dt
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc, Input, Output, no_update, State, callback

df = pd.read_csv(r"C:\Users\admin\Documents\Conda files\IBM's\Historical_wildfires.csv")

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month
month_names = [dt.datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
                        html.Img(src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMLoiaWivPI-o1YYKfn7yk51iWsYNIRe8wD6FiFgrPqQ&s', style={'height': '70px', 'margin-right': '15px'}),
                 html.H1('AUSTRALIA WILDFIRE DASHBOARD', style={'height':'60%','textAlign':'center','color':'Navy', 'font-weight':'bold','font-size':35, 'display':'inline-block'}),
                  html.Div([
                    html.Div([ 
                      html.H2(
                'Select Australia Region: ', style={'margin-right':'2em'}
            ), dcc.RadioItems([
                {'label':'New South Wales','value':'NSW'},
                {'label':'Northern Territory','value':'NT'},
                {'label':'Queensland','value':'QL'},
                {'label':'South Australia','value':'SA'},
                {'label':'Tasmania','value':'TA'},
                {'label':'Victoria','value':'VI'},
                {'label':'Western Australia','value':'WA'}], 'NSW',
                id='region',style = {'font-size':'20px', 'text-align-last':'left', 'justify-content':'center'},inline=True ), 
            ]),
            
            html.Div([
                html.H1( 'Select Year: ', style={'margin-right':'2em','font-size':'20px'}),
                dcc.Dropdown(df.Year.unique(), value=2005, id='year', style={'width':'40%','padding':'5px','font-size':'17px','text-align-last':'center','color':'black'})
                ], style={'display':'flex', 'justify-content':'left', 'align-items':'center'}),
           
        html.Div([
            html.Div([ ], id='pie-plot', className='chart'),
            html.Div([ ], id ='bar-plot', className ='chart'),
           
        ], style={'display':'flex',}),

        html.Div([
            html.Div([],id='line-plot', className='chart'),
            html.Div([], id='time-series', className='chart')
        ],  style={'display':'flex', }),

    ]),
], style ={'margin':'30px'})
@app.callback([Output(component_id='pie-plot', component_property='children'),
                Output(component_id='bar-plot', component_property='children'),
                Output(component_id='line-plot', component_property='children'),
                Output(component_id='time-series', component_property='children')],
                [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')]
                )


def data_choice(input_region, input_year):

    region_data = df[df['Region'] == input_region]
    year_data = region_data[region_data['Year'] == input_year]

    #Pie Chart on Monthly Average Estimated Fire Area
    pie_data = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    #Bar Chart on Monthly Average Count of Pixels for Presumed Vegetation Fires
    bar_data = year_data.groupby('Month')['Count'].mean().reset_index()
    scatter_data = year_data.groupby(['Count','Mean_confidence'])['Mean_estimated_fire_radiative_power'].mean().reset_index()
    time_series_data = year_data.groupby('Month')['Count'].sum().reset_index()


    pie_fig = px.pie(pie_data, names=month_names, values='Estimated_fire_area', title='{}: Monthly Average Estimated Fire Area {}'.format(input_region, input_year))
    pie_fig.update_traces(textinfo='percent', pull=[0.0,0.0,0,0,0,0,0,0,0,0], )
   
    bar_fig = px.bar(bar_data, x='Month', y='Count', title='{} : Monthly Average Count of Pixels for Presumed Vegetation Fires {}'.format(input_region, input_year))
    bar_fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=month_names)


    scatter_fig = px.scatter(scatter_data, x='Mean_confidence', y='Mean_estimated_fire_radiative_power', color='Count' ,title='Mean Estimated Fire Radiative Power vs. Mean Confidence {}'.format(input_region,input_year))

    time_series_fig = px.line(time_series_data, x='Month', y='Count', title='{}: Fire Count Trend over Months {}'.format(input_region, input_year))
    time_series_fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=month_names)


    return[dcc.Graph(figure=pie_fig),
            dcc.Graph(figure=bar_fig),
            dcc.Graph(figure=scatter_fig),
            dcc.Graph(figure=time_series_fig),]


if __name__=='__main__':
    app.run_server(debug=True)