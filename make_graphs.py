
import json
import os
from datetime import datetime, date
import math

# plotting
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

N_TICKS = 10
n_figures = 0

def plot_trend(measure, dates, ax):
    """
    Plot trend
    
    The trend is calculated as mid point of two-weeks linear regression on measure (with 13 days overlapping)
    """
    trend = []
    trend_dates = []

    for index, day in enumerate(dates):
        # avoid first and last 7 days due to insufficient data
        if (index < 7 or index > len(dates)-7): continue

        model = np.polyfit(np.arange(0, 14), measure[index-7:index+7], 1)
        predict = np.poly1d(model)
        trend.append(predict(7))
        trend_dates.append(day)

    ax.plot(trend_dates, trend, label='Andamento', color='r')

    return


def plot_measure(measure, dates, title, is_variation=False):
    global n_figures

    fig = plt.figure(n_figures)
    ax = fig.subplots()

    # plot measure
    ax.plot(dates, measure, label=title, marker='o', linestyle='None')

    # plot trend
    if is_variation:
        plot_trend(measure, dates, ax)

    # plot events as vertical lines
    ax.axvline(dates.index(date(2020, 9, 14).strftime("%b %d")), label='Riapertura scuole', linestyle='--', color='g')
    ax.axvline(dates.index(date(2020, 10, 24).strftime("%b %d")), label='DPCM 24 ottobre', linestyle='--', color='c')
    ax.axvline(dates.index(date(2020, 11, 3).strftime("%b %d")), label='DPCM 3 novembre', linestyle='--', color='m')

    # x axis properties
    dates_step = math.floor(len(dates)/(N_TICKS-1))
    ax.set_xticks(np.arange(0, len(dates), dates_step))
    ax.set_xticklabels(dates[0::dates_step])

    # other properties
    ax.set(title=title)
    ax.legend()

    n_figures += 1

    return


if __name__ == "__main__":
    # load data
    data_file_path = os.path.join('COVID-19', 'dati-json', 'dpc-covid19-ita-andamento-nazionale.json')

    with open(data_file_path, 'r') as data_file:
        national_data = json.load(data_file)
        
        dates_step = math.floor(len(national_data)/(N_TICKS-1))
        dates = []
        hospitalized_with_sympthoms = []
        intensive_care_unit = []
        staying_at_home = []
        positives = []
        healed = []
        deaths = []

        for daily_data in national_data:
            hospitalized_with_sympthoms.append(daily_data['ricoverati_con_sintomi'])
            intensive_care_unit.append(daily_data['terapia_intensiva'])
            staying_at_home.append(daily_data['isolamento_domiciliare'])
            positives.append(daily_data['totale_positivi'])
            healed.append(daily_data['dimessi_guariti'])
            deaths.append(daily_data['deceduti'])

            day = datetime.fromisoformat(daily_data['data'])
            dates.append(day.strftime("%b %d"))

        variation_hospitalized_with_sympthoms = np.diff(np.array(hospitalized_with_sympthoms))
        variation_intensive_care_unit = np.diff(np.array(intensive_care_unit))
        variation_staying_at_home = np.diff(np.array(staying_at_home))
        variation_positives = np.diff(np.array(positives))
        variation_healed = np.diff(np.array(healed))
        variation_deaths = np.diff(np.array(deaths))
        
        # print graph
        # plot_measure(hospitalized_with_sympthoms, dates, 'Ricoverati con sintomi')
        # plot_measure(intensive_care_unit, dates, 'Terapia intensiva')
        # plot_measure(staying_at_home, dates, 'Isolamento domiciliare')
        # plot_measure(positives, dates, 'Positivi')
        # plot_measure(healed, dates, 'Guariti')

        plot_measure(variation_hospitalized_with_sympthoms, dates[1:], 'Variazione ricoverati con sintomi', is_variation=True)
        plot_measure(variation_intensive_care_unit, dates[1:], 'Variazione terapia intensiva', is_variation=True)
        plot_measure(variation_staying_at_home, dates[1:], 'Variazione isolamento domiciliare', is_variation=True)
        plot_measure(variation_positives, dates[1:], 'Variazione positivi', is_variation=True)
        plot_measure(variation_healed, dates[1:], 'Variazione guariti', is_variation=True)
        plot_measure(variation_deaths, dates[1:], 'Variazione deceduti', is_variation=True)

        plt.show()

    exit(0)