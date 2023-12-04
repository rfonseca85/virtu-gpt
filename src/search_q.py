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
from streamlit_extras.stylable_container import stylable_container

# Flags
mute_stream = False
show_source = True


@st.cache_resource
def load_model():
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
    llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gguf', n_batch=model_n_batch,
                  callbacks=callbacks, verbose=False)

    # Get the answer from the chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                     return_source_documents=True)

    # match model_type:
    #     case "LlamaCpp":
    #         llm = LlamaCpp(model_path=model_path, max_tokens=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks,
    #                        verbose=False)
    #     case "GPT4All":
    #         llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gguf', n_batch=model_n_batch,
    #                       callbacks=callbacks, verbose=False)
    #     case _default:
    #         # raise exception if model_type is not supported
    #         raise Exception(
    #             f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")

    return qa


def main():
    qa = load_model()
    response = None

    with st.sidebar:
        st.title("Search configs")
        global show_source
        show_source = st.checkbox("Show source documents", value=True)

    st.title("💬 " + config('COMPANY_NAME') + " Q")
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

        with st.spinner('Wait for it...'):
            response = qa(prompt)
            msg = response["result"]
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

            # Start the response time
            end_time = time.time()

            if show_source:
                with stylable_container(
                        key="container_with_border1",
                        css_styles="""
                            {
                                border: 2px solid rgba(49, 51, 63, 0.2);
                                border-radius: 0.5rem;
                                padding: calc(1em - 1px);
                                background-color: #F0F0F0;
                            }
                            .stMarkdown {
                                color: #000000;
                            }
                            """,
                ):
                    st.caption("Search took - {:.2f} seconds".format(end_time - start_time))
                    for i, document in enumerate(response['source_documents'], start=0):
                        st.caption(f"**Document {i}: {document.metadata['source']}**")
                        st.caption("**Content:**\n" + document.page_content)
