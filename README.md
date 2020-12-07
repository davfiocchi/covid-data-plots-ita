# COVID DATA PLOTS 

This repository contains a simple Python script to plot Italian COVID-19 data.  

The data is provided by Civil Protection Department (Dipartimento Protezione Civile) and can be found [here](https://github.com/pcm-dpc/COVID-19)

I made this script for me to have a better understanding of what is the COVID situation like in Italy.  
I hope that it might be useful also for others! 

### How do I get set up?

* Clone this repo
* Install requirements
  * Matplot lib [install instructions](https://matplotlib.org/users/installing.html#installing-an-official-release)
  * GitPython [install instructions](https://gitpython.readthedocs.io/en/stable/intro.html#installing-gitpython)
* Run the script
```
python ./make_graphs.py [<region1>] ... [<region N>]
```

### TODO
* plot events based on province
* color area under trend based on region zone colour (yellow, orange, red)
