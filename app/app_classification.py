import base64
import collections
import sys
import time
from pathlib import Path

import emoji
import flag
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from prediction_functions import get_prediction_binary_cls

sys.path.insert(0, "")


def img_to_bytes(img_path: str) -> str:
    """Converts an image file to bytes.

    Parameters
    ----------
    img_path : str
        Path to the image file.

    Returns
    -------
    str
        Bytes of the image file.
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(width: int, img_path: str) -> str:
    """Converts an image file to HTML.

    Parameters
    ----------
    width : int
        Width of the image.
    img_path : str
        Path to the image file.

    Returns
    -------
    str
        HTML format of the image.
    """
    img_html = "<img width={}pt src='data:image/png;base64,{}' class='img-fluid'>".format(
        width, img_to_bytes(img_path)
    )
    return img_html


def add_bg_from_local(image_file) -> None:
    """Adds a background image to the Streamlit app.

    Parameters
    ----------
    image_file : str
        Path to the image file.
    """

    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
        # background-opacity: 0.6;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="FIFA22 Winner Predictor",
    page_icon=emoji.emojize(":trophy:"),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.linkedin.com/in/zaid-ghazal/",
        "Report a bug": "https://www.linkedin.com/in/zaid-ghazal/",
        "About": "## This is an AI-based winner predictor for FIFA22 World Cup matches!"
        + "\n"
        + "**@Done by [Zaid Ghazal](https://www.linkedin.com/in/zaid-ghazal/) & [Ali Albustami](https://www.linkedin.com/in/alibustami/)**",
    },
)

add_bg_from_local("app/assets/Asset_5.png")
# Title container
with st.container():
    st.markdown(
        "<p style='text-align: center; color: grey;'>"
        + img_to_html("50%", "app/assets/Asset_1.png")
        + "</p>",
        unsafe_allow_html=True,
    )


# Challenge container
flags_dict = {
    "Argentina": flag.flag(":AR:"),
    "Portugal": flag.flag(":PT:"),
    "Ecuador": flag.flag(":EC:"),
    "Netherlands": flag.flag(":NL:"),
    "Brazil": flag.flag(":BR:"),
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Iran": flag.flag(":IR:"),
    "United States": flag.flag(":US:"),
    "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Mexico": flag.flag(":MX:"),
    "Poland": flag.flag(":PL:"),
    "France": flag.flag(":FR:"),
    "Australia": flag.flag(":AU:"),
    "Denmark": flag.flag(":DK:"),
    "Tunisia": flag.flag(":TN:"),
    "Costa Rica": flag.flag(":CR:"),
    "Germany": flag.flag(":DE:"),
    "Japan": flag.flag(":JP:"),
    "Korea Republic": flag.flag(":KR:"),
    "Croatia": flag.flag(":HR:"),
    "Canada": flag.flag(":CA:"),
    "Morocco": flag.flag(":MA:"),
    "Serbia": flag.flag(":RS:"),
    "Switzerland": flag.flag(":CH:"),
    "Cameroon": flag.flag(":CM:"),
    "Ghana": flag.flag(":GH:"),
    "Uruguay": flag.flag(":UY:"),
    "Saudi Arabia": flag.flag(":SA:"),
    "Senegal": flag.flag(":SN:"),
    "Spain": flag.flag(":ES:"),
    "Qatar": flag.flag(":QA:"),
    "Belgium": flag.flag(":BE:"),
}
teams_flags_ls = [team + " " + flag for team, flag in flags_dict.items()]
teams_flags_ls.insert(0, "Select Team")
flags_dict = collections.OrderedDict(sorted(flags_dict.items()))

with st.container():
    st.markdown(
        "<h2 style='text-align: left; color: white;'>Insert Match</h2>",
        unsafe_allow_html=True,
    )
    # Drop lists and display flage
    col1, col2, col3 = st.columns(3)
    with col1:

        country1 = st.selectbox(
            "", options=teams_flags_ls, label_visibility="collapsed"
        )
    with col2:
        components.html(
            """
                <div style="text-align: center; font-size: 30px; font-weight: bold; margin-top: 1px;color: white;">VS</div>
                """,
            height=50,
        )
    with col3:
        country2 = st.selectbox(
            " ", options=teams_flags_ls, label_visibility="collapsed"
        )


# Prediction container
with st.container():

    if country1 == teams_flags_ls[0]:
        pass
    elif country1 == country2 and country1 != teams_flags_ls[0]:
        st.warning(
            f'{emoji.emojize(":thinking_face:")} Please Select Different Teams'
        )
    elif country2 != teams_flags_ls[0] and country1 != teams_flags_ls[0]:
        with st.spinner(""):
            time.sleep(3)
            print(country1, country2)
            prediction = get_prediction_binary_cls(
                country1.rsplit(" ", 1)[0], country2.rsplit(" ", 1)[0]
            )
            team_1 = prediction[0]
            team_2 = prediction[1]
            team_1_winning_prob = round(prediction[2], 3)
            team_2_prob_winning_prob = round(prediction[3], 3)

            sorted_results = {
                team_1: team_1_winning_prob,
                team_2: team_2_prob_winning_prob,
            }
            sorted_results = {
                k: v
                for k, v in sorted(
                    sorted_results.items(), key=lambda item: item[1]
                )
            }

            flag_first = (
                flags_dict.get(list(sorted_results.keys())[1])
                if flags_dict.get(list(sorted_results.keys())[1]) is not None
                else ""
            )
            flag_second = (
                flags_dict.get(list(sorted_results.keys())[0])
                if flags_dict.get(list(sorted_results.keys())[0]) is not None
                else ""
            )

            name_first = (
                list(sorted_results.keys())[1]
                if list(sorted_results.keys())[1] is not None
                else "Draw"
            )
            name_second = (
                list(sorted_results.keys())[0]
                if list(sorted_results.keys())[0] is not None
                else "Draw"
            )

            prob_first = list(sorted_results.values())[1]
            prob_second = list(sorted_results.values())[0]

            st.markdown(
                "<h2 style='text-align: center; color: white;'>Winning Chances 🏆</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h2 style='text-align: center; color: white;'>______________________</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h1 style='text-align: center; color: white;'>{name_first} {flag_first}: {prob_first}%</h1>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h1 style='text-align: center; color: white;'>{name_second} {flag_second}: {prob_second}%</h1>",
                unsafe_allow_html=True,
            )
