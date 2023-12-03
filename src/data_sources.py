import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
import src.upload_docs as upload_docs


def main():
    # CSS style definitions
    data_source_model = option_menu(None, ["Upload", "Google Docs", 'Confluence'],
                                    icons=['cloud-upload', 'google', "book"],
                                    menu_icon="cast", default_index=0, orientation="horizontal",
                                    styles={
                                        "container": {"padding": "0!important", "background-color": "#fafafa"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": "#eee"},
                                        "nav-link-selected": {"background-color": "gray"},
                                    }
                                    )

    with stylable_container(
            key="container_with_border1",
            css_styles="""
                {
                    border: 2px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    background-color: #F0F0F0;
                }
                """,
    ):

        if data_source_model == "Upload":
            upload_docs.main()
        elif data_source_model == "Google Docs":
            st.write("Google Docs")
        elif data_source_model == "Confluence":
            st.write("Confluence")
