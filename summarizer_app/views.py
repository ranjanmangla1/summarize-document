# summarizer_app/views.py
from django.shortcuts import render
from .forms import DocumentForm
from PyPDF2 import PdfReader  # Updated import
from docx import Document as DocxDocument


# summarizer_app/summarizer.py
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain




def extract_text(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(docx_file_path):
    doc = DocxDocument(docx_file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text



def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def summarize_pdf(raw_text):
    load_dotenv()

    # raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)

    response = conversation_chain({'question': "summarize this document"})
    chat_history = response['chat_history']

    summary = ""
    for i, message in enumerate(chat_history):
        if i == 1:
            summary += message.content + "\n"

    return summary.strip()





# def upload_file(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save()

#             if document.file.name.endswith('.pdf'):
#                 raw_text = extract_text(document.file.path)
#                 text = summarize_pdf(raw_text)
#             elif document.file.name.endswith('.docx'):
#                 raw_text = extract_text_from_docx(document.file.path)
#                 text = summarize_pdf(raw_text)
#             else:
#                 text = "Sorry, this file format is an Unsupported file format. Only pdf & doc"

#             return render(request, 'summarizer_app/result.html', {'text': text})
#     else:
#         form = DocumentForm()

#     return render(request, 'summarizer_app/upload.html', {'form': form})


# def upload_file(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save()

#             if document.file.name.endswith('.pdf'):
#                 raw_text = extract_text(document.file.path)
#                 text = summarize_pdf(raw_text)
#             elif document.file.name.endswith('.docx'):
#                 raw_text = extract_text_from_docx(document.file.path)
#                 text = summarize_pdf(raw_text)
#             else:
#                 text = "Sorry, this file format is an Unsupported file format. Only pdf & doc"

#             return render(request, 'summarizer_app/upload.html', {'form': form, 'text': text})
#     else:
#         form = DocumentForm()

#     return render(request, 'summarizer_app/upload.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()

            if document.file.name.endswith('.pdf'):
                raw_text = extract_text(document.file.path)
                text = summarize_pdf(raw_text)
            elif document.file.name.endswith('.docx'):
                raw_text = extract_text_from_docx(document.file.path)
                text = summarize_pdf(raw_text)
            else:
                text = "Sorry, this file format is an unsupported file format. Only pdf & doc"

            return render(request, 'summarizer_app/upload.html', {'form': form, 'text': text})
    else:
        form = DocumentForm()

    return render(request, 'summarizer_app/upload.html', {'form': form})