
import csv
from datetime import datetime, timedelta
from enum import Enum

ALL_AREAS = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Lombardia", "Piemonte", "P.A. Bolzano", "Toscana", "Valle d'Aosta", "Emilia-Romagna",  "Friuli Venezia Giulia", "Lazio", "Liguria", "Marche", "Molise", "P.A. Trento", "Puglia", "Sardegna", "Sicilia", "Umbria", "Veneto"]


class AreaColour(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    WHITE = 4
    NONE = 5


class ColourPeriod:
    """
    Colour period class

    This class contains information about areas colour for a specific period of time
    """
    def __init__(self, start_date, end_date=datetime.now().date(), red_areas=[], orange_areas=[], yellow_areas=[], white_areas=[]):
        """
        Class constructor

        Parameters
        ----------
        start_date : Date
            Start date for the colour period
        end_date : Date
            End date for the colour period (default to now)
        red_areas : list of str
            List of all the area names maked as red for the period
        orange_areas : list of str
            List of all the area names maked as orange for the period
        yellow_areas : list of str
            List of all the area names maked as yellow for the period
        white_areas : list of str
            List of all the area names maked as white for the period
        """
        self.start_date = start_date
        self.end_date = end_date
        self.red_areas = red_areas
        self.orange_areas = orange_areas
        self.yellow_areas = yellow_areas
        self.white_areas = white_areas

    def __str__(self):
        col_period_string = "Start date: " + self.start_date.isoformat() + "\n"
        col_period_string += "End date: " + self.end_date.isoformat() + "\n"
        col_period_string += "Red areas: " + str(self.red_areas) + "\n"
        col_period_string += "Orange areas: " + str(self.orange_areas) + "\n"
        col_period_string += "Yellow areas: " + str(self.yellow_areas) + "\n"
        col_period_string += "White areas: " + str(self.white_areas) + "\n"
        
        return col_period_string

    def set_end_date(self, next_period_start_date):
        """
        Set the end date of the actual colour period using the next period start date

        Parameters
        ----------
        next_period_start_date : Date
            Start date for the next period
        """
        self.end_date = next_period_start_date - timedelta(1)
    
    def contains_duplicates(self):
        """
        Check if more than one colour is assigned to a single area

        Returns
        ----------
        True if more than one colour is assigned to a area
        False otherwise 
        """
        all_areas = self.red_areas + self.orange_areas + self.yellow_areas + self.white_areas

        if len(all_areas) == len(set(all_areas)):
            return False
        else:
            print(len(all_areas))
            print(len(set(all_areas)))
            print(all_areas)
            print(set(all_areas))
            return True

    def every_area_has_colour_assigned(self):
        """
        Check if all the areas have been assigned to a colour

        Returns
        ----------
        True if all the area has been assigned to a colour
        False otherwise 
        """
        areas_assigned_to_colour = self.red_areas + self.orange_areas + self.yellow_areas + self.white_areas

        for area in ALL_AREAS:
            if area not in areas_assigned_to_colour:
                print("No colour has been assigned to " + area)
                return False

        return True
    
    def is_date_before_start(self, date):
        """
        Check if the date is before start date of the period

        Parameters
        ----------
        date : Date
            Input date to check

        Returns
        ----------
        True if the date is before start date
        False otherwise 
        """
        return date < self.start_date

    def is_date_after_end(self, date):
        """
        Check if the date is after end date of the period

        Parameters
        ----------
        date : Date
            Input date to check

        Returns
        ----------
        True if the date is after end date
        False otherwise 
        """
        return date > self.end_date

    def get_colour(self, date, area=None):
        """
        Get the colour for the given area for this period.
        If the area is not provided, the percentage of each colour is provided

        Parameters
        ----------
        date : Date
            Date (needed to check if the date is valid)
        area : str
            Desired area (default to all)

        Returns
        ----------
        AreaColour
            Area colour if the area is provided 
            If the date is not valid or the area hasn't been found then AreaColour.NONE is returned
        obj
            If the area is not provided the following object is returned
            {
                AreaColour.RED = <value_r>,
                AreaColour.ORANGE = <value_o>,
                AreaColour.YELLOW = <value_y>,
                AreaColour.WHITE = <value_w>,
                AreaColour.NONE = <value_n>,
            }
            Where each value is a number between 0 and 1
        """
        while True:

            # date check
            if self.is_date_before_start(date) or self.is_date_after_end(date):
                break

            # all data
            if area is None:
                return {
                    AreaColour.RED: len(self.red_areas)/len(ALL_AREAS),
                    AreaColour.ORANGE: len(self.orange_areas)/len(ALL_AREAS),
                    AreaColour.YELLOW: len(self.yellow_areas)/len(ALL_AREAS),
                    AreaColour.WHITE: len(self.white_areas)/len(ALL_AREAS),
                    AreaColour.NONE: 0,
                }

            # specific area data
            else:
                if area in self.red_areas:
                    return AreaColour.RED
                elif area in self.orange_areas:
                    return AreaColour.ORANGE
                elif area in self.yellow_areas:
                    return AreaColour.YELLOW
                elif area in self.white_areas:
                    return AreaColour.WHITE
                else:
                    print(f"The area {area} hasn't been found")
                    break
        
        # return with errors
        if area is None:
            return {
                AreaColour.RED: 0,
                AreaColour.ORANGE: 0,
                AreaColour.YELLOW: 0,
                AreaColour.WHITE: 0,
                AreaColour.NONE: 1,
            }
        else:
            return AreaColour.NONE

def load_data():
    """
    Load data from file

    Internal function to convert the file content to Python structures

    Returns
    -------
    list
        list of ColourPeriod instances
    """
    loaded_data = []

    with open('area_colour.csv') as csv_file:
        file_content = csv.reader(csv_file, delimiter=',')

        for row_index, row in enumerate(file_content):

            if row_index > 0:

                # retrieve data from row
                red_areas = list(filter(None, row[1].split(', ')))
                orange_areas = list(filter(None, row[2].split(', ')))
                yellow_areas = list(filter(None, row[3].split(', ')))
                white_areas = list(filter(None, row[4].split(', ')))

                start_date = datetime.fromisoformat(row[0]).date()

                # define a new colour period
                loaded_data.append(ColourPeriod(start_date=start_date,
                                               red_areas=red_areas,
                                               orange_areas=orange_areas,
                                               yellow_areas=yellow_areas,
                                               white_areas=white_areas))
                
                # update end date for previous colour period
                if len(loaded_data) > 1:
                    loaded_data[-2].set_end_date(start_date)

    return loaded_data


def validate_data():
    """
    Validate data
    
    Checks that the file content is consistent and does not contain errors (such as duplicates, ...).

    This is needed since the file that contains the colour information of the area has been created and updated manually, thus an automated check is needed.
    Once the area colour could be retrieved from the Civil Protection Department repository, then this function might be helpful to find any errors in their files.
    Hopefully the automatic retrieval from Civil Protection Department repository would be available soon!
    """
    area_colour_data = load_data()

    all_data_is_ok = True

    for period in area_colour_data:

        there_is_some_error = False

        if period.contains_duplicates():
            print("The following colour period has more than one colour assigned to a area")
            there_is_some_error = True

        if not period.every_area_has_colour_assigned():
            print("Not all the area has a colour assigned in the following colour period")
            there_is_some_error = True
        
        if there_is_some_error:
            all_data_is_ok = False
            print(period)

    if all_data_is_ok:
        print("Data is correct!")

    return True


def get_area_colour(dates, area=None):
    """
    Get area colour for all the input dates 
    
    Parameters
    ----------
    dates : list of Date
        List of dates for which the area colour is requested
    area : str
        Desired area (default to all)

    Returns
    ----------
    list
        List of AreaColours or obj if all the areas have been requested (return value of get_colour function for each ColourPeriod class)
    """
    colour_data = load_data()
    colour_data_index = 0

    area_colours = []

    for date in dates:

        if colour_data[colour_data_index].is_date_after_end(date) and colour_data_index < len(colour_data):
            colour_data_index += 1

        area_colours.append(colour_data[colour_data_index].get_colour(date, area))

    return area_colours

if __name__ == "__main__":
    validate_data()

    exit(0)