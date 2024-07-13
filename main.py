import streamlit as st
import os
from anthropic import Anthropic

# Streamlit page configuration
st.set_page_config(
    page_title="CodeWithJoe - CV ChatBot",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded",
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hi :wave:")
    st.title("I'm CodeWithJoe")

with col2:
    st.image("logo.png")

st.title(" ")

# Main content
st.title("💼 CodeWithJoe ChatBot")
st.write("ASk me anything")


# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This chatbot leverages Claude AI to answer your questions about CodeWithJoe's YouTube channel. "
    "Feel free to ask about his skills, experience, or background!"
)

st.sidebar.title("CodeWithJoe")
st.sidebar.info(
    "Discover more exciting projects and tutorials at [CodeWithJoe.net](https://codewithjoe.net)!"
)

st.sidebar.title("Hire Me")
st.sidebar.info(
    """
    I'm Joe, a seasoned Web3 developer since 2018, with expertise in Ethereum, EVMs, and machine learning. 
    I specialize in creating custom Python Web3 Telegram bots, trading bots, and offer consultation and educational services. 
    Available for project-based, hourly, or consultation work.
    Reach out via my [YouTube Channel](https://www.youtube.com/@CodeWithJoe).
    """
)



# Use environment variable for API key
ANTHROPIC_API_KEY = os.environ.get("")
if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = st.text_input("Enter your Anthropic API Key:", type="password")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def load_cv(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"CV file not found at {file_path}. Please check the file path.")
        return ""

def get_claude_response(prompt, cv_content):
    system_message = f"""You are a chatbot that only discusses the CV of CodeWithJoe. 
    Respond to queries based solely on the information in this CV:

    {cv_content}

    Only provide information that is explicitly stated in the CV. If asked about something not in the CV, 
    politely state that you don't have that information."""

    try:
        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="claude-3-opus-20240229",
            system=system_message
        )
        
        # Extract the text content from the response
        response_text = message.content[0].text if message.content else "No response received."
        
        # Clean up the response (remove any remaining formatting)
        response_text = response_text.strip()
        
        return response_text
    except Exception as e:
        st.error(f"An error occurred while calling the Claude API: {str(e)}")
        return "I'm sorry, but I encountered an error while processing your request. Please check the API key and try again."

# Load the CV content
cv_path = "code.txt"  # Hardcoded path to the CV file
cv_content = load_cv(cv_path)

# Create a form for user input
with st.form(key='user_input_form'):
    user_input = st.text_input("Ask me anything about CodeWithJoe's YouTube Channel:")
    submit_button = st.form_submit_button(label='Submit Question')

# Handle form submission
if submit_button:
    if user_input:
        response = get_claude_response(user_input, cv_content)
        st.markdown("### Claude's Response:")
        st.markdown(response)
    else:
        st.warning("Please enter a question before submitting.")

# Display previous conversations
if 'conversations' not in st.session_state:
    st.session_state.conversations = []

if submit_button and user_input:
    st.session_state.conversations.append((user_input, response))

if st.session_state.conversations:
    st.markdown("### Previous Conversations:")
    for q, a in reversed(st.session_state.conversations[:-1]):
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {a}")
        st.markdown("---")





with open('cv.txt') as f:
   st.download_button('Download CSV', f)
   st.write('Thanks for downloading!')


st.title(" ")
col3, col4 = st.columns(2)

with col3:
    st.subheader("YouTube Channel")
    st.write("- 20k subs")
    st.write("- 2 billion Views")
    st.write("- Python, Javascript")

with col4:
    st.video("https://www.youtube.com/channel/UCdgU4pljNproO0RQVbT5QKg")
# Footer
st.markdown("---")
st.markdown("Created with ❤️ by [CodeWithJoe](https://codewithjoe.net)")


#https://www.youtube.com/@CodeWithJoe
