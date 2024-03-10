# Fully Online Matching with Stochastic Arrivals and Departures

This repository is the official implementation of 'Fully Online Matching with Stochastic Arrivals and Departures'

## Requirements

All the code are based on Python 3 in Anaconda. 

###Install gurobi

```setup
conda install -c gurobi gurobi
```

If you cannot install by this command, see <https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python-> for help.
### Gurobi license
You need to get a license for gurobi (see <https://www.gurobi.com/academia/academic-program-and-licenses/>)

## Evaluation
###Experiments in Our paper
Run the code below. It will store the results that we tested in our paper in the directory "result/". 

```main
python main.py
```

Run the code below (in the "result/" directory), it will plot figures for the results generated. The figures are saved in "result/imgs/".

```plot
python plot.py
```
If there are no figures, you can check ``plot.py'' to ensure that the input file names are the same as the file names in 'result/'.

###Set your parameters
Run the code below to check you own parameter settings :

```eval
python eval.py
```

Use the command below to show the help message of eval.py:

```eval
python eval.py -h
```


