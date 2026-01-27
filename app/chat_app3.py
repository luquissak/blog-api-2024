import streamlit as st
import random
import time
import backend_chat
import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
import csv
from langchain_google_community import BigQueryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image
from langchain_core.messages import SystemMessage


load_dotenv()
assert "LANGSMITH_TRACING" in os.environ, "Please set the LANGSMITH_TRACING environment variable."
assert "LANGSMITH_API_KEY" in os.environ, "Please set the LANGSMITH_API_KEY environment variable."
assert "PROJECT_ID" in os.environ, "Please set the PROJECT_ID environment variable."
assert "LOCATION" in os.environ, "Please set the LOCATION environment variable."
assert "DATASET" in os.environ, "Please set the DATASET environment variable."
assert "TABLE" in os.environ, "Please set the TABLE environment variable."
PROJECT_ID = os.getenv("PROJECT_ID") 
LOCATION = os.getenv("LOCATION") 
DATASET = os.getenv("DATASET") 
TABLE = os.getenv("TABLE") 

PROJECT_ID = "llm-studies"
LOCATION = "us-central1"
DATASET = "blog_embeddings"
TABLE = "rag_embeddings_s_b" # s: simple, b: BQ

embeddings = VertexAIEmbeddings(model="textembedding-gecko@latest")

vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=LOCATION,
    embedding=embeddings,
)

llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}

# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}

tools = ToolNode([retrieve])

graph_builder = StateGraph(MessagesState)
graph_builder.add_node(query_or_respond)
graph_builder.add_node(tools)
graph_builder.add_node(generate)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile()


# Streamed response emulator
def response_generator(prompt):
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )

    print(f"PROMPT: {prompt.strip()}")
    response = graph.invoke(
        {"messages": [{"role": "user", "content": prompt}, {"role": "system", "content": "Você é um tutor de filosofia e deve trazer as respostas baseadas na teorias encontradas nos textos, sejam de autores ou termos"}]},
        stream_mode="values",
    )

    print(len(response.get('messages')))
    answer = response.get('messages')[len(response.get('messages')) - 1].content
    print(f"RESPONSE: {response.get('messages')[len(response.get('messages')) - 1].content}")

    for word in answer.split():
        yield word + " "
        time.sleep(0.05)


st.title("Deuso do Olimpo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Vamos filosofar?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})