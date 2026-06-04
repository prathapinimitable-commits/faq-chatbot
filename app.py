import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# -----------------------------
# CONFIG
# -----------------------------
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false") == "true"

# -----------------------------
# LOAD EMBEDDING MODEL (cached)
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# -----------------------------
# FAQ DATA
# -----------------------------
faq_data = [
    "Admission process is online through the university portal.",
    "Fees for B.Tech is 1 lakh per year.",
    "Course duration for B.Tech is 4 years.",
    "MBA course duration is 2 years.",
    "MBA course fee is 30,000 per year.",
    "Fees for MBBS is 5 lakhs per year.",
    "Course duration for MBBS is 5.5 years.",
    "Contact us at 9876543210.",
    "Hostel facilities are available for all students.",
    "Scholarships are available based on merit.",
]

# -----------------------------
# CREATE FAISS INDEX (cached)
# -----------------------------
@st.cache_resource
def create_index(data):
    embeddings = model.encode(data)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, embeddings

index, embeddings = create_index(faq_data)

# -----------------------------
# SAFE OLLAMA IMPORT
# -----------------------------
ollama_available = False
if USE_LOCAL_LLM:
    try:
        import ollama
        ollama_available = True
    except:
        ollama_available = False

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("University FAQ Chatbot")

# Sidebar with sample questions
with st.sidebar:
    st.header("Example Questions")
    st.markdown("""
**Try these questions:**

- What courses are available?
- What is the fee for B.Tech?
- What is the duration of MBA?
- Is hostel accommodation available?
- Are scholarships available?

!! For AI response, install Ollama-Llama3 locally as mentioned in README.md file
""")

#st.write("DEBUG:", USE_LOCAL_LLM, ollama_available)  to check if LLM and ollama works

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
query = st.chat_input("Ask your question...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    # -----------------------------
    # RETRIEVAL (FAISS)
    # -----------------------------
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=3)

    results = [faq_data[i] for i in I[0]]
    context = " ".join(results)

    # -----------------------------
    # RESPONSE GENERATION
    # -----------------------------
    if USE_LOCAL_LLM and ollama_available:
        try:
            prompt = f"""
You are a helpful university assistant.

Answer ONLY from the context below.

Context:
{context}

Question: {query}

Answer:
"""
            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response["message"]["content"]

        except:
            # fallback if ollama fails
            answer = f"Based on available information: {context}"

    else:
        # demo mode (safe)
        answer = f"Based on available information: {context}"

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
