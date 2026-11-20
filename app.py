import streamlit as st
import sqlite3
from datetime import date

# ---------------- APP SETTINGS ----------------
st.set_page_config(
    page_title="MEMORA | Your Memory Space",
    page_icon="💜",
    layout="wide"
)

DB_NAME = "memora.db"

# ---------------- DATABASE ----------------
def create_database():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            memory_date TEXT NOT NULL,
            mood TEXT NOT NULL,
            story TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_memory(title, memory_date, mood, story):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO memories (title, memory_date, mood, story) VALUES (?, ?, ?, ?)",
        (title, memory_date, mood, story)
    )
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT id, title, memory_date, mood, story FROM memories ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows

create_database()

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp { background-color: #faf8ff; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { color: #493568; }
div[data-testid="stMetric"] {
    background: #f0eaff;
    padding: 16px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 💜 MEMORA")
    st.caption("Your memories, your emotions, your story.")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Home", "Add a Memory", "My Memories", "About MEMORA"]
    )

    st.divider()
    st.caption("Made with love, for memories ✨")

memories = get_memories()

# ---------------- HOME ----------------
if page == "Home":
    st.markdown("### ✨ Your personal memory space")
    st.title("Welcome to MEMORA 💜")
    st.write("Every moment matters. Keep your memories alive.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Memories Saved", len(memories))
    col2.metric("Your Memory Space", "🌷 Personal")
    col3.metric("Today's Date", date.today().strftime("%d %b %Y"))

    st.divider()
    st.subheader("💭 A little reminder")
    st.info("Some moments are small, but the feelings they leave are forever.")

    st.subheader("🌸 Recent Memories")

    if memories:
        for memory in memories[:3]:
            with st.container(border=True):
                st.subheader(memory[1])
                st.caption(f"📅 {memory[2]}  |  {memory[3]}")
                st.write(memory[4])
    else:
        st.write("Your memory collection is waiting for its first beautiful moment. 💌")
        st.caption("Go to 'Add a Memory' from the sidebar to begin.")

# ---------------- ADD MEMORY ----------------
elif page == "Add a Memory":
    st.title("💌 Save a new memory")
    st.write("Take a moment. What would you like to remember?")

    with st.form("memory_form", clear_on_submit=True):
        title = st.text_input("Memory title", placeholder="e.g. The best day ever")
        memory_date = st.date_input("When did it happen?", value=date.today())

        mood = st.selectbox(
            "How did this memory make you feel?",
            ["😊 Happy", "🥰 Loved", "🌈 Excited", "🥹 Nostalgic",
             "😌 Peaceful", "😢 Sad", "😤 Angry", "🤍 Neutral"]
        )

        story = st.text_area(
            "Your memory",
            placeholder="Write your memory here...",
            height=180
        )

        save_button = st.form_submit_button("💜 Save Memory")

        if save_button:
            if title.strip() and story.strip():
                save_memory(
                    title.strip(),
                    memory_date.strftime("%d %B %Y"),
                    mood,
                    story.strip()
                )
                st.success("Your memory has been permanently saved! 💜")
            else:
                st.error("Please enter both a title and your memory.")

# ---------------- MY MEMORIES ----------------
elif page == "My Memories":
    st.title("📚 My Memories")
    st.write("Every memory is a piece of your story.")

    search = st.text_input("🔍 Search memories by title or text")

    filtered = [
        m for m in memories
        if search.lower() in m[1].lower()
        or search.lower() in m[4].lower()
        or search.lower() in m[3].lower()
    ]

    if filtered:
        for memory in filtered:
            with st.container(border=True):
                st.subheader(memory[1])
                st.caption(f"📅 {memory[2]}  |  {memory[3]}")
                st.write(memory[4])
    else:
        st.info("No memories found. Try another search or add your first memory.")

# ---------------- ABOUT ----------------
elif page == "About MEMORA":
    st.title("🌷 About MEMORA")
    st.subheader("An AI-Powered Sentimental Memory and Emotion Assistant")

    st.write("""
    MEMORA is designed to help people store, organize, and revisit
    precious memories in a meaningful way.
    """)

    st.markdown("""
    **Our vision:**
    - 💌 Preserve precious moments
    - 🧠 Understand emotions
    - 🔍 Find memories easily
    - ✨ Relive meaningful experiences

    *Every memory deserves a place.*
    """)

st.divider()
st.caption("MEMORA 💜 | Your memories. Your emotions. Your story.")
