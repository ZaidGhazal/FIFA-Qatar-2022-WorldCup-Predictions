import streamlit as st
import collections
import streamlit.components.v1 as components
st.set_page_config(
    page_title="FIFA22 Winner Predictor",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/zaid-ghazal/',
        'Report a bug': "https://www.linkedin.com/in/zaid-ghazal/",
        'About': "## This is an AI-based winner predictor for FIFA22 World Cup matches!" +
        "\n" + "**@Done by [Zaid Ghazal](https://www.linkedin.com/in/zaid-ghazal/) & [Ali Albustami](https://www.linkedin.com/in/alibustami/)**"
    }
)

# Title container
with st.container():
    st.title('FIFA 2022 World Cup ⚽ Match Winner Predictor 🏆')

# Challenge container
flags_dict = {
    'Argentina': '🇦🇷',
    'Portugal': '🇵🇹',
    'Ecuador': '🇪🇨',
    'Netherlands': '🇳🇱',
    'Brazil': '🇧🇷',
    'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'Iran': '🇮🇷',
    'USA': '🇺🇸',
    'Wales': '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    'Mexico': '🇲🇽',
    'Poland': '🇵🇱',
    'France': '🇫🇷',
    'Australia': '🇦🇺',
    'Denmark': '🇩🇰',
    'Tunisia': '🇹🇳',
    'Costa Rica': '🇨🇷',
    'Germany': '🇩🇪',
    'Japan': '🇯🇵',
    'South Korea': '🇰🇷',
    'Croatia': '🇭🇷',
    'Canada': '🇨🇦',
    'Morocco': '🇲🇦',
    'Serbia': '🇷🇸',
    'Switzerland': '🇨🇭',
    'Cameroon': '🇨🇲',
    'Ghana': '🇬🇭',
    'Uruguay': '🇺🇾',
    'Saudi Arabia': '🇸🇦',
    'Senegal': '🇸🇳',
    'Spain': '🇪🇸',
    'Qatar': '🇶🇦',
    'Belgium': '🇧🇪',
}
teams_flags_ls = [team + " " + flag for team, flag in flags_dict.items()]
teams_flags_ls.insert(0, "Select Team")
flags_dict = collections.OrderedDict(sorted(flags_dict.items()))

# ------------------------------------------------------------------------
with st.container():
    st.header('Insert Match')
# Drop lists and display flage
    col1, col2, col3 = st.columns(3)
    with col1:
        country1 = st.selectbox('Select **1st Team**', teams_flags_ls)
    with col2:
        components.html(
            """
                <div style="text-align: center; font-size: 30px; font-weight: bold; margin-top: 10px;">VS</div>
                """,
        )
    with col3:
        country2 = st.selectbox('Select **2nd Team**', teams_flags_ls)

st.empty().text(" ")
st.empty().text(" ")

# ------------------------------------------------------------------------
# Prediction container
with st.container():

    if country1 == teams_flags_ls[0]:
        pass
    elif country1 == country2 and country1 != teams_flags_ls[0]:
        st.warning('🤔 Please Select Different Teams')
    else:
        # TODO: Model CODE HERE
        pass

# Footer container
# with st.container():
#     st.write('Made by [Your Name](https://www.linkedin.com/in/your-name/)')
#     st.write('Source code available on [GitHub]')


# Result container
# Display the final result
