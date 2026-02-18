"""
Multilingual Content Creator AI Assistant
Supports Tamil and English content generation
"""

import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI

load_dotenv()

class ContentCreatorAI:
    def __init__(self):
        """Initialize the Content Creator AI"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize LLM (using ChatOpenAI for better quality)
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model_name="gpt-4",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Initialize multilingual embeddings for RAG
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Load vector store (knowledge base)
        try:
            self.vectorstore = FAISS.load_local("faiss_index", self.embeddings)
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        except:
            print("⚠️  Knowledge base not found. RAG disabled. Using direct LLM.")
            self.retriever = None
    
    def get_relevant_context(self, topic):
        """Retrieve relevant content from knowledge base"""
        if self.retriever:
            docs = self.retriever.get_relevant_documents(topic)
            context = "\n".join([doc.page_content for doc in docs])
            return context
        return ""
    
    def create_blog_post(self, topic, language="English"):
        """Generate a blog post"""
        context = self.get_relevant_context(topic)
        
        if language.lower() == "tamil":
            prompt = PromptTemplate(
                input_variables=["topic", "context"],
                template="""நீங்கள் ஒரு தமிழ் உள்ளடக்க निर्माता. 
                
தலைப்பு: {topic}

প্রাসঙ্গিক তথ্য: {context}

பின்வரும் குறிப்புடன் தமிழ் மொழியில் ஒரு நல்ல ப்ளாக் பதிப்பை எழுதுக:
- முன்னுரை (அறிமுகம்)
- 3 முக்கிய பிரிவுகள்
- முடிவு
- அழைப்பு நடவடிக்கை

த��ிழ்:"""
            )
        else:
            prompt = PromptTemplate(
                input_variables=["topic", "context"],
                template="""You are an expert content creator specializing in engaging blog posts.

Topic: {topic}

Relevant Information: {context}

Write an awesome blog post with:
- Catchy Introduction
- 3 Main Sections (each with insights)
- Conclusion with key takeaways
- Call to Action

Blog Post:"""
            )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        content = chain.run(topic=topic, context=context)
        return content
    
    def create_social_media_content(self, topic, language="English", platform="LinkedIn"):
        """Generate social media content"""
        context = self.get_relevant_context(topic)
        
        if language.lower() == "tamil":
            prompt = PromptTemplate(
                input_variables=["topic", "platform", "context"],
                template="""நீங்கள் ஒரு சமூக ஊடக உள்ளடக்க நிபுணர்.

தலைப்பு: {topic}
தளம்: {platform}

প्रাসঙ्गिक তথ্য: {context}

{platform} க்கு கவர்ச்சிகரமான, ஈர்க்கும் பதிப்பு எழுதுக (150-200 சொற்கள்) தமிழ் மொழியில்:"""
            )
        else:
            prompt = PromptTemplate(
                input_variables=["topic", "platform", "context"],
                template="""You are a social media expert creating viral content.

Topic: {topic}
Platform: {platform}

Relevant Information: {context}

Write an engaging, shareable {platform} post (150-200 words):"""
            )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        content = chain.run(topic=topic, platform=platform, context=context)
        return content
    
    def create_product_description(self, product_name, features, language="English"):
        """Generate product description"""
        
        if language.lower() == "tamil":
            prompt = PromptTemplate(
                input_variables=["product_name", "features"],
                template="""நீங்கள் ஒரு পণ்য விপণன் நிபு���ர்.

பண்டம் பெயர்: {product_name}
பொருட்கள்: {features}

பின்வரும் உண்ணவும் ஈர்க்கும் பண்ட விளக்கம் எழுதுக தமிழ் மொழியில்:"""
            )
        else:
            prompt = PromptTemplate(
                input_variables=["product_name", "features"],
                template="""You are an expert copywriter for e-commerce products.

Product Name: {product_name}
Features: {features}

Write a compelling, persuasive product description:"""
            )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        content = chain.run(product_name=product_name, features=features)
        return content
    
    def create_email_campaign(self, topic, language="English"):
        """Generate email marketing content"""
        context = self.get_relevant_context(topic)
        
        if language.lower() == "tamil":
            prompt = PromptTemplate(
                input_variables=["topic", "context"],
                template="""நீங்கள் ஒரு மின்னஞ்சல் சந்தை நிபுணர்.

தலைப்பு: {topic}

प्रாসङ्गिक तথ्य: {context}

பின்வரும் கூறிய மின்னஞ்சல் பிரচாரம் எழுதுக தமிழ் மொழியில்:
- விষயம் கோடு (கவர்ச்சிகரமான)
- மூல (வ్యక్తিगత, ஈர்க்கும்)
- அழைப்பு நடவடிக்கை"""
            )
        else:
            prompt = PromptTemplate(
                input_variables=["topic", "context"],
                template="""You are an email marketing expert.

Topic: {topic}

Relevant Information: {context}

Write an effective email campaign with:
- Subject Line (catchy & compelling)
- Body (personalized, engaging)
- Call to Action"""
            )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        content = chain.run(topic=topic, context=context)
        return content

    def create_seo_content(self, keyword, language="English"):
        """Generate SEO-optimized content"""
        context = self.get_relevant_context(keyword)
        
        if language.lower() == "tamil":
            prompt = PromptTemplate(
                input_variables=["keyword", "context"],
                template="""நீங்கள் ஒரு SEO உள்ளடக்க நிபுணர்.

முக்கிய சொல்: {keyword}

प्राসङ्गिक தகவல்: {context}

{keyword} க்கு SEO-பொருத்தமான விஷயம் எழுதுக:
- H1, H2 தலைப்புகள்
- meta விளக்கம்
- 500 சொற்கள் + மூல"""
            )
        else:
            prompt = PromptTemplate(
                input_variables=["keyword", "context"],
                template="""You are an SEO content expert.

Target Keyword: {keyword}

Relevant Information: {context}

Write SEO-optimized content for "{keyword}":
- Include H1, H2 headings
- Meta description
- 500+ words with natural keyword placement"""
            )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        content = chain.run(keyword=keyword, context=context)
        return content

# Test function
def test_content_creator():
    creator = ContentCreatorAI()
    
    print("=" * 60)
    print("📝 ENGLISH BLOG POST")
    print("=" * 60)
    blog = creator.create_blog_post("Artificial Intelligence in Healthcare", language="English")
    print(blog)
    
    print("\n" + "=" * 60)
    print("📝 TAMIL BLOG POST")
    print("=" * 60)
    blog_tamil = creator.create_blog_post("செயற்கை புத்திமைமை", language="Tamil")
    print(blog_tamil)

if __name__ == "__main__":
    test_content_creator()