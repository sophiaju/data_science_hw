import pandas as pd
import numpy as np
from random import random

from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, PreText, Select
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, show

# user authentication through url params
args = curdoc().session_context.request.arguments

if ('username' in args) and ('password' in args):
    #print(args['username'][0].decode('utf-8'), args['password'][0].decode('utf-8'))
    user = args['username'][0].decode('utf-8')
    pwd = args['password'][0].decode('utf-8')
    if (user == 'nyc') and (pwd == 'iheartnyc'):

        # read in preprocessed data, _copy means that the december outlier was removed
        df = pd.read_csv('output_copy.csv', sep=',', dtype='str')
        all_2020 = pd.read_csv('all_2020_copy.csv', sep=',')

        # list of all zip codes
        zip_list = df.zip.unique()

        # gets list of all zips except the one passed in
        def diff(zip, zip_list):
            return [i for i in zip_list if i != zip]

        # callbacks

        # zip callbacks will update the options for selecting zip codes and call update
        def zip1_callback(attr, old, new):
            zip_select_2.options = diff(new, zip_list)

            update()

        def zip2_callback(attr, old, new):
            zip_select_1.options = diff(new, zip_list)

            update()

        # update will get the new zip data and graph it
        def update():
            zip1, zip2 = zip_select_1.value, zip_select_2.value

            # plot for zip1 data

            zip1 = zip_select_1.value

            df_zip1 = df.loc[df['zip']==zip1].sort_values(by='month')[['month','duration']]
            source1.data = df_zip1

            # plot for zip2 data

            zip2 = zip_select_2.value

            df_zip2 = df.loc[df['zip']==zip2].sort_values(by='month')[['month','duration']]
            source2.data = df_zip2


        # fix empty months in all 2020? this is not necessary
        for i in range(1,13):
            if i not in list(all_2020['month']):
                #print(i)
                all_2020 = all_2020.append(pd.DataFrame([[i, np.nan]], columns=['month','duration']), ignore_index=True)

            #print(all_2020.loc[all_2020['month']==i])

        all_2020 = all_2020.sort_values(by=['month'])
        #print(all_2020)

        # create ColumnDataSource
        source1 = ColumnDataSource(data=dict(month=[], duration=[]))
        source2 = ColumnDataSource(data=dict(month=[], duration=[]))

        # create dropdowns
        zip_select_1 = Select(title='zip 1', value='11415', options=diff('10000', zip_list))
        zip_select_2 = Select(title='zip 2', value='10000', options=diff('11415', zip_list))

        zip_select_1.on_change('value', zip1_callback)
        zip_select_2.on_change('value', zip2_callback)

        # create plot
        p = figure(title='Monthly average incident duration (in hours)', x_axis_label='month', y_axis_label='hours (avg)')

        # plot for all 2020 data
        p.line(list(all_2020['month']), list(all_2020['duration']), legend_label='all 2020', line_width=2)

        update()

        # plots for zip1 and zip2 and streamed in
        p.line(x='month', y='duration', source=source1, legend_label='zip1', line_width=2, color='green')
        p.line(x='month', y='duration', source=source2, legend_label='zip2', line_width=2, color='orange')

        widgets = column(zip_select_1, zip_select_2)
        layout = column(widgets, p)

        curdoc().add_root(layout)
        curdoc().title = "nyc_dash"
