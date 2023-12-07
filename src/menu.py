import streamlit as st
from streamlit_option_menu import option_menu
from decouple import config
import src.search_q as search_q
import src.data_sources as data_sources

def page():

    # CSS style definitions
    custom_css = f"""
    <style>
        [data-testid="stSidebarNav"]::before {{
            content: "JIRA EXPLORER";
            margin-left: 40px;
            font-size: 30px;
            position: relative;
            top: 50px;
            color: #8b8b8e;
        }}
        
        .st-emotion-cache-lrlib {{
            max-height: 100vh;
            list-style: none;
            overflow: overlay;
            margin: 0px;
            padding-top: 5rem;
            padding-bottom: 1rem;
        }}
        
        .stDeployButton {{
            visibility: hidden;
        }}
        footer {{
            visibility: hidden;
        }}
        
        .marks  {{
            width: 95%;
        }}
        
        # .st-emotion-cache-vk3wp9 {{
        #     background-color: white;
        # }}
        
        .st-emotion-cache-ztfqz8 {{
            visibility: hidden;
        }}
        
        [data-testid="stFileUploader"] {{
            width: 95%;
        }}
        
        [data-testid="stFileUploadDropzone"] {{
            background-color: #F0F0F0;
        }}
        
        .st-emotion-cache-1q7spjk {{
            width: 95%;
            color: black;
        }}     
                
    </style>
    """

    # Use the CSS in Streamlit
    st.markdown(custom_css, unsafe_allow_html=True)

    with st.sidebar:
        # CSS style definitions
        company_name = config('COMPANY_NAME')
        menu_selected = option_menu(None, [company_name, "Data Sources", 'Settings'],
                                    icons=['search', 'database-add', "gear"],
                                    menu_icon="cast", default_index=0, orientation="vertical",
                                    styles={
                                        "container": {"padding": "0!important", "background-color": "#fafafa"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": "#eee", "color": "black"},
                                        "nav-link-selected": {"background-color": "gray"},
                                    }
                                    )
    if menu_selected == company_name:
        return search_q.main()
    elif menu_selected == "Data Sources":
        return data_sources.main()
    elif menu_selected == "Settings":
        return st.write("Settings")
    else:
        return st.write("Error")


1
