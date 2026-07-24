import streamlit as st
from chatbot import get_answer
import random
import time

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config (
    page_title="AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Main App */


/* Chat Messages */
[data-testid="stChatMessage"]{
    background:white;
    border-radius:18px;
    padding:18px;
    margin-bottom:15px;
    border:1px solid #E5E7EB;
    box-shadow:0px 3px 10px rgba(0,0,0,0.05);
}

/* Headings */
h1{
    font-size:34px !important;
    font-weight:700 !important;
    color:#1F2937;
}

h2{
    font-size:34px !important;
    font-weight:800 !important;
    color:#111827;
    margin-top:30px;
}

h3{
    font-size:22px !important;
    font-weight:700 !important;
    color:#2563EB;
    margin-top:20px;
}

/* Paragraph */
p{
    font-size:16px !important;
    line-height:1.8 !important;
    color:#374151;
}

/* Lists */
li{
    font-size:18px !important;
    margin-bottom:12px;
}

/* Code */
code{
    font-size:15px;
}

/* Progress Bar */
.stProgress{
    margin-top:10px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#FFFFFF;
}

[data-testid="stChatMessage"]{

transition:all .3s ease;

}

[data-testid="stChatMessage"]:hover{

transform:translateY(-4px);

box-shadow:0 14px 30px rgba(79,70,229,.15);

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "liked" not in st.session_state:
    st.session_state.liked = {}

if "disliked" not in st.session_state:
    st.session_state.disliked = {}
# =====================================================
# RANDOM THINKING MESSAGES
# =====================================================

loading_messages = [
    "🧠 Understanding your question...",
    "🤖 Thinking...",
    "📚 Searching Knowledge Base...",
    "🔍 Finding the best answer...",
    "💡 Processing your request...",
    "⚡ AI is generating a response...",
    "📖 Reading AI concepts...",
    "🚀 Almost there..."
]

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

.chat-title{
    text-align:center;
    color:white;
}

.user-box{
    background:#EEF6FF;
    padding:12px;
    border-radius:10px;
}

.bot-box{
    background:#F7F7F7;
    padding:12px;
    border-radius:10px;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#4F46E5,#7C3AED);
padding:35px;
border-radius:20px;
text-align:center;
color:white;
box-shadow:0px 8px 20px rgba(0,0,0,0.2);
">

<h1>🤖 AI FAQ Chatbot</h1>

<h3>Artificial Intelligence Virtual Assistant</h3>

<p style="font-size:18px;">
Powered by NLP • TF-IDF • Cosine Similarity
</p>

</div>
""", unsafe_allow_html=True)
# =====================================================
# QUICK QUESTIONS
# =====================================================

st.markdown("## 💡 Quick Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button("🤖 What is Artificial Intelligence?"):
        st.session_state.selected_question = "What is Artificial Intelligence?"

    if st.button("🧠 Explain Machine Learning"):
        st.session_state.selected_question = "Explain Machine Learning"

    if st.button("📚 What is Deep Learning?"):
        st.session_state.selected_question = "What is Deep Learning?"

    if st.button("🐍 What is Python?"):
        st.session_state.selected_question = "What is Python?"

with col2:

    if st.button("💬 What is NLP?"):
        st.session_state.selected_question = "What is NLP?"

    if st.button("📊 What is Data Science?"):
        st.session_state.selected_question = "What is Data Science?"

    if st.button("🎨 What is Generative AI?"):
        st.session_state.selected_question = "What is Generative AI?"

    if st.button("🤖 What is ChatGPT?"):
        st.session_state.selected_question = "What is ChatGPT?"

      # =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:

    avatar = "👤" if msg["role"] == "user" else "🤖"

    with st.chat_message(msg["role"], avatar=avatar):

        st.markdown(msg["content"])

        if msg["role"] == "assistant":

            st.markdown(
                f"""
<div style="
display:inline-block;
background:#EEF2FF;
color:#4338CA;
padding:6px 16px;
border-radius:20px;
font-weight:bold;
font-size:14px;
margin-bottom:10px;
">
🏷 {msg["category"]}
</div>
""",
                unsafe_allow_html=True
            )

            st.progress(float(msg["confidence"]))

            st.caption(
                f"📊 Confidence Score : {msg['confidence']*100:.1f}%"
            )

            if msg["confidence"] >= 0.80:
                st.success("✅ Excellent Match")

            elif msg["confidence"] >= 0.60:
                st.info("👍 Good Match")

            elif msg["confidence"] >= 0.40:
                st.warning("⚠ Average Match")

            else:
                st.error("❌ Low Confidence")  
        
# =====================================================
# CHAT INPUT
# =====================================================

default_question = st.session_state.selected_question

prompt = st.chat_input("💬 Ask me anything about Artificial Intelligence...")

if not prompt and default_question:
    prompt = default_question
    st.session_state.selected_question = ""

if prompt:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display User Message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # AI Thinking
    loading = random.choice(loading_messages)

    with st.spinner(loading):

        start = time.time()

        answer, confidence, category = get_answer(prompt)

        end = time.time()

    st.caption(f"⚡ Search Time: {end-start:.3f} sec")

    # Save Assistant Message
    assistant_message = {
        "role": "assistant",
        "content": answer,
        "confidence": confidence,
        "category": category
    }

    st.session_state.messages.append(assistant_message)

    # Display Assistant Message
    with st.chat_message("assistant", avatar="🤖"):

        placeholder = st.empty()
        typed = ""

        for ch in answer:
            typed += ch

           
            placeholder.markdown(
    f"""
<div style="
background:rgba(255,255,255,.80);
backdrop-filter:blur(18px);
padding:28px;
border-radius:20px;
border:1px solid #E5E7EB;
box-shadow:0 8px 25px rgba(0,0,0,.08);
">
{answer}
</div>
""",
    unsafe_allow_html=True,
)
            time.sleep(0.0002)

        st.write("")

        st.markdown(
            f"""
<div style="
display:inline-block;
background:#EEF2FF;
color:#4338CA;
padding:8px 18px;
border-radius:25px;
font-weight:600;
font-size:14px;
">
🏷 {category}
</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        # ChatGPT Style Buttons
        col1, col2, col3 = st.columns([1,1,6])

        with col1:
            if st.button("👍", key=f"like_{len(st.session_state.messages)}"):
                st.toast("Thanks for your feedback ❤️")

        with col2:
            if st.button("👎", key=f"dislike_{len(st.session_state.messages)}"):
                st.toast("Thanks! We'll improve future answers.")

        with col3:
            with st.expander("📋 Copy Answer"):
                st.code(answer, language=None)
                st.caption("Press Ctrl + C to copy")

        st.write("")

        st.progress(float(confidence))
        st.caption(f"🎯 Confidence : {confidence*100:.1f}%")

        if confidence >= 0.80:
            st.success("✅ Excellent Match")
        elif confidence >= 0.60:
            st.info("👍 Good Match")
        elif confidence >= 0.40:
            st.warning("⚠ Average Match")
        else:
            st.error("❌ Low Confidence")