import base64
import collections
import time
from pathlib import Path

import emoji
import flag
import streamlit as st
import streamlit.components.v1 as components


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(width, img_path):
    img_html = "<img width={}pt src='data:image/png;base64,{}' class='img-fluid'>".format(
        width, img_to_bytes(img_path)
    )
    return img_html


def add_bg_from_local(image_file):
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
    "England": flag.flag(":GB:"),
    "Iran": flag.flag(":IR:"),
    "USA": flag.flag(":US:"),
    "Wales": flag.flag(":GB:"),
    "Mexico": flag.flag(":MX:"),
    "Poland": flag.flag(":PL:"),
    "France": flag.flag(":FR:"),
    "Australia": flag.flag(":AU:"),
    "Denmark": flag.flag(":DK:"),
    "Tunisia": flag.flag(":TN:"),
    "Costa Rica": flag.flag(":CR:"),
    "Germany": flag.flag(":DE:"),
    "Japan": flag.flag(":JP:"),
    "South Korea": flag.flag(":KR:"),
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
            time.sleep(1)
            # TODO: Model CODE HERE
            
            result = country1
            difference = 2
            st.markdown(
                "<h2 style='text-align: center; color: white;'>The Winner 🏆</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h2 style='text-align: center; color: white;'>______________________</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h1 style='text-align: center; color: white;'>{result}</h1>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='text-align: center; color: white;'>By {difference} Goals Difference </h3>",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------------
#  st.image("app/assets/Asset_2.png", width=20)

# Footer container
# with st.container():
#     st.write('Made by [Your Name](https://www.linkedin.com/in/your-name/)')
#     st.write('Source code available on [GitHub]')


# Result container
# Display the final result
