import bs4 
import os 
from langchain_community.document_loaders import WebBaseLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser 
from langchain_groq import ChatGroq   
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv
import re 
from chromadb.config import Settings 

load_dotenv()  

# Initialize the User Agent.

os.environ["USER_AGENT"] = "dd"



def get_the_content_into_splitted_document():
    
    # Ist Website for worldwise information.
    bs4_strainer = bs4.SoupStrainer(class_=("app"))
    loader = WebBaseLoader(
        web_paths = ("https://www.bbc.com/news",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs1 = loader.load()
    #print(docs1)

    #t the Technology based news.
    bs4_strainer = bs4.SoupStrainer(class_=("wp-site-blocks"))
    loader = WebBaseLoader(
        web_paths = ("https://techcrunch.com/",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs2 = loader.load()
    #print(docs2)

    # Get the Technology based news.
    bs4_strainer = bs4.SoupStrainer(class_=("wp-site-blocks"))
    loader = WebBaseLoader(
        web_paths = ("https://techcrunch.com/category/artificial-intelligence/",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs3 = loader.load()
    #print(docs3)

    # Get the Technology based news.
    bs4_strainer = bs4.SoupStrainer(id=("app-root"))
    loader = WebBaseLoader(
        web_paths = ("https://www.wired.com/category/business/",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs4 = loader.load()
    #print(docs4)

    # Get the Technology based news.
    bs4_strainer = bs4.SoupStrainer(class_=("container--homepage-wrapper"))
    loader = WebBaseLoader(
        web_paths = ("https://www.aljazeera.com/",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs5 = loader.load()
    #print(docs5)

    # Get the Technology based news.
    bs4_strainer = bs4.SoupStrainer( class_=("BaseWrap-sc-gjQpdd RowWrapper-UmqTg iUEiRd HEhan RecircListExtendedOverlayWrapper-fTTpDF eyvUKs ContentFooterRelated-kEBiFe kVUuwq extended-overlay"))
    loader = WebBaseLoader(
        web_paths = ("https://www.wired.com/story/the-ai-fueled-future-of-work-needs-humans-more-than-ever/",),
        bs_kwargs={"parse_only" : bs4_strainer}
    )

    # Get the Documents.
    docs6 = loader.load()
    #print(docs6)

    # Combine all documents
    main_docs = [docs1, docs2, docs3, docs4, docs5, docs6]
    main_docs = sum(main_docs, [])  # Flatten into single list

    # Verify total number of Document objects
    #print(f"✅ Total documents combined: {len(main_docs)}")

    # Clean each document (remove \n)
    for doc in main_docs:
        doc.page_content = doc.page_content.replace("\n", "")
        doc.page_content = doc.page_content.replace("\t","")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=12000,
        chunk_overlap=100,
        add_start_index=True
    )

    all_splits = text_splitter.split_documents(main_docs)

    # Verify the result
    #print(f"✅ Total splits created: {len(all_splits)}")
    #print(all_splits[:1])  # Print a sample splits
    
    return all_splits 


def get_the_embeedings(all_splits):
    local_embeddings = OllamaEmbeddings(model="all-minilm:33m")

    # ✅ Chroma settings with persist directory
    settings = Settings(
        persist_directory="my_chroma_store",  # you can name this folder anything
        anonymized_telemetry=False
    )

    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=local_embeddings,
        collection_name="news_collection",  # koi bhi naam chalega
        client_settings=settings
    )

    return vectorstore


def fetch_related_documents(question):
    all_splits = get_the_content_into_splitted_document()
    vectorstore = get_the_embeedings(all_splits) 
    retriver = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2})
    retrived_docs = retriver.invoke(question)
    return retrived_docs


prompt = PromptTemplate(
        input_variables = ["context","user_question"] , 
        template = """
        Answer the user_question according to the given context given very briefly 
        
        Response Generation Approach:
        1. First analyze the context , ok
        2. Then you have to answer the users question in a way as fetch the keyword form the user_question about which company mainly user is askeing ok.
        3. After analyzing the context you will definately understand that the context has not only covered a single news it put lost of news within himself.
        4. Then what you have to do then is only that, I will suggest you the output format

          ---Output Format---
          Generate output in a dictionery python dictionery format first put the company name , then put the Articles as a Key, and put Title , Summary , Semtiment of the particular Summary and the key Topics covered in it as a nested dictionery.
          And put generally two Articles and at most 3 articles you have to do the same. 
          - Comparitive Score Sentiment in which cover Sentimet Distribution in which you have to check the Positive , Negative and Neutral Sentiment for articles.
          - Coverage Differences generate them cover "Comparision , impact they have to be for all the articles.
          - Get the Topic Overlap in which cover Common Topics , Unique Topics in Article 1 and so on for each article.
          - Final Sentiment Analysis in which write content for it, in the Hindi language as of the summary of the above summarized content which has to be bried and include all the above geenerated response summary in the hindi langhaue ok. 
        Context : {context} , 
        user_question : {user_question}
        """
)

llm = ChatGroq( model= "deepseek-r1-distill-qwen-32b" , api_key = os.getenv("api_key") )


def get_response_from_ai_model(retrived_docs , question):
    context = " ".join([doc.page_content for doc in retrived_docs])
    chain = prompt | llm | StrOutputParser() 
    response = chain.invoke({"context" : context , "user_question" : question}) 
    return response 





def remove_think_tags(text):
    # Remove all <think>...</think> tags and their content
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def extract_python_code(text):
    # Match content between ```python and ```
    return re.sub(r"```python(.*?)```", lambda m: m.group(1).strip(), text, flags=re.DOTALL)




def get_answer(question):
    retrived_documents = fetch_related_documents(question)
    response = get_response_from_ai_model(retrived_documents , question)
    print(response)
    response = remove_think_tags(response) 
    response = extract_python_code(response)
    return response   





my_response = get_answer("Tell me about Tesla?")
print(my_response) 