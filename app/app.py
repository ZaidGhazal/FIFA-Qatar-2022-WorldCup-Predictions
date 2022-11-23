import streamlit as st
import collections
import streamlit.components.v1 as components
import time 
import base64
from pathlib import Path
import emoji

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(width, img_path):
    img_html = "<img width={}pt src='data:image/png;base64,{}' class='img-fluid'>".format(
    width,
      img_to_bytes(img_path)
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
    unsafe_allow_html=True
    )

st.set_page_config(
    page_title="FIFA22 Winner Predictor",
    page_icon=emoji.emojize(":trophy:"),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/zaid-ghazal/',
        'Report a bug': "https://www.linkedin.com/in/zaid-ghazal/",
        'About': "## This is an AI-based winner predictor for FIFA22 World Cup matches!" +
        "\n" + "**@Done by [Zaid Ghazal](https://www.linkedin.com/in/zaid-ghazal/) & [Ali Albustami](https://www.linkedin.com/in/alibustami/)**"
    }
)

add_bg_from_local('app/assets/Asset_5.png')  
# Title container
with st.container():
    st.markdown("<p style='text-align: center; color: grey;'>"+img_to_html("500",'app/assets/Asset_1.png')+"</p>", unsafe_allow_html=True)
    # st.image("app/assets/Asset_1.png", width=500)
    # st.empty().text(" ")

    
    # st.title('FIFA 2022 World Cup ⚽ Match Winner Predictor 🏆')

# Challenge container
flags_dict = {
    'Argentina': emoji.emojize(":flag_ar:"),
    'Portugal': emoji.emojize(":flag_pt:"),
    'Ecuador': emoji.emojize(":flag_ec:"),
    'Netherlands': emoji.emojize(":flag_nl:"),
    'Brazil': emoji.emojize(":flag_br:"),
    'England': emoji.emojize(":flag_gb:"),
    'Iran': emoji.emojize(":flag_ir:"),
    'USA': emoji.emojize(":flag_us:"),
    'Wales': emoji.emojize(":flag_gb:"),
    'Mexico': emoji.emojize(":flag_mx:"),
    'Poland': emoji.emojize(":flag_pl:"),
    'France': emoji.emojize(":flag_fr:"),
    'Australia': emoji.emojize(":flag_au:"),
    'Denmark': emoji.emojize(":flag_dk:"),
    'Tunisia': emoji.emojize(":flag_tn:"),
    'Costa Rica': emoji.emojize(":flag_cr:"),
    'Germany': emoji.emojize(":flag_de:"),
    'Japan': emoji.emojize(":flag_jp:"),
    'South Korea': emoji.emojize(":flag_kr:"),
    'Croatia': emoji.emojize(":flag_hr:"),
    'Canada': emoji.emojize(":flag_ca:"),
    'Morocco': emoji.emojize(":flag_ma:"),
    'Serbia': emoji.emojize(":flag_rs:"),
    'Switzerland': emoji.emojize(":flag_ch:"),
    'Cameroon': emoji.emojize(":flag_cm:"),
    'Ghana': emoji.emojize(":flag_gh:"),
    'Uruguay': emoji.emojize(":flag_uy:"),
    'Saudi Arabia': emoji.emojize(":flag_sa:"),
    'Senegal': emoji.emojize(":flag_sn:"),
    'Spain': emoji.emojize(":flag_es:"),
    'Qatar': emoji.emojize(":flag_qa:"),
    'Belgium': emoji.emojize(":flag_be:"),
}
teams_flags_ls = [team + " " + flag for team, flag in flags_dict.items()]
teams_flags_ls.insert(0, "Select Team")
flags_dict = collections.OrderedDict(sorted(flags_dict.items()))

# ------------------------------------------------------------------------
with st.container():
    # components.html("""<p style="color:white width:150pt;">Insert Match</p>""")
    st.markdown("<h2 style='text-align: left; color: white;'>Insert Match</h2>", unsafe_allow_html=True)
# Drop lists and display flage
    col1, col2, col3 = st.columns(3)
    with col1:

       
        country1 = st.selectbox("",options=teams_flags_ls, label_visibility="collapsed")
    with col2:
        components.html(
            """
                <div style="text-align: center; font-size: 30px; font-weight: bold; margin-top: 1px;color: white;">VS</div>
                """,
        )
    with col3:
        country2 = st.selectbox( " ",options=teams_flags_ls, label_visibility="collapsed")

# st.empty().text(" ")
# st.empty().text(" ")

# ------------------------------------------------------------------------
# Prediction container
with st.container():

    if country1 == teams_flags_ls[0]:
        pass
    elif country1 == country2 and country1 != teams_flags_ls[0]:
        st.warning(f'{emoji.emojize(":thikink_face:")} Please Select Different Teams')
    elif country2 != teams_flags_ls[0] and country1 != teams_flags_ls[0]:
        with st.spinner(""):
            time.sleep(1)
            # TODO: Model CODE HERE
            result = country1
            difference = 2
            # st.markdown("<h2 style='text-align: center; color: white;'>" +"The Winner "+img_to_html("15",'app/assets/Asset_2.png')+ "</h2>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: white;'>The Winner 🏆</h2>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: white;'>______________________</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: white;'>{result}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>By {difference} Goals Difference </h3>", unsafe_allow_html=True)
       
# ------------------------------------------------------------------------
#  st.image("app/assets/Asset_2.png", width=20)

# Footer container
# with st.container():
#     st.write('Made by [Your Name](https://www.linkedin.com/in/your-name/)')
#     st.write('Source code available on [GitHub]')


# Result container
# Display the final result
