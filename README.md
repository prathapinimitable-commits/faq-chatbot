\#  University FAQ Chatbot (RAG-based)



This is a Retrieval-Augmented Generation (RAG) based FAQ chatbot built using FAISS, Sentence Transformers, and Streamlit.



The chatbot answers user queries about university details such as courses, fees, admission process, and facilities.



\---



\##  Features



\* Semantic search using FAISS

\* Sentence embeddings using Sentence Transformers

\* Chat-style UI with Streamlit

\* Dual mode support:



&#x20;  - Demo mode (no external dependencies - only FAISS retrieval)

&#x20;  - Local LLM mode using Ollama (optional "full AI" - need to install Ollama locally)



\---



\##  How it works



1\. FAQ data is converted into vector embeddings

2\. User query is also converted into embedding

3\. FAISS retrieves the most similar answers

4\. Retrieved context is used to generate a response



\---



\##  Demo



Deployed app: https://faq--chatbot.streamlit.app/           [  It may take 2 mins to load the page & resources while trying for first time]

###  Try these questions:
- What courses are available?
- What is the fee for B.Tech?
- What is the duration of MBA?
- Is hostel accommodation available??
- Are scholarships available?



\---



\##  Installation (Local)



```bash

git clone https://github.com/prathapinimitable-commits/faq-chatbot

cd faq-chatbot

pip install -r requirements.txt

streamlit run app.py

```



\---



\##  Optional: Enable Local AI (Ollama)



Install Ollama and run:



```bash

ollama run llama3

```



Then start app with:



```bash

set USE\_LOCAL\_LLM=true

streamlit run app.py

```



\---



\##  Tech Stack



\* Python

\* Streamlit

\* FAISS

\* Sentence Transformers

\* Ollama (optional)



\---



\##  Use Case



This project demonstrates how to build a lightweight FAQ chatbot using RAG architecture without relying on paid APIs.



\---



\## 📌 Note



The deployed version runs in demo mode (without local LLM) for simplicity. Full AI responses can be tested locally using Ollama.



\---



