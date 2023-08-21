# ✨ CodeGPT Agent
#### A simple chatbot boilerplate that uses the CodeGPT Agent to respond to user input.

## Getting Started

To use this chatbot, follow these steps:

1. Make sure you have the required dependencies installed. You can install them using the following command: `pip install -r requirements.txt`
2. Get your CodeGPT API key and agent ID. You can either set them as environment variables or pass them as query parameters in the URL.
3. Run the Streamlit app by executing the following command in your terminal: `streamlit run codegpt-agent-boilerplate-streamlit.py`

![Preview](https://github.com/gustavoespindola/codegpt-simple-chatbot-agent-boilerplate-streamlit/blob/75d04012c21bb037ae76b8f37ddde5001fad905e/intro.gif)

## Streamlit Environment Variables Usage for CodeGPT API Key and Agent ID

### Option 1: Reading from STREAMLIT Environment Variables
1. Create a folder named `.streamlit` in your project directory if it doesn't already exist.
2. Inside the `.streamlit` folder, create a file named `secrets.toml`.
3. In `secrets.toml`, enter your CodeGPT API Key and Agent ID in the following format:
```
codegpt_api_key = "your-api-key"
codegpt_agent_id = "your-agent-id"
```

### Option 2: Getting from URL Query Parameters
1. If you prefer, you can pass the API Key and Agent ID as query parameters in the URL when running the Streamlit app. For example: `http://localhost:8501/?codegpt_api_key=your-api-key&codegpt_agent_id=your-agent-id`



## Chat

1. Type your message in the input box and press Enter to send it to the chatbot.
2. The chatbot will process your message using the CodeGPT Agent and provide a response.

## Memory

The chatbot has memory functionality, which means it can store and use conversation history for context. By default, it remembers the last 10 messages, but you can modify this behavior.

![Alt Text](https://raw.githubusercontent.com/gustavoespindola/codegpt-simple-chatbot-agent-boilerplate-streamlit/e1a00f2e3a12ae8b88c2a7328a07de82069433d6/intro.gif)

## Code Structure

The code is structured as follows:

- **Sending Messages**: The `send_message()` function sends messages to the CodeGPT Agent API. It accepts a boolean argument `memory` to control whether the full conversation history or only the latest message is sent.

- **Initializing Chat History**: The chat history is stored in the `st.session_state.messages` list.

- **Displaying Messages**: The app displays chat messages from history on rerun and allows users to input their messages.

- **Displaying Responses**: The assistant's response is displayed using the `st.chat_message()` function.

- **Streamlit Configuration**: The Streamlit app is configured with a page title, icon, and menu items.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Contact

For more information or assistance, you can visit the [CodeGPT website](https://codegpt.co) or report issues on the GitHub repository.

This chatbot boilerplate is provided as-is and can serve as a foundation for test or building your own conversational applications.
