
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

from area_colour import get_area_colour, AreaColour

N_TICKS = 10
n_figures = 0


def plot_trend(measure, dates, area_colours, ax):
    """
    Plot trend
    
    The trend is calculated as mid point of two-weeks linear regression on measure (with 13 days overlapping)
    """
    trend = []
    trend_dates = []
    trend_index = 0
    area_colours_data = np.zeros((AreaColour.NONE.value+1, len(dates)-13))

    for index, day in enumerate(dates):
        # avoid first and last 7 days due to insufficient data
        if (index < 7 or index > len(dates)-7): continue

        model = np.polyfit(np.arange(0, 14), measure[index-7:index+7], 1)
        predict = np.poly1d(model)
        trend.append(predict(7))
        trend_dates.append(day)

        if type(area_colours[index]) is AreaColour:
            # Region plot:
            # The area underneath the trend shall be filled with the colour assigned to the region for that day
            if area_colours[index] is AreaColour.RED:
                area_colours_data[AreaColour.RED.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.ORANGE.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.YELLOW.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.NONE.value][trend_index] = trend[trend_index]
            elif area_colours[index] is AreaColour.ORANGE:
                area_colours_data[AreaColour.ORANGE.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.YELLOW.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.NONE.value][trend_index] = trend[trend_index]
            elif area_colours[index] is AreaColour.YELLOW:
                area_colours_data[AreaColour.YELLOW.value][trend_index] = trend[trend_index]
                area_colours_data[AreaColour.NONE.value][trend_index] = trend[trend_index]
            else:
                area_colours_data[AreaColour.NONE.value][trend_index] = trend[trend_index]
        else:
            # National plot:
            # The area underneath the trend shall be coloured with every colour in proportion to the number of regions assigned to that colour
            # Example: if half of the regions are marked as red on a specifc day, then half of the area underneath the trend will be filled with red on that day
            area_colours_data[AreaColour.RED.value][trend_index] = trend[trend_index]*area_colours[index][AreaColour.RED]
            area_colours_data[AreaColour.ORANGE.value][trend_index] = trend[trend_index]*area_colours[index][AreaColour.ORANGE] + area_colours_data[AreaColour.RED.value][trend_index]
            area_colours_data[AreaColour.YELLOW.value][trend_index] = trend[trend_index]*area_colours[index][AreaColour.YELLOW] + area_colours_data[AreaColour.ORANGE.value][trend_index]
            area_colours_data[AreaColour.NONE.value][trend_index] = trend[trend_index]*area_colours[index][AreaColour.NONE] + area_colours_data[AreaColour.YELLOW.value][trend_index]
        
        trend_index += 1

    ax.plot(trend_dates, trend, label='Andamento', color='r')

    ax.fill_between(trend_dates, area_colours_data[AreaColour.RED.value], 0, color='red', alpha=0.5)
    ax.fill_between(trend_dates, area_colours_data[AreaColour.ORANGE.value], area_colours_data[AreaColour.RED.value], color='orange', alpha=0.5)
    ax.fill_between(trend_dates, area_colours_data[AreaColour.YELLOW.value], area_colours_data[AreaColour.ORANGE.value], color='yellow', alpha=0.5)
    ax.fill_between(trend_dates, area_colours_data[AreaColour.NONE.value], area_colours_data[AreaColour.YELLOW.value], color='white')

    return


def plot_events(dates, ax):
    """
    Plot events
    
    Plot events as vertical lines
    """
    ax.axvline(dates.index(date(2020, 9, 14).strftime("%b %d")), label='Riapertura scuole', linestyle='--', color='g')
    ax.axvline(dates.index(date(2020, 10, 24).strftime("%b %d")), label='DPCM 24 ottobre', linestyle='--', color='c')
    ax.axvline(dates.index(date(2020, 11, 3).strftime("%b %d")), label='DPCM 3 novembre', linestyle='--', color='m')
    ax.axvline(dates.index(date(2020, 12, 21).strftime("%b %d")), label='Blocco regioni', linestyle='--', color='b')
    ax.axvline(dates.index(date(2020, 12, 25).strftime("%b %d")), label='Natale', linestyle='--', color='g')

    return


def plot_measure(measure, dates, title, area_colours=[], is_variation=False, notes=None):
    """
    Plot single measure
    
    Plot measure, define each plot style, plot trend, ...
    """
    global n_figures

    fig = plt.figure(n_figures)
    ax = fig.subplots()

    # convert date into suitable string format
    dates = [day.strftime("%b %d") for day in dates]

    # plot measure
    ax.plot(dates, measure, marker='o', linestyle='None')

    # plot trend
    if is_variation:
        plot_trend(measure, dates, area_colours, ax)

    # plot events
    plot_events(dates, ax)

    # plot notes, if any
    if notes:
        plt.figtext(0.5, 0.03, notes, fontsize=9, horizontalalignment='center', wrap=True)

    # x axis properties
    dates_step = math.floor(len(dates)/(N_TICKS-1))
    ax.set_xticks(np.arange(0, len(dates), dates_step))
    ax.set_xticklabels(dates[0::dates_step])

    # other properties
    ax.set(title=title)
    ax.legend()

    n_figures += 1

    return


def plot_all_measures(dates, hospitalized_with_sympthoms, intensive_care_unit, staying_at_home, positives, healed, deaths, n_tests, area_colours, area_name):
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
    variation_n_tests = np.where(variation_n_tests==0, 1, variation_n_tests)

    plot_measure(variation_hospitalized_with_sympthoms, dates[1:], 'Variazione ricoverati con sintomi - ' + area_name, area_colours[1:], is_variation=True)
    plot_measure(variation_intensive_care_unit, dates[1:], 'Variazione terapia intensiva - ' + area_name, area_colours[1:], is_variation=True)
    plot_measure(variation_staying_at_home, dates[1:], 'Variazione isolamento domiciliare - ' + area_name, area_colours[1:], is_variation=True)
    plot_measure(variation_positives, dates[1:], 'Variazione positivi - ' + area_name, area_colours[1:], is_variation=True)
    plot_measure(variation_healed, dates[1:], 'Variazione guariti - ' + area_name, area_colours[1:], is_variation=True)
    plot_measure(variation_deaths, dates[1:], 'Variazione deceduti - ' + area_name, area_colours[1:], is_variation=True)

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
    
    # set the maximum ratio to +-1
    ratio_positive_over_tests = np.where(ratio_positive_over_tests>1, 1, ratio_positive_over_tests)
    ratio_positive_over_tests = np.where(ratio_positive_over_tests<-1, -1, ratio_positive_over_tests)

    plot_measure(ratio_positive_over_tests, dates[1+n_days_to_wait_before_test_result:], 'Rapporto positivi/numero tamponi - ' + area_name, area_colours[1:], is_variation=True, notes='Il rapporto è stato calcolato assumendo che il risultato del tampone arrivasse '+ str(n_days_to_wait_before_test_result) +' giorno/i dopo il test. \nL\'assunzione è forte e poco affidabile, serve solo per mostrare un grafico dell\'andamento')

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

            dates.append(datetime.fromisoformat(daily_data['data']).date())
        
        area_colours = get_area_colour(dates)

        plot_all_measures(dates=dates,
                          hospitalized_with_sympthoms=hospitalized_with_sympthoms, 
                          intensive_care_unit=intensive_care_unit,
                          staying_at_home=staying_at_home,
                          positives=positives,
                          healed=healed,
                          deaths=deaths,
                          n_tests=n_tests,
                          area_colours=area_colours,
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

                region_dict[region]['dates'].append(datetime.fromisoformat(daily_data['data']).date())
        
        
        for region in region_dict.keys():

            if len(region_dict[region]['dates']) == 0:
                print("Invalid region: ", region)
                continue

            area_colours = get_area_colour(region_dict[region]['dates'], region)

            plot_all_measures(dates=region_dict[region]['dates'],
                            hospitalized_with_sympthoms=region_dict[region]['hospitalized_with_sympthoms'],
                            intensive_care_unit=region_dict[region]['intensive_care_unit'],
                            staying_at_home=region_dict[region]['staying_at_home'],
                            positives=region_dict[region]['positives'],
                            healed=region_dict[region]['healed'],
                            deaths=region_dict[region]['deaths'],
                            n_tests=region_dict[region]['n_tests'],
                            area_colours=area_colours,
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