from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from sys import argv
import os

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class ResearchAssitant(object):

    def __init__(self, researcher_name, model_name='deepseek-r1:1.5b'):
       
        self.researcher_name = researcher_name
        self.model_name = model_name
        
        # 1. Create the model
        self.llm = Ollama(model=model_name)
        self.embeddings = OllamaEmbeddings(model=model_name)

        # 2. 
        self.paper_dir = f'./tools/papers/{researcher_name}/'

        # 3. Prompt
        # 3. Create the prompt template
        template = """
        Answer the questions based on the context provided.
        
        Context: {context}

        question: {question}
        
        """
        self.prompt = PromptTemplate.from_template(template)

        # 4. knowledge base
        self.db = {}

    def start_analysis(self, year_begin=None, year_end=None): 
        paper_list = os.listdir(self.paper_dir)
        if year_begin and year_end:
            paper_list = list(filter(lambda x: int(x[1:5]) <= year_end and int(x[1:5]) >= year_begin, paper_list))

        # 1. Load the PDF file and create a retriever to be used for providing context
        for paper_name in paper_list:
            filepath = os.path.join(self.paper_dir, paper_name)
            loader = PyPDFLoader(filepath)
            pages = loader.load_and_split()
            store = DocArrayInMemorySearch.from_documents(pages, embedding=self.embeddings)
            retriever = store.as_retriever()

            print(f'Analyzing paper = {paper_name}')
            # 4. Build the chain of operations
            chain = (
                {
                    'context': retriever | format_docs,
                    'question': RunnablePassthrough(),
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
            )
            question = """
            1. What is the topic and key problem does this paper study?
            2. What kind of method does it use to study?
            3. What will the author study next?
            4. Give three new ideas that related to this topic
            """
            output = chain.invoke({'question': question})
            print(output)
            self.db[paper_name] = output

    
    def summarize(self):
        print(self.db)


