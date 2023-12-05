import streamlit as st
import scripts.ingest_utils as ingest
import tempfile
import os


def main():
    # Streamlit app code
    uploaded_file = st.file_uploader("Upload Source Document")
    # uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True)

    if uploaded_file is not None:
        st.caption("You have uploaded the following PDF:")
        st.caption(uploaded_file.name)

        with st.spinner('Uploading docs...'):
            # Create a temporary file to store the uploaded PDF
            temp_file = tempfile.NamedTemporaryFile(suffix=".whatever")
            temp_file.write(uploaded_file.getvalue())

            # Get the name of the uploaded PDF
            new_temp_file = os.path.dirname(temp_file.name) + '/' + uploaded_file.name
            os.rename(temp_file.name, new_temp_file)

            # Ingest the PDF
            ingest.vector_documents(new_temp_file)

            # Deleting the temporary PDF
            os.remove(new_temp_file)
