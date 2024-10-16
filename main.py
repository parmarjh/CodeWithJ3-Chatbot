import streamlit as st
import os
from anthropic import Anthropic

# Streamlit page configuration
st.set_page_config(
    page_title="CodeWithJatin - CV ChatBot",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded",
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hi :wave:")
    st.title("I'm CodeWithJatin")

with col2:
    st.image("logo.png")

st.title(" ")

# Main content
st.title("💼 CodeWithJatin ChatBot")
st.write("ASk me anything")


# Custom CSS
# st.markdown("""
# <style>
#     .reportview-container {
#         background: #f0f2f6
#     }
#     .main {
#         background-color: #ffffff;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     h1 {
#         color: #2c3e50;
#     }
#     .stButton>button {
#         background-color: #3498db;
#         color: white;
#         width: 100%;
#     }
# </style>
# """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This chatbot leverages Claude AI to answer your questions about CodeWithJatin's YouTube channel. "
    "Feel free to ask about his skills, experience, or background!"
)

st.sidebar.title("CodeWithJatin")
st.sidebar.info(
    "Discover more exciting projects and tutorials at [CodeWithJoe.net](https://codewithjoe.net)!"
)

st.sidebar.title("Hire Me")
st.sidebar.info(
    """
    I'm Jatin, a seasoned Ai ml genai  llm Web3 developer since 2018, with expertise in Ethereum, EVMs,genai, llm chatbot and machine learning. 
    I specialize in creating custom Python Web3 Telegram bots, trading bots, and offer consultation and educational services. 
    Available for project-based, hourly, or consultation work.
    Reach out via my [YouTube Channel](https://www.youtube.com/@funinaiofficial).
    """
)



# Use environment variable for API key
ANTHROPIC_API_KEY = os.environ.get("ClaudeAI- API Key")
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


# Predefined questions
predefined_questions = [
    "What are CodeWithJoe's key skills?",
    "What is CodeWithJoe's educational background?",
    "What is CodeWithJoe's most recent work experience?"
]

# Create buttons for predefined questions
st.subheader("Quick Questions:")
cols = st.columns(len(predefined_questions))
for idx, question in enumerate(predefined_questions):
    if cols[idx].button(question, key=f"pred_q_{idx}"):
        response = get_claude_response(question, cv_content)
        st.markdown(f"**Q:** {question}")
        st.markdown(f"**A:** {response}")
        st.markdown("---")

# Create a form for custom user input
with st.form(key='user_input_form'):
    st.subheader("Ask Your Own Question:")
    user_input = st.text_input("Enter your question about CodeWithJoe's YoutubeChannel:")
    submit_button = st.form_submit_button(label='Submit Question')

# Handle form submission
if submit_button:
    if user_input:
        response = get_claude_response(user_input, cv_content)
        st.markdown(f"**Q:** {user_input}")
        st.markdown(f"**A:** {response}")
        st.markdown("---")
    else:
        st.warning("Please enter a question before submitting.")

# Display previous conversations
if 'conversations' not in st.session_state:
    st.session_state.conversations = []

if submit_button and user_input:
    st.session_state.conversations.append((user_input, response))

if st.session_state.conversations:
    st.subheader("Previous Conversations:")
    for q, a in reversed(st.session_state.conversations):
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {a}")
        st.markdown("---")


with open('code.txt') as f:
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
st.markdown("Created with ❤️ by [CodeWithJ3](https://codewithjatin.net)")


