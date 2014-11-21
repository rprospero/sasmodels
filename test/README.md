# Develop

Developers tests. To be used when migrating from the old models to the new models.

Main file:

```
utest.py
```

Test can be launched typing:
```
cd test 
python develop/utest.py
````

**Note:**

- Random tests are not working as the parameters low and high limit appear to be to large for some models.
- Also random numbers are generated with ```random.uniform``` which outputs floats. This also must be checked!

**Dummy files to be deleted**

- ```test/develop/test.py```
- ```test/develop/helper/tmp.py```


**Parameters file:**

File: ```test/develop/helper/defs_pd.csv```:

Desription:

| Field | Description |
|------------|----------------------|
| model_old | SasView model name |
| model_new | New model name  |
| param_old | SasView parameter name |
| param_new | new parameter name |
| value | default parameter value |
| low | low limit for parameter value (for generating random values) |
| high | high limit for parameter value (for generating random values) |
| qmax | Qmax for generating Q data |
| cutoff | CutOff when evaluating the model (just for new models) |
| dtype | Single or double presition when evaluating the new models |
| n_sasview | Number of iterations to evaluate Sasview model |
| n_opencl | Number of iterations to evaluate the new model |
| rel_error_1d | Relative error limit between the new and the old model for 1D data |
| rel_error_2d | Relative error limit between the new and the old model for 2D data |

