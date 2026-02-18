"""
Streamlit Web Interface for Content Creator AI
Run with: streamlit run app.py
"""

import streamlit as st
from content_creator import ContentCreatorAI

# Page config
st.set_page_config(
    page_title="🎨 Content Creator AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton > button { width: 100%; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px; }
    .stTextInput > div > div > input { font-size: 16px; padding: 10px; }
    h1 { color: #FF6B6B; text-align: center; }
    h2 { color: #4ECDC4; }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'creator' not in st.session_state:
    st.session_state.creator = ContentCreatorAI()

# Header
st.markdown("# 🎨 Multilingual Content Creator AI Assistant")
st.markdown("### Create Awesome Content in English & Tamil 🚀")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    content_type = st.selectbox(
        "📌 Select Content Type",
        [
            "🖊️ Blog Post",
            "📱 Social Media",
            "🛍️ Product Description",
            "✉️ Email Campaign",
            "🔍 SEO Content"
        ]
    )
    
    language = st.radio(
        "🌐 Choose Language",
        ["English", "Tamil"],
        horizontal=True
    )
    
    st.markdown("---")
    st.info("💡 Tip: Be specific with your topics for better results!")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Input Details")
    
    if "Blog Post" in content_type:
        topic = st.text_input(
            "📝 Enter Blog Topic",
            placeholder="e.g., How AI is changing education"
        )
        
        if st.button("✨ Generate Blog Post", key="blog"):
            if topic:
                with st.spinner("🎯 Creating awesome content..."):
                    content = st.session_state.creator.create_blog_post(topic, language)
                    st.session_state.blog_content = content
                    st.success("✅ Blog post created!")
            else:
                st.warning("⚠️ Please enter a topic!")
    
    elif "Social Media" in content_type:
        topic = st.text_input(
            "📝 Enter Topic",
            placeholder="e.g., Remote work benefits"
        )
        platform = st.selectbox(
            "📱 Select Platform",
            ["LinkedIn", "Twitter", "Instagram", "Facebook"]
        )
        
        if st.button("✨ Generate Social Post", key="social"):
            if topic:
                with st.spinner("🎯 Creating awesome content..."):
                    content = st.session_state.creator.create_social_media_content(
                        topic, language, platform
                    )
                    st.session_state.social_content = content
                    st.success("✅ Social media post created!")
            else:
                st.warning("⚠️ Please enter a topic!")
    
    elif "Product" in content_type:
        product_name = st.text_input(
            "🛍️ Product Name",
            placeholder="e.g., Premium Wireless Headphones"
        )
        features = st.text_area(
            "✨ Product Features",
            placeholder="e.g., Noise cancellation, 30-hour battery, Premium sound"
        )
        
        if st.button("✨ Generate Description", key="product"):
            if product_name and features:
                with st.spinner("🎯 Creating awesome content..."):
                    content = st.session_state.creator.create_product_description(
                        product_name, features, language
                    )
                    st.session_state.product_content = content
                    st.success("✅ Product description created!")
            else:
                st.warning("⚠️ Please fill in product details!")
    
    elif "Email" in content_type:
        topic = st.text_input(
            "📝 Campaign Topic",
            placeholder="e.g., New product launch"
        )
        
        if st.button("✨ Generate Email", key="email"):
            if topic:
                with st.spinner("🎯 Creating awesome content..."):
                    content = st.session_state.creator.create_email_campaign(topic, language)
                    st.session_state.email_content = content
                    st.success("✅ Email campaign created!")
            else:
                st.warning("⚠️ Please enter a topic!")
    
    elif "SEO" in content_type:
        keyword = st.text_input(
            "🔍 Target Keyword",
            placeholder="e.g., best productivity apps"
        )
        
        if st.button("✨ Generate SEO Content", key="seo"):
            if keyword:
                with st.spinner("🎯 Creating awesome content..."):
                    content = st.session_state.creator.create_seo_content(keyword, language)
                    st.session_state.seo_content = content
                    st.success("✅ SEO content created!")
            else:
                st.warning("⚠️ Please enter a keyword!")

# Display generated content
with col2:
    st.subheader("📤 Generated Content")
    
    content_key = None
    if "Blog Post" in content_type:
        content_key = "blog_content"
    elif "Social Media" in content_type:
        content_key = "social_content"
    elif "Product" in content_type:
        content_key = "product_content"
    elif "Email" in content_type:
        content_key = "email_content"
    elif "SEO" in content_type:
        content_key = "seo_content"
    
    if content_key and content_key in st.session_state:
        st.markdown(st.session_state[content_key])
        
        # Copy button
        st.code(st.session_state[content_key], language="markdown")
        
        # Download button
        st.download_button(
            label="⬇️ Download as TXT",
            data=st.session_state[content_key],
            file_name="generated_content.txt",
            mime="text/plain"
        )
    else:
        st.info("👈 Generate content to see it here!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 Powered by LangChain + OpenAI GPT-4 + RAG</p>
    <p>Made with ❤️ for Content Creators</p>
    </div>
    """, unsafe_allow_html=True)