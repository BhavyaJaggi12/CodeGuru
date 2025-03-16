import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.schema import Document 
from youtube_transcript_api import YouTubeTranscriptApi

## Streamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

## Get the Groq API Key and URL (YT or website) to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

## LLM Model Using Groq API
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    ## Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YouTube video URL or website URL")
    else:
        try:
            with st.spinner("Waiting..."):
                docs = []  # Initialize docs to prevent NameError
                
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    try:
                        # Extract video ID for both full and short URLs
                        if "youtube.com" in generic_url:
                            video_id = generic_url.split("v=")[-1].split("&")[0]  # Remove extra parameters
                        else:
                            video_id = generic_url.split("/")[-1]  # For short URLs like youtu.be/VIDEO_ID

                        # Fetch transcript
                        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)
                        text = " ".join([entry['text'] for entry in transcript])
                        docs = [Document(page_content=text)]
                    except Exception as yt_error:
                        st.error(f"Failed to fetch YouTube transcript: {yt_error}")
                        
                else:
                    try:
                        loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                       headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                                                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
                                                                "Safari/537.36"})
                        docs = loader.load()
                    except Exception as web_error:
                        st.error(f"Failed to load webpage: {web_error}")
                
                if docs:
                    ## Chain For Summarization
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain.run(docs)
                    st.success(output_summary)
                else:
                    st.error("No content available for summarization.")
        except Exception as e:
            st.exception(f"Exception: {e}")
