import os
from pickle import load
from typing import Iterable, Tuple, Union

import numpy as np
import pandas as pd


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

reg_models_list: list = []
for regressor in os.listdir("models/regression"):
    if regressor.endswith(".pkl"):
        temp_model = load(
            open(os.path.join("models/regression", regressor), "rb")
        )
        reg_models_list.append(temp_model)

encoder = load(open("models/encoders/countries_encoder.pkl", "rb"))

cls_models_list: list = []
for classifier in os.listdir("models/classification"):
    if classifier.endswith(".pkl") and not classifier.startswith("XGB"):
        cls_model = load(
            open(os.path.join("models/classification", classifier), "rb")
        )
        cls_models_list.append(cls_model)
# cls_model = load(open("models/classification/LogisticRegression.pkl", "rb"))


def reg_predict(data: pd.DataFrame) -> pd.DataFrame:
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
    data.loc[0, "1st_team"] = encoder.transform(
        np.array(data.loc[0, "1st_team"]).reshape(
            1,
        )
    )
    data.loc[0, "2nd_team"] = encoder.transform(
        np.array(data.loc[0, "2nd_team"]).reshape(
            1,
        )
    )

    # Make predictions

    predictions_list: list = []
    for model in reg_models_list:
        predictions_list.append(model.predict(data))

    prediction = np.mean(predictions_list)

    return prediction


def get_prediction_reg(team_1: str, team_2: str):
    mask_1 = (lookup_table["1st_team"] == team_1) & (
        lookup_table["2nd_team"] == team_2
    )
    mask_2 = (lookup_table["1st_team"] == team_2) & (
        lookup_table["2nd_team"] == team_1
    )

    team_1_stats = lookup_table[mask_1]
    team_2_stats = lookup_table[mask_2]
    first_team = ""
    second_team = ""

    if not team_1_stats.empty:
        team_1_stats.reset_index(drop=True, inplace=True)
        first_team = team_1_stats.loc[0, "1st_team"]
        second_team = team_1_stats.loc[0, "2nd_team"]
        prediction = reg_predict(team_1_stats)

    elif not team_2_stats.empty:
        team_2_stats.reset_index(drop=True, inplace=True)
        first_team = team_2_stats.loc[0, "1st_team"]
        second_team = team_2_stats.loc[0, "2nd_team"]
        prediction = reg_predict(team_2_stats)

    else:
        prediction = np.nan
        raise ValueError("No match in the lookup table found")

    return (first_team, second_team, prediction)


def cls_predict(data: pd.DataFrame) -> Tuple[Iterable[float]]:
    """Make predictions using a trained model

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data to predict

    Returns
    -------
    Tuple[Iterable[float]]
        Tuple containing the predictions

    """

    # Encode categorical features
    data.loc[0, "1st_team"] = encoder.transform(
        np.array(data.loc[0, "1st_team"]).reshape(
            1,
        )
    )
    data.loc[0, "2nd_team"] = encoder.transform(
        np.array(data.loc[0, "2nd_team"]).reshape(
            1,
        )
    )

    # Make predictions
    # probs = cls_model.predict_proba(data)[0]
    probs_list: list = []
    for model in cls_models_list:
        probs_list.append(model.predict_proba(data)[0])

    probs = np.mean(probs_list, axis=0)

    team_1_winning_prob = np.round(probs[1], 3) * 100
    team_2_winning_prob = np.round(probs[2], 3) * 100
    draw_prob = np.round(probs[0], 3) * 100

    return (team_1_winning_prob, team_2_winning_prob, draw_prob)


def get_prediction_cls(
    team_1: str, team_2: str
) -> Tuple[Iterable[Union[str, float]]]:
    """Get prediction for a match

    Parameters
    ----------
    team_1 : str
        Name of the first team
    team_2 : str
        Name of the second team

    Returns
    -------
    Tuple[Iterable[Union[str, float]]]
        Tuple containing the name of the first team, the name of the second team and the prediction

    Raises
    ------
    ValueError
        If no match in the lookup table is found
    """

    mask_1 = (lookup_table["1st_team"] == team_1) & (
        lookup_table["2nd_team"] == team_2
    )
    mask_2 = (lookup_table["1st_team"] == team_2) & (
        lookup_table["2nd_team"] == team_1
    )

    team_1_stats = lookup_table[mask_1]
    team_2_stats = lookup_table[mask_2]
    first_team = ""
    second_team = ""

    if not team_1_stats.empty:
        team_1_stats.reset_index(drop=True, inplace=True)
        first_team = team_1_stats.loc[0, "1st_team"]
        second_team = team_1_stats.loc[0, "2nd_team"]
        team_1_winning_prob, team_2_winning_prob, draw_prob = cls_predict(
            team_1_stats
        )

    elif not team_2_stats.empty:
        team_2_stats.reset_index(drop=True, inplace=True)
        first_team = team_2_stats.loc[0, "1st_team"]
        second_team = team_2_stats.loc[0, "2nd_team"]
        team_1_winning_prob, team_2_winning_prob, draw_prob = cls_predict(
            team_2_stats
        )

    else:
        team_1_winning_prob = np.nan
        team_2_winning_prob = np.nan
        draw_prob = np.nan
        raise ValueError("No match in the lookup table found")

    print(
        first_team,
        second_team,
        team_1_winning_prob,
        team_2_winning_prob,
        draw_prob,
    )
    return (
        first_team,
        second_team,
        team_1_winning_prob,
        team_2_winning_prob,
        draw_prob,
    )


if __name__ == "__main__":
    print(get_prediction_cls("Japan", "Germany"))
