
import csv
from datetime import datetime, timedelta


class ColourPeriod:
    """
    Colour period class

    This class contains information about regions colour for a specific period of time
    """
    def __init__(self, start_date, end_date=datetime.now(), red_regions=[], orange_regions=[], yellow_regions=[]):
        """
        Class constructor

        Parameters
        ----------
        start_date : Date
            Start date for the colour period
        end_date : Date
            End date for the colour period (default to now)
        red_regions : list of str
            List of all the region names maked as red for the period
        orange_regions : list of str
            List of all the region names maked as orange for the period
        yellow_regions : list of str
            List of all the region names maked as yellow for the period
        """
        self.start_date = start_date
        self.end_date = end_date
        self.red_regions = red_regions
        self.orange_regions = orange_regions
        self.yellow_regions = yellow_regions

    def __str__(self):
        col_period_string = "Start date: " + self.start_date.isoformat() + "\n"
        col_period_string += "End date: " + self.end_date.isoformat() + "\n"
        col_period_string += "Red regions: " + str(self.red_regions) + "\n"
        col_period_string += "Orange regions: " + str(self.orange_regions) + "\n"
        col_period_string += "Yellow regions: " + str(self.yellow_regions) + "\n"
        
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
        Check if more than one colour is assigned to a single region

        Returns
        ----------
        True if more than one colour is assigned to a region
        False otherwise 
        """
        all_regions = self.red_regions + self.orange_regions + self.yellow_regions

        if len(all_regions) == len(set(all_regions)):
            return False
        else:
            print(len(all_regions))
            print(len(set(all_regions)))
            print(all_regions)
            print(set(all_regions))
            return True

    def every_region_has_colour_assigned(self):
        """
        Check if all the regions have been assigned to a colour

        Returns
        ----------
        True if all the region has been assigned to a colour
        False otherwise 
        """
        all_regions = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Lombardia", "Piemonte", "Provincia Autonoma di Bolzano", "Toscana", "Valle d'Aosta", "Emilia Romagna",  "Friuli Venezia Giulia", "Lazio", "Liguria", "Marche", "Molise", "Provincia autonoma di Trento", "Puglia", "Sardegna", "Sicilia", "Umbria", "Veneto"]

        regions_assigned_to_colour = self.red_regions + self.orange_regions + self.yellow_regions

        for region in all_regions:
            if region not in regions_assigned_to_colour:
                print("No colour has been assigned to " + region)
                return False

        return True


def load_data():
    """
    Load data from file

    Function to convert the file content to Python structures

    Returns
    -------
    list
        list of ColourPeriod instances
    """
    loaded_data = []

    with open('region_colour.csv') as csv_file:
        file_content = csv.reader(csv_file, delimiter=',')

        for row_index, row in enumerate(file_content):

            if row_index > 0:

                # retrieve data from row
                red_regions = list(filter(None, row[1].split(', ')))
                orange_regions = list(filter(None, row[2].split(', ')))
                yellow_regions = list(filter(None, row[3].split(', ')))

                start_date = datetime.fromisoformat(row[0])

                # define a new colour period
                loaded_data.append(ColourPeriod(start_date=start_date,
                                               red_regions=red_regions,
                                               orange_regions=orange_regions,
                                               yellow_regions=yellow_regions))
                
                # update end date for previous colour period
                if len(loaded_data) > 1:
                    loaded_data[-2].set_end_date(start_date)

    return loaded_data


def validate_data():
    """
    Validate data
    
    Checks that the file content is consistent and does not contain errors (such as duplicates, ...).

    This is needed since the file that contains the colour information of the region has been created and updated manually, thus an automated check is needed.
    Once the region colour could be retrieved from the Civil Protection Department repository, then this function might be helpful to find any errors in their files.
    Hopefully the automatic retrieval from Civil Protection Department repository would be available soon!
    """
    region_colour_data = load_data()

    all_data_is_ok = True

    for period in region_colour_data:

        there_is_some_error = False

        if period.contains_duplicates():
            print("The following colour period has more than one colour assigned to a region")
            there_is_some_error = True

        if not period.every_region_has_colour_assigned():
            print("Not all the region has a colour assigned in the following colour period")
            there_is_some_error = True
        
        if there_is_some_error:
            all_data_is_ok = False
            print(period)

    if all_data_is_ok:
        print("Data is correct!")

    return True



if __name__ == "__main__":
    validate_data()

    exit(0)