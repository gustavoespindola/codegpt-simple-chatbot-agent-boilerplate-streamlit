# Description: This is a simple chatbot that uses the CodeGPT Agent to respond to user input.
# Original code from: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import json
import requests
import time
import streamlit as st

# Variables (delete this section and sidebar if you are using environment variables)
codegpt_selected_agent_id = ''
if 'agents_list' not in st.session_state:
  st.session_state['agents_list'] = []
if 'selected_agent_id' not in st.session_state:
  st.session_state['selected_agent'] = []
if 'codegpt_api_key' not in st.session_state:
  st.session_state['codegpt_api_key'] = st.secrets.codegpt_api_key if st.secrets.codegpt_api_key else ''

# Set the URL for the CodeGPT Agent API
get_agent_url = f"https://playground.judini.ai/api/v1/agent"
agent_response_url = f"https://playground.judini.ai/api/v1/agent/"

#Keys:
# Read API Key and Agent ID from STREAMLIT environment variables
# More info: https://docs.streamlit.io/library/advanced-features/secrets-management
# To set environment variables, create a folder called .streamlit
# Inside, create a file called secrets.toml with the following contents:
# codegpt_api_key=my-api-key
# codegpt_agent_id=my-agent-id

#OR:

# Get API Key and Agent ID from URL query parameters
# get_codegpt_api_key=st.experimental_get_query_params().get("codegpt_api_key", None)
# get_codegpt_agent_id=st.experimental_get_query_params().get("codegpt_agent_id", None)
# 86d58c5f-d247-479c-bd1e-69f767d2e3f8

# This function gets the CodeGPT API key from the environment variable
# Or from the URL query parameter. For example -> http://localhost:8501/?codegpt_api_key=&codegpt_agent_id=
# codegpt_api_key=get_codegpt_api_key[0] if get_codegpt_api_key != None else st.secrets.codegpt_api_key
# codegpt_agent_id=get_codegpt_agent_id[0] if get_codegpt_agent_id != None else st.secrets.codegpt_agent_id

# Set page metadata config
st.set_page_config(
  page_title="CodeGPT Agent Boilerplate",
  page_icon="✨",
  menu_items={
      'Get Help': 'https://codegpt.co',
      'Report a bug': "https://codegpt.co",
      'About': "This is a simple chatbot boilerplate with memory that uses the CodeGPT Agent API"
  }
)


# Set request headers
headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Authorization": f"Bearer {st.session_state['codegpt_api_key']}"
}
#

# The function getAgents() gets the list of agents from the CodeGPT API.
def getAgents():
  get_agents = requests.get(get_agent_url, headers=headers)

  if get_agents.status_code != 200:
    st.session_state['agents_list'] = []
    print(f"Error getting agents: {get_agents.status_code} - {get_agents.text}")
  else:
    st.session_state['agents_list'] = get_agents.json()

# The function send_message() sends a message to the CodeGPT Agent.
# The function expects a boolean argument memory, which defaults to True. For default, CodeGPT API Agent remember 10 messages in memory.
# If memory is True, send_message() sends the entire conversation history to the agent.
# If memory is False, send_message() sends only the most recent message to the agent.
# The function returns the HTTP response from the agent.

def send_message(memory: bool = True) -> None:
  # Create a dictionary to hold the conversation messages.
  if memory:
    data = { "messages": [] }
    # Add each message to the messages dictionary.
    for message in st.session_state.messages:
      data["messages"].append(message)
  else:
    data = { "messages": [ st.session_state.messages[-1] ] }
  # Send the messages to the agent.
  try:
    return requests.post(agent_response_url + st.session_state['selected_agent']['id'], headers=headers, stream=True, json=data)
  # If there's an error sending the message, print the error message.
  except Exception as e:
    print(f"Error sending message: {e}")
    return None
#


# Streamlit UI | Sidebar

# creates a input to save the CodeGPT API Key
if st.session_state['codegpt_api_key'] == '':
  st.session_state['codegpt_api_key'] = st.sidebar.text_input("CodeGPT API Key", placeholder="Enter your CodeGPT API Key")
else:
  st.session_state['codegpt_api_key'] = st.sidebar.text_input("CodeGPT API Key", value=st.session_state['codegpt_api_key'], placeholder="Enter your CodeGPT API Key")


if st.sidebar.button("Get Agents"):
  getAgents()

st.sidebar.divider()

# creates a selectbox to save the agent id
st.session_state["selected_agent"] = st.sidebar.selectbox(
  'Select an agent',
  help='Select an agent from your CodeGPT account',
  options=st.session_state['agents_list'],
  format_func=lambda agent: agent['name']
)
if st.session_state['agents_list']:
  st.sidebar.success('This is a success message!', icon="✅")
#


# Main | Chat
st.title(":sparkles: CodeGPT Agent")
st.subheader(f"A simple chatbot boilerplate that uses the CodeGPT Agent to respond to user input.")

if st.session_state["selected_agent"]:
  st.write('Chat with:', st.session_state['selected_agent']["name"])

#
# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    try:
      st.markdown(message["content"])
    except:
      pass

# Accept user input
if prompt := st.chat_input("Type a message..."):
  # Add user message to the list of messages
  st.session_state.messages.append({"role": "user", "content": prompt})
  # Display the user message in the chat widget
  with st.chat_message("user"):
    st.markdown(prompt)

  # Display assistant response in chat message container
  with st.chat_message("assistant"):
    # Create a placeholder to display assistant response
    message_placeholder = st.empty()
    # Create a variable to store the full response
    full_response = ""
    # Call the send_message() function to get the assistant response
    assistant_response = send_message()

    # It then waits for a response from the assistant and displays the result.
    # If the assistant returns a "finished" event, it closes the connection and exits.
    # If the assistant returns a "continue" event, it keeps listening for more results.

    for chunk in assistant_response.iter_content(chunk_size=1024):
      if chunk:
        raw_data = chunk.decode('utf-8').replace("data: ", '')
        if raw_data != "":
            lines = raw_data.strip().splitlines()
            for line in lines:
                line = line.strip()
                if line and line != "[DONE]":
                  try:
                    json_object = json.loads(line)
                    if 'data' in json_object:
                      result = json_object['data']
                      full_response += result
                      time.sleep(0.05)
                      message_placeholder.markdown(full_response + "▌")
                  except json.JSONDecodeError:
                    print(f'Error decoding JSON: {line}')
    if not full_response:
      full_response = "No response from the assistant"

    # Send the response to the user
    message_placeholder.markdown(full_response)

  # Add the response to the message history
  st.session_state.messages.append({"role": "assistant", "content": full_response})
  # start with a message from the assistant