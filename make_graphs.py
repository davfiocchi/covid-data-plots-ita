
import json
import os
import sys
from datetime import datetime, date
import math
import git

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


def plot_events(dates, ax):
    """
    Plot events
    
    Plot events as vertical lines
    """
    ax.axvline(dates.index(date(2020, 9, 14).strftime("%b %d")), label='Riapertura scuole', linestyle='--', color='g')
    ax.axvline(dates.index(date(2020, 10, 24).strftime("%b %d")), label='DPCM 24 ottobre', linestyle='--', color='c')
    ax.axvline(dates.index(date(2020, 11, 3).strftime("%b %d")), label='DPCM 3 novembre', linestyle='--', color='m')

    return


def plot_measure(measure, dates, title, is_variation=False):
    """
    Plot single measure
    
    Plot measure, define each plot style, plot trend, ...
    """
    global n_figures

    fig = plt.figure(n_figures)
    ax = fig.subplots()

    # plot measure
    ax.plot(dates, measure, marker='o', linestyle='None')

    # plot trend
    if is_variation:
        plot_trend(measure, dates, ax)

    # plot events
    plot_events(dates, ax)

    # x axis properties
    dates_step = math.floor(len(dates)/(N_TICKS-1))
    ax.set_xticks(np.arange(0, len(dates), dates_step))
    ax.set_xticklabels(dates[0::dates_step])

    # other properties
    ax.set(title=title)
    ax.legend()

    n_figures += 1

    return


def plot_all_measures(dates, hospitalized_with_sympthoms, intensive_care_unit, staying_at_home, positives, healed, deaths, n_tests, area_name):
    """
    Plot all measures
    
    Derive and plot data for all measures
    """
    variation_hospitalized_with_sympthoms = np.diff(np.array(hospitalized_with_sympthoms))
    variation_intensive_care_unit = np.diff(np.array(intensive_care_unit))
    variation_staying_at_home = np.diff(np.array(staying_at_home))
    variation_positives = np.diff(np.array(positives))
    variation_healed = np.diff(np.array(healed))
    variation_deaths = np.diff(np.array(deaths))
    variation_n_tests = np.diff(np.array(n_tests))

    plot_measure(variation_hospitalized_with_sympthoms, dates[1:], 'Variazione ricoverati con sintomi - ' + area_name, is_variation=True)
    plot_measure(variation_intensive_care_unit, dates[1:], 'Variazione terapia intensiva - ' + area_name, is_variation=True)
    plot_measure(variation_staying_at_home, dates[1:], 'Variazione isolamento domiciliare - ' + area_name, is_variation=True)
    plot_measure(variation_positives, dates[1:], 'Variazione positivi - ' + area_name, is_variation=True)
    plot_measure(variation_healed, dates[1:], 'Variazione guariti - ' + area_name, is_variation=True)
    plot_measure(variation_deaths, dates[1:], 'Variazione deceduti - ' + area_name, is_variation=True)

    # we assume that one day after the test the result is ready
    # this is needed to best match the number of tests with the number of positives (but it is not reliable)
    n_days_to_wait_before_test_result = 1
    ratio_positive_over_tests = variation_positives[n_days_to_wait_before_test_result:]/variation_n_tests[:-n_days_to_wait_before_test_result]

    # check if the assumption leads to impossible result (ratio>1)
    if np.any(ratio_positive_over_tests > 1):

        print(n_days_to_wait_before_test_result, "day(s) to wait before test result leads to an impossible ratio. Trying with higher number of days...")

        # try every number of days up to 5
        for n_days_to_wait_before_test_result in range(2, 6):
            print("Evaluating", n_days_to_wait_before_test_result, "...")
            ratio_positive_over_tests = variation_positives[n_days_to_wait_before_test_result:]/variation_n_tests[:-n_days_to_wait_before_test_result]

            if np.any(ratio_positive_over_tests > 1) and n_days_to_wait_before_test_result<5 :
                print("Impossible ratio, continue")
                continue

            elif np.any(ratio_positive_over_tests > 1):
                print("Impossible ratio. Any number of days leads to impossible result. Fallback to 1 number of days")
                n_days_to_wait_before_test_result = 1
                ratio_positive_over_tests = variation_positives[n_days_to_wait_before_test_result:]/variation_n_tests[:-n_days_to_wait_before_test_result]
                break

            else:
                print("Possible number of days found")

                break
    
    plot_measure(ratio_positive_over_tests, dates[1+n_days_to_wait_before_test_result:], 'Rapporto positivi/numero tamponi - ' + area_name, is_variation=True)

    return


def plot_national_data():
    """
    Plot national data
    
    Loads and plot national data
    """
    data_file_path = os.path.join('COVID-19', 'dati-json', 'dpc-covid19-ita-andamento-nazionale.json')

    with open(data_file_path, 'r') as data_file:
        national_data = json.load(data_file)
        
        dates = []
        hospitalized_with_sympthoms = []
        intensive_care_unit = []
        staying_at_home = []
        positives = []
        healed = []
        deaths = []
        n_tests = []

        for daily_data in national_data:
            hospitalized_with_sympthoms.append(daily_data['ricoverati_con_sintomi'])
            intensive_care_unit.append(daily_data['terapia_intensiva'])
            staying_at_home.append(daily_data['isolamento_domiciliare'])
            positives.append(daily_data['totale_positivi'])
            healed.append(daily_data['dimessi_guariti'])
            deaths.append(daily_data['deceduti'])
            n_tests.append(daily_data['tamponi'])

            day = datetime.fromisoformat(daily_data['data'])
            dates.append(day.strftime("%b %d"))
        
        plot_all_measures(dates=dates,
                          hospitalized_with_sympthoms=hospitalized_with_sympthoms, 
                          intensive_care_unit=intensive_care_unit,
                          staying_at_home=staying_at_home,
                          positives=positives,
                          healed=healed,
                          deaths=deaths,
                          n_tests=n_tests,
                          area_name='Italia')
    
    return


def plot_regional_data(region_list):
    """
    Plot regional data

    Loads and plot data for each region in region_list
    """
    region_dict = {}

    for region_province in region_list:
        region_dict[region_province] = {
            "dates": [],
            "hospitalized_with_sympthoms": [],
            "intensive_care_unit": [],
            "staying_at_home": [],
            "positives": [],
            "healed": [],
            "deaths": [],
            "n_tests": []
        }
    
    # load data
    data_file_path = os.path.join('COVID-19', 'dati-json', 'dpc-covid19-ita-regioni.json')

    with open(data_file_path, 'r') as data_file:
        national_data = json.load(data_file)

        for daily_data in national_data:
            region = daily_data['denominazione_regione']
            if region in region_dict:
                region_dict[region]['hospitalized_with_sympthoms'].append(daily_data['ricoverati_con_sintomi'])
                region_dict[region]['intensive_care_unit'].append(daily_data['terapia_intensiva'])
                region_dict[region]['staying_at_home'].append(daily_data['isolamento_domiciliare'])
                region_dict[region]['positives'].append(daily_data['totale_positivi'])
                region_dict[region]['healed'].append(daily_data['dimessi_guariti'])
                region_dict[region]['deaths'].append(daily_data['deceduti'])
                region_dict[region]['n_tests'].append(daily_data['tamponi'])

                day = datetime.fromisoformat(daily_data['data'])
                region_dict[region]['dates'].append(day.strftime("%b %d"))
        
        
        for region in region_dict.keys():

            if len(region_dict[region]['dates']) == 0:
                print("Invalid region: ", region)
                continue

            plot_all_measures(dates=region_dict[region]['dates'],
                            hospitalized_with_sympthoms=region_dict[region]['hospitalized_with_sympthoms'],
                            intensive_care_unit=region_dict[region]['intensive_care_unit'],
                            staying_at_home=region_dict[region]['staying_at_home'],
                            positives=region_dict[region]['positives'],
                            healed=region_dict[region]['healed'],
                            deaths=region_dict[region]['deaths'],
                            n_tests=region_dict[region]['n_tests'],
                            area_name=region)
    
    return

if __name__ == "__main__":

    # update or clone data
    if os.path.isdir('COVID-19'):

        g = git.cmd.Git('COVID-19')

        print("Updating data...")

        ret = g.fetch()
        if ret != '': g.pull()

        print("Data up-to-date!")

    else:
        print("Cloning data from https://github.com/pcm-dpc/COVID-19.git (it takes several minutes) ...")

        g = git.cmd.Git('./')
        g.clone('--depth=1', 'https://github.com/pcm-dpc/COVID-19.git')

        print("Cloning done!")


    if len(sys.argv) > 1:
        plot_regional_data(sys.argv[1:])

    else:
        plot_national_data()

    plt.show()

    exit(0)