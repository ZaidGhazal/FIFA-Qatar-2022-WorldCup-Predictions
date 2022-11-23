import pandas as pd
import numpy as np
from pickle import load

def remove_whitespaces(df: pd.DataFrame) -> None:
    """Remove whitespaces from column names and string values

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to clean
    """
    # Remove whitespace from each column name
    df.columns = df.columns.str.strip()
    
    # Remove whitespace from each string value
    categorical_columns = df.select_dtypes("O").columns
    for column in categorical_columns:
        df[column] = df[column].str.strip()

lookup_table = pd.read_csv("data/dataset/lookup_table.csv")
remove_whitespaces(lookup_table)

model = load(open('models/regression/AdaBoostRegressor.pkl', 'rb'))
encoder =load(open('models/encoders/countries_encoder.pkl', 'rb'))


def predict(data: pd.DataFrame) -> pd.DataFrame:
    """Make predictions using a trained model

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data to predict

    Returns
    -------
    pd.DataFrame
        Dataframe containing the predictions
    """
    
    # Encode categorical features
    data.loc[0, "1st_team"] = encoder.transform(np.array(data.loc[0, "1st_team"]).reshape(1,))
    data.loc[0, "2nd_team"] = encoder.transform(np.array(data.loc[0, "2nd_team"]).reshape(1,))
    
    # Make predictions

    predictions = model.predict(data)
    
    
    return predictions


def get_prediction(team_1, team_2):

    mask_1 = (lookup_table["1st_team"] == team_1) & (lookup_table["2nd_team"] == team_2)
    mask_2 = (lookup_table["1st_team"] == team_2) & (lookup_table["2nd_team"] == team_1)

    team_1_stats = lookup_table[mask_1]
    team_2_stats = lookup_table[mask_2]
    first_team = ""
    second_team = ""

    if not team_1_stats.empty:
        team_1_stats.reset_index(drop=True, inplace=True)
        first_team = team_1_stats.loc[0, "1st_team"]
        second_team = team_1_stats.loc[0, "2nd_team"]
        prediction = predict(team_1_stats)
        

    
    elif not team_2_stats.empty:
        team_2_stats.reset_index(drop=True, inplace=True)
        first_team = team_2_stats.loc[0, "1st_team"]
        second_team = team_2_stats.loc[0, "2nd_team"]
        prediction = predict(team_2_stats)
        
    else:
        prediction = np.nan
        raise ValueError("No match in the lookup table found")
    
    return (first_team, second_team, prediction[0])
 


if __name__ == "__main__":
    print(get_prediction("Japan", "Germany"))