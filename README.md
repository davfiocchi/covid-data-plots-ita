# COVID DATA PLOTS 

This repository contains a simple Python script to plot Italian COVID-19 data.  

The data is provided by Civil Protection Department (Dipartimento Protezione Civile) and can be found [here](https://github.com/pcm-dpc/COVID-19)

I made this script for me to have a better understanding of what the COVID situation is like in Italy.  
I hope that others will find it useful as well!  

The following day-by-day difference of measures are plotted:
* \# hospitalized with sympthoms
* \# intensive care unit
* \# staying at home
* \# positives
* \# healed
* \# deaths

When available, the area underneath the trend will be coloured:
* if national data, all three colours are shown. The height of each colour is proportional to the number of regions assigned to that colour 
* if regional data, the area will be coloured based on the region's colour for the period

### How do I get set up?

* Clone this repo
* Install requirements
  * Numpy lib [install instructions](https://numpy.org/install/)
  * Matplot lib [install instructions](https://matplotlib.org/users/installing.html#installing-an-official-release)
  * GitPython [install instructions](https://gitpython.readthedocs.io/en/stable/intro.html#installing-gitpython)
* Run the script  
  When no arguments are provided, national data will be shown
```
python ./make_graphs.py [<region1>] ... [<region N>]
```

### TODO
* automatic update of region colour data
* if more than one region is provided, display each measure them in a single plot (so you can compare region data easily)
* vaccine information display (not yet available on Civil Protection Department repo)
