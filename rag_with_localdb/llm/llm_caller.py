from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from embedding import embedding_pdf

def llm_caller_func(gpt_model,query):
    
    gpt_llm=ChatOpenAI(model=gpt_model)

    prompts_template=ChatPromptTemplate.from_messages([
        ("system","You an AI assistant that helps answer the user questions."),
        ("user","Input: {input}\n\n Context:{context}")
        ])

    output_parse=StrOutputParser()

    chain= ({"input": RunnablePassthrough(), "context":embedding_pdf.chroma_retriever} | prompts_template | gpt_llm | output_parse)
    response=chain.invoke(query)

    return response