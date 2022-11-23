import pandas as pd
import numpy as np
from pickle import load

model = load(open('../models/regression/Lasso.pkl', 'rb'))
encoder =load(open('../models/encoders/countries_encoder.pkl', 'rb'))
def 