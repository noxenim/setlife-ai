import streamlit as st
import json
import time
from agents import ProfileAgent, UniversityAgent, ActionPlanAgent


st.set_page_config(
    page_title="SetLife-AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    div.block-container {
        padding-top: 2rem;
    }
    .uni-card {
        background-color: white;
        color: black !important; /* Force black text */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #6c757d;
    }
    .uni-card h4 {
        color: black !important;
        margin-top: 0;
    }
    .uni-card p {
        color: #333333 !important;
    }
    .reach { border-left-color: #ff4b4b; }
    .target { border-left-color: #ffa500; }
    .safe { border-left-color: #4CAF50; }
    </style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80) 
with col2:
    st.title("SetLife-AI")
    st.markdown("**Your AI-Powered Academic Strategist**")

st.divider()


with st.sidebar:
    st.header("📝 Student Profile")
    st.info("Fill in the details below to generate your strategy.")
    
    academics = st.text_area(" Academic Stats", height=100, 
                             placeholder="Grade 11\nGPA: 3.9/4.0\nSAT: 1520(if applicable)\nBranch:Computer Science")
    
    interests = st.text_area(" Interests & Story", height=100,
                             placeholder="President of Robotics Club.\nBuilt a wildfire detection drone.\nLove Formula 1 engineering.")
    
    preferences = st.text_area(" Preferences", height=70,
                             placeholder="Location: USA/UK\nMajor: Mechanical Engineering")
    
    budget = st.selectbox(" Yearly Budget Constraint", 
                      [ "Low (< $20k)","Medium ($20k - $50k)","High(above $50k)"])
    
    st.markdown("---")
    submit_btn = st.button("Generate Strategy Plan")


if not submit_btn:
    st.markdown("## 👋 Welcome to SetLife-AI")
    st.markdown("##### Your personal AI strategist for university admissions.")
    
    st.markdown("<br>", unsafe_allow_html=True) # Add some spacing
    
   
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("Step 1: The Profile")
        st.markdown("👈 **Go to the Sidebar** and enter your academic stats (GPA, SAT, Grade) and your personal story.")
        
    with col2:
        st.info("Step 2: The Goal")
        st.markdown("Tell us where you want to study, your major, and your budget constraints.")
        
    with col3:
        st.info("Step 3: The Strategy")
        st.markdown("Click **'Generate Strategy Plan'** to get a gap analysis, university list, and project roadmap.")

    st.markdown("---")
    st.markdown("### 💡 *Pro Tip: Be specific in your 'Story' for better project ideas!*")


if submit_btn:
    if not academics or not interests:
        st.error("Please provide at least your Academics and Interests to proceed.")
    else:
       
        progress_text = "Agents are collaborating..."
        my_bar = st.progress(0, text=progress_text)
        
       
        full_user_prompt = f"""
        ACADEMICS: {academics}
        INTERESTS/STORY: {interests}
        PREFERENCES: {preferences}
        BUDGET CONSTRAINT: {budget}
        """

        try:
           
            my_bar.progress(30, text=" Profile Agent: Analyzing transcript...")
            profile_agent = ProfileAgent()
            profile = profile_agent.analyze(full_user_prompt)
            
            
            my_bar.progress(60, text=" University Agent: Scanning global database...")
            uni_agent = UniversityAgent()
            unis = uni_agent.recommend(profile)
            
            
            my_bar.progress(90, text=" Strategy Agent: Identifying gaps & best strategy to follow...")
            plan_agent = ActionPlanAgent()
            plan = plan_agent.generate_plan(profile, unis)
            
            my_bar.empty() 

            
            tab1, tab2, tab3 = st.tabs(["👤 Student Profile", "🏫 University List", "🚀 Action Plan"])
            
            
            with tab1:
                st.subheader("Extracted Profile Analysis")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Core Strengths**")
                    for s in profile.get('academic_strengths', []):
                        st.caption(f"✅ {s}")
                with c2:
                    st.markdown("**Interests Detected**")
                    for i in profile.get('interests', []):
                        st.caption(f"⭐ {i}")
                
                

           
            with tab2:
                st.subheader("Your Balanced College List")
                
                
                def draw_uni_card(type_name, uni_list, color_class):
                    st.markdown(f"### {type_name}")
                    if not uni_list:
                        st.write("No universities found in this category.")
                    for u in uni_list:
                        st.markdown(f"""
                        <div class="uni-card {color_class}">
                            <h4>{u['name']}</h4>
                            <p><i>{u['reason']}</i></p>
                        </div>
                        """, unsafe_allow_html=True)

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    draw_uni_card("🚀 Reach", unis.get('reach', []), "reach")
                with col_b:
                    draw_uni_card("🎯 Target", unis.get('target', []), "target")
                with col_c:
                    draw_uni_card("🛡️ Safe", unis.get('safe', []), "safe")

            
            with tab3:
                st.subheader("Strategic Execution Plan")
                
                
                st.warning(f"**⚠️ Gap Analysis:** {plan.get('gap_analysis', 'N/A')}")
                
                
                st.markdown("### 🦄 Your 'Spike' Project")
                spike = plan.get('the_spike', {})
                st.info(f"**Project:** {spike.get('title')}\n\n**Brief:** {spike.get('description')}")
                
                st.divider()
                
               
                st.markdown("### 📅 Monthly Roadmap")
                for period in plan.get('timeline', []):
                    with st.container():
                        st.markdown(f"**{period.get('period')}**")
                        for item in period.get('action_items', []):
                            st.markdown(f"- {item}")
                        st.markdown("---")

        except Exception as e:
            st.error(f"An error occurred: {e}")
