from decouple import config
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import time
from constants import CHROMA_SETTINGS
import streamlit as st


def main():
    # flags
    mute_stream = False
    hide_source = False

    # Loading configurations
    embeddings_model_name = config("EMBEDDINGS_MODEL_NAME")
    persist_directory = config('PERSIST_DIRECTORY')
    model_type = config('MODEL_TYPE')
    model_path = config('MODEL_PATH')
    model_n_ctx = config('MODEL_N_CTX')
    model_n_batch = int(config('MODEL_N_BATCH'))
    target_source_chunks = int(config('TARGET_SOURCE_CHUNKS'))

    # Parse the command line arguments
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS,
                client=chroma_client)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

    callbacks = [] if mute_stream else [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, max_tokens=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks,
                           verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gguf', n_batch=model_n_batch,
                          callbacks=callbacks, verbose=False)
        case _default:
            # raise exception if model_type is not supported
            raise Exception(
                f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")

    # def parse_arguments():
    #     parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
    #                                                  'using the power of LLMs.')
    #     parser.add_argument("--hide-source", "-S", action='store_true',
    #                         help='Use this flag to disable printing of source documents used for answers.')
    #
    #     parser.add_argument("--mute-stream", "-M",
    #                         action='store_true',
    #                         help='Use this flag to disable the streaming StdOut callback for LLMs.')
    #
    #     return parser.parse_args()

    st.title("💬 Article Q")
    st.caption("🚀 A streamlit chatbot powered by Virtu.GPT")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Your question?", key="article_q"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Start the response time
        start_time = time.time()

        # Get the answer from the chain
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                         return_source_documents=not hide_source)
        response = qa(prompt)
        msg = response["result"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # Start the response time
        end_time = time.time()

        # # Get Documents from chain
        # for document in response['source_documents']:
        #     # st.write(document.metadata["source"])
        #     # st.write(document.page_content)

        # Custom CSS to inject for prettier expander
        st.markdown("""
            <style>
            div.st-Expander > div:first-child {
                font-size: 16px;
                font-weight: bold;
                color: #0c6ef7;
                background-color: #e6f0ff;
                border-radius: 5px;
                padding: 5px 10px;
            }
            div.st-Expander > div:last-child {
                background-color: #f2f2f2;
                padding: 10px;
                border-radius: 5px;
                margin-top: 5px;
            }
            </style>
            """, unsafe_allow_html=True)

        # Display documents in expandable sections
        for i, document in enumerate(response['source_documents'], start=1):
            with st.expander(f"Document {i}: {document.metadata['source']}"):
                st.markdown("**Content:**\n" + document.page_content)