import pandas as pd
import requests


def return_figures():
    """Creates four plotly visualizations


    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    indicators = ['TIME_SERIES_DAILY']
    company = 'MSFT'
    key = 'Y30E2S63RTWADYO4'

    data_frames = []
    urls = []

    for indicator in indicators:
        url = 'https://www.alphavantage.co/query?function=' + indicator +\
            '&symbol=' + company + '&outputsize=full&apikey=' + key
        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()['Time Series (Daily)']
        except:
            print('could not load data ', indicator)

        for i, date in enumerate(data):
            for j, value in enumerate(date):
                value['open'] = value['1. open']
                value['high'] = value['2. high']
                value['low'] = value['3. low']
                value['close'] = value['4. close']
                value['volume'] = value['5. volume']
            print(date)
        data_frames.append(date)

    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )


    # append all charts to the figures list
    figures = []
    # figures.append(dict(data=graph_one, layout=layout_one))

    return figures
