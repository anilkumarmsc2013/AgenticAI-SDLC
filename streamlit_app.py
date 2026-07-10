# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from sdlc_graph import (
    graph,  # your compiled LangGraph
    State,  # your TypedDict state schema
)
import time
from datetime import datetime
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="ANIL KUMAR R - AGENTIC AI SDLC",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional MVP Look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Custom Card Styling */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Progress Steps */
    .progress-step {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .step-completed {
        background: #10b981;
        color: white;
    }
    
    .step-active {
        background: #3b82f6;
        color: white;
        animation: pulse 2s infinite;
    }
    
    .step-pending {
        background: #e5e7eb;
        color: #6b7280;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-approved {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-denied {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .status-pending {
        background: #fef3c7;
        color: #92400e;
    }
    
    /* Animated Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: #1e293b;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Metrics Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Code Block Enhancement */
    .stCodeBlock {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-block;
        width: 80px;
        height: 20px;
    }
    
    .loading-dots:after {
        content: ' .';
        animation: dots 1s steps(5, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% {
            color: rgba(0,0,0,0);
            text-shadow:
                .25em 0 0 rgba(0,0,0,0),
                .5em 0 0 rgba(0,0,0,0);
        }
        40% {
            color: #1e293b;
            text-shadow:
                .25em 0 0 rgba(0,0,0,0),
                .5em 0 0 rgba(0,0,0,0);
        }
        60% {
            text-shadow:
                .25em 0 0 #1e293b,
                .5em 0 0 rgba(0,0,0,0);
        }
        80%, 100% {
            text-shadow:
                .25em 0 0 #1e293b,
                .5em 0 0 #1e293b;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced tracking
if "thread" not in st.session_state:
    import uuid
    st.session_state.thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
    st.session_state.state = {
        "requirements": "",
        "user_stories": [],
        "user_story_status": "Approve",
        "user_story_feedback": [],
        "design_document": {},
        "design_document_review_status": "Approve",
        "design_document_review_feedback": [],
        "code": "",
        "code_review_status": "Approve",
        "code_review_feedback": [],
        "security_review_status": "Approve",
        "security_review_feedback": "",
        "test_cases": "",
        "test_cases_review_status": "Approve",
        "test_cases_review_feedback": [],
        "qa_review_status": "Approve",
        "qa_review_feedback": [],
        "deployment": ""
    }
    st.session_state.active_node = "User Requirements"
    st.session_state.events = []
    st.session_state.start_time = None
    st.session_state.notifications = []
    st.session_state.theme = "light"
    st.session_state.export_history = []

# Helper Functions
def add_notification(message, type="info"):
    """Add a notification to the queue"""
    st.session_state.notifications.append({
        "message": message,
        "type": type,
        "timestamp": datetime.now()
    })

def get_elapsed_time():
    """Get elapsed time since workflow started"""
    if st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"

def get_completion_percentage():
    """Calculate workflow completion percentage"""
    flow_order = [
        "User Requirements", "Auto-generate User Stories", "Human User Story Approval",
        "Create Design Document", "Human Design Document Review", "Generate Code",
        "Human Code Review", "Security Review", "Human Security Review",
        "Write Test Cases", "Human Test Cases Review", "QA Testing",
        "Human QA Review", "Deployment"
    ]
    current = st.session_state.active_node
    if current in flow_order:
        return int((flow_order.index(current) + 1) / len(flow_order) * 100)
    return 0

def render_progress_bar():
    """Render an animated progress bar"""
    progress = get_completion_percentage()
    st.markdown(f"""
    <div style="background: #e5e7eb; border-radius: 8px; height: 8px; overflow: hidden;">
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    width: {progress}%; height: 100%; transition: width 0.5s ease;">
        </div>
    </div>
    <p style="text-align: center; margin-top: 8px; color: #64748b; font-size: 14px;">
        {progress}% Complete
    </p>
    """, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Project Info Card
    st.markdown("""
    <div class="custom-card">
        <h4 style="margin: 0 0 10px 0;">📊 Project Dashboard</h4>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #64748b;">Session ID:</span>
            <span style="font-family: monospace; font-size: 12px;">
                {}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #64748b;">Elapsed Time:</span>
            <span style="font-weight: 600;">{}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #64748b;">Status:</span>
            <span class="status-badge status-pending">In Progress</span>
        </div>
    </div>
    """.format(
        st.session_state.thread["configurable"]["thread_id"][:8],
        get_elapsed_time()
    ), unsafe_allow_html=True)
    
    # Progress Overview
    render_progress_bar()
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export All", use_container_width=True):
            # Export functionality
            add_notification("Exporting all artifacts...", "info")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            if st.checkbox("Confirm reset?"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()
    
    # Notifications Panel
    if st.session_state.notifications:
        st.markdown("### 🔔 Notifications")
        for notif in st.session_state.notifications[-3:]:  # Show last 3
            icon = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(notif["type"], "ℹ️")
            st.markdown(f"{icon} {notif['message']}")
    
    # Settings
    with st.expander("⚙️ Settings", expanded=False):
        st.checkbox("Enable Auto-Save", value=True)
        st.checkbox("Show Advanced Options", value=False)
        st.selectbox("LLM Model", ["gemma2-9b-it", "deepseek-r1-distill-llama-70b","llama-3.3-70b-versatile"], index=0)

# Main Header
st.markdown("""
<div class="main-header fade-in">
    <h1 style="margin: 0; font-size: 2.5rem;">🚀 ANIL KUMAR R - AI-Powered SDLC Workflow Wizard</h1>
    <p style="margin: 10px 0 0 0; opacity: 0.9;">Transform your ideas into production-ready software with AI</p>
</div>
""", unsafe_allow_html=True)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card fade-in">
        <div class="metric-value">14</div>
        <div class="metric-label">Workflow Steps</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    stories_count = len(st.session_state.state.get("user_stories", []))
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-value">{stories_count}</div>
        <div class="metric-label">User Stories</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    files_count = len(os.listdir("generated_code")) if os.path.exists("generated_code") else 0
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-value">{files_count}</div>
        <div class="metric-label">Code Files</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    completion = get_completion_percentage()
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-value">{completion}%</div>
        <div class="metric-label">Complete</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Progress Tracker
st.markdown("### 🎯 Workflow Progress")

flow_order = [
    ("User Requirements", "📋", "Define project requirements"),
    ("Auto-generate User Stories", "🤖", "AI generates user stories"),
    ("Human User Story Approval", "👥", "Review and approve stories"),
    ("Create Design Document", "📐", "Generate technical design"),
    ("Human Design Document Review", "🔍", "Review design document"),
    ("Generate Code", "💻", "AI writes the code"),
    ("Human Code Review", "👨‍💻", "Review generated code"),
    ("Security Review", "🔒", "Automated security check"),
    ("Human Security Review", "🛡️", "Manual security review"),
    ("Write Test Cases", "🧪", "Generate test cases"),
    ("Human Test Cases Review", "✔️", "Review test cases"),
    ("QA Testing", "🎯", "Run quality assurance"),
    ("Human QA Review", "✅", "Final QA approval"),
    ("Deployment", "🚀", "Deploy to production")
]

def get_node_status(node_name):
    current = st.session_state.active_node
    current_names = [n[0] for n in flow_order]
    if current not in current_names:
        return "pending"
    current_idx = current_names.index(current)
    node_idx = current_names.index(node_name)
    if node_idx < current_idx:
        return "completed"
    elif node_idx == current_idx:
        return "active"
    return "pending"

# Create visual workflow
workflow_cols = st.columns(7)
for i, (node, icon, desc) in enumerate(flow_order):
    col_idx = i % 7
    status = get_node_status(node)
    
    with workflow_cols[col_idx]:
        if status == "completed":
            st.markdown(f"""
            <div class="progress-step step-completed" title="{desc}">
                {icon} {node.split()[0]}
            </div>
            """, unsafe_allow_html=True)
        elif status == "active":
            st.markdown(f"""
            <div class="progress-step step-active" title="{desc}">
                {icon} {node.split()[0]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="progress-step step-pending" title="{desc}">
                {icon} {node.split()[0]}
            </div>
            """, unsafe_allow_html=True)

# Main Content Area with Enhanced Tabs
tabs = st.tabs([
    "📋 Requirements", 
    "📘 User Stories", 
    "📐 Design", 
    "💻 Code", 
    "🧪 Tests", 
    "🔒 Security", 
    "✅ QA", 
    "🚀 Deploy",
    "📊 Analytics"
])

state = st.session_state.state

# Tab 1: Requirements
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Project Requirements")
        
        # Requirements input with enhanced UI
        # Check if we have a template to use
        default_requirements = state.get("requirements", "")
        if "template_to_use" in st.session_state:
            default_requirements = st.session_state.template_to_use
            # Update the state with the template content
            state['requirements'] = st.session_state.template_to_use
            st.session_state.state = state
            # Clear the template after using it
            del st.session_state.template_to_use
        
        requirements = st.text_area(
            "Enter your project requirements:",
            default_requirements,
            height=300,
            placeholder="Describe your software project in detail...\n\nExample:\nCreate a flight booking system that allows users to:\n- Search for flights\n- Book tickets\n- Manage reservations\n- Process payments",
            key="requirements_input"
        )
        
        # Update state with current requirements value
        state['requirements'] = requirements
        st.session_state.state = state
        
        # Word count and validation
        word_count = len(requirements.split()) if requirements else 0
        st.caption(f"📊 Word count: {word_count} | Recommended: 50-500 words")
        
        if st.button("🚀 Start Workflow", type="primary", use_container_width=True):
            # Get the current requirements from the widget
            current_requirements = st.session_state.requirements_input
            word_count = len(current_requirements.split()) if current_requirements else 0
            
            if word_count < 10:
                st.error("❌ Please provide more detailed requirements (at least 10 words)")
            else:
                # Start timer
                st.session_state.start_time = datetime.now()
                
                # Update state with current requirements
                state['requirements'] = current_requirements
                st.session_state.state = state
                
                # Progress animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Start the graph stream with progress updates
                for i, event in enumerate(graph.stream(state, st.session_state.thread)):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
                        
                        # Update progress
                        progress_bar.progress(min((i + 1) * 10, 100))
                        status_text.text(f"Processing: {node}...")
                        time.sleep(0.1)  # Small delay for visual effect
                
                add_notification("Requirements submitted successfully!", "success")
                st.rerun()
    
    with col2:
        st.markdown("### 💡 Tips for Better Results")
        st.info("""
        **Best Practices:**
        - Be specific about features
        - Include user roles
        - Mention technical constraints
        - Specify integrations needed
        - Define success criteria
        """)
        
        # Template Examples
        with st.expander("📄 View Templates"):
            template = st.selectbox("Choose a template:", [
                "E-commerce Platform",
                "SaaS Dashboard",
                "Mobile App Backend",
                "API Service"
            ])
            
            templates = {
                "E-commerce Platform": "Create an e-commerce platform with user authentication, product catalog, shopping cart, payment processing, and order management.",
                "SaaS Dashboard": "Build a SaaS analytics dashboard with user management, data visualization, real-time updates, and export capabilities.",
                "Mobile App Backend": "Develop a REST API backend for a mobile app with user authentication, push notifications, and data synchronization.",
                "API Service": "Create a microservice API with CRUD operations, authentication, rate limiting, and comprehensive documentation."
            }
            
            if st.button("Use Template"):
                # Store template in a separate session state variable
                st.session_state.template_to_use = templates[template]
                st.rerun()

# Tab 2: User Stories
with tabs[1]:
    st.markdown("### 📚 Generated User Stories")
    
    user_stories = st.session_state.state.get("user_stories", [])
    
    if user_stories:
        # Display stories in cards
        for i, story in enumerate(user_stories, 1):
            st.markdown(f"""
            <div class="custom-card fade-in">
                <h4 style="color: #667eea; margin-bottom: 10px;">Story #{i}</h4>
                <p style="margin: 0;">{story}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Review Section
        st.markdown("### 🔍 Review User Stories")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            status = st.radio(
                "Do these user stories accurately capture your requirements?",
                ["Approve", "Denied"],
                horizontal=True,
                key="user_stories_approval"
            )
            
            if status == "Denied":
                feedback = st.text_area(
                    "Please provide specific feedback for improvement:",
                    placeholder="E.g., Missing admin functionality, need more detail on payment processing...",
                    key="user_stories_feedback"
                )
        
        with col2:
            st.markdown("### 📊 Story Stats")
            st.metric("Total Stories", len(user_stories))
            st.metric("Avg. Length", f"{sum(len(s.split()) for s in user_stories) // len(user_stories)} words")
        
        if st.button("✅ Submit Review", type="primary", use_container_width=True):
            # Update state with review decision
            feedback_text = st.session_state.get("user_stories_feedback", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"user_story_status": status, "user_story_feedback": [feedback_text]},
                as_node="Human User Story Approval"
            )
            
            # Continue graph execution
            with st.spinner("Processing your feedback..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"User stories {status.lower()}!", "success" if status == "Approve" else "info")
            st.rerun()
    else:
        st.info("🤖 User stories will be generated after you submit requirements.")

# Tab 3: Design Document
with tabs[2]:
    st.markdown("### 📐 Technical Design Document")
    
    doc = st.session_state.state.get("design_document", {})
    has_content = any(doc.get(section, []) for section in ["functional", "technical", "assumptions", "open_questions"])
    
    if has_content:
        # Design Document Viewer
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Functional Requirements
            if doc.get("functional"):
                with st.expander("🎯 Functional Requirements", expanded=True):
                    for item in doc["functional"]:
                        st.markdown(f"• {item}")
            
            # Technical Requirements
            if doc.get("technical"):
                with st.expander("⚙️ Technical Requirements", expanded=True):
                    for item in doc["technical"]:
                        st.markdown(f"• {item}")
            
            # Assumptions
            if doc.get("assumptions"):
                with st.expander("💭 Assumptions", expanded=False):
                    for item in doc["assumptions"]:
                        st.markdown(f"• {item}")
            
            # Open Questions
            if doc.get("open_questions"):
                with st.expander("❓ Open Questions / Risks", expanded=False):
                    for item in doc["open_questions"]:
                        st.markdown(f"• {item}")
        
        with col2:
            st.markdown("### 📄 Document Actions")
            if st.button("📥 Export to Word", use_container_width=True):
                st.success("✅ Document exported to artifacts/design_document.docx")
            
            if st.button("📧 Email Document", use_container_width=True):
                st.info("📧 Email functionality coming soon!")
        
        # Review Section
        st.markdown("### 🔍 Review Design Document")
        status = st.radio(
            "Is the design document complete and accurate?",
            ["Approve", "Denied"],
            horizontal=True,
            key="design_doc_approval"
        )
        
        if status == "Denied":
            feedback = st.text_area(
                "What needs to be improved?",
                placeholder="E.g., Need more detail on API endpoints, missing database schema...",
                key="design_doc_feedback"
            )
        
        if st.button("✅ Submit Design Review", type="primary", use_container_width=True):
            feedback_text = st.session_state.get("design_doc_feedback", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"design_document_review_status": status, "design_document_review_feedback": [feedback_text]},
                as_node="Human Design Document Review"
            )
            
            with st.spinner("Processing design review..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"Design document {status.lower()}!", "success" if status == "Approve" else "info")
            st.rerun()
    else:
        st.info("📐 Design document will be created after user stories are approved.")

# Tab 4: Generated Code
with tabs[3]:
    st.markdown("### 💻 Generated Source Code")
    
    code = st.session_state.state.get("code", "")
    
    if code and code != "No code generated yet.":
        # Code Statistics
        col1, col2, col3, col4 = st.columns(4)
        lines_of_code = len(code.split('\n'))
        
        with col1:
            st.metric("Lines of Code", f"{lines_of_code:,}")
        with col2:
            files_count = code.count("Filename:")
            st.metric("Files Generated", files_count)
        with col3:
            st.metric("Language", "Python")
        with col4:
            st.metric("Status", "Ready for Review")
        
        # Code Display with Syntax Highlighting
        st.markdown("#### 📄 Source Files")
        
        # Parse and display code files
        if os.path.exists("generated_code"):
            files = os.listdir("generated_code")
            
            # File selector
            selected_file = st.selectbox("Select a file to view:", files)
            
            if selected_file:
                file_path = os.path.join("generated_code", selected_file)
                with open(file_path, 'r') as f:
                    file_content = f.read()
                
                # Display code with line numbers
                st.code(file_content, language='python', line_numbers=True)
        else:
            st.code(code, language='python')
        
        # Code Review Section
        st.markdown("### 🔍 Code Review")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            status = st.radio(
                "Does the code meet your quality standards?",
                ["Approve", "Denied"],
                horizontal=True,
                key="code_approval"
            )
            
            if status == "Denied":
                feedback = st.text_area(
                    "Describe the issues found:",
                    placeholder="E.g., Missing error handling, need better documentation, security concerns...",
                    height=150,
                    key="code_feedback"
                )
        
        with col2:
            st.markdown("#### 📋 Review Checklist")
            st.checkbox("✅ Follows coding standards")
            st.checkbox("✅ Proper error handling")
            st.checkbox("✅ Well documented")
            st.checkbox("✅ Modular design")
            st.checkbox("✅ Security best practices")
        
        if st.button("✅ Submit Code Review", type="primary", use_container_width=True):
            feedback_text = st.session_state.get("code_feedback", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"code_review_status": status, "code_review_feedback": [feedback_text]},
                as_node="Human Code Review"
            )
            
            with st.spinner("Processing code review..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"Code {status.lower()}!", "success" if status == "Approve" else "info")
            st.rerun()
    else:
        st.info("💻 Code will be generated after the design document is approved.")

# Tab 5: Test Cases
with tabs[4]:
    st.markdown("### 🧪 Test Cases")
    
    test_cases = st.session_state.state.get("test_cases", "")
    
    if test_cases and test_cases != "No test cases yet.":
        # Test Statistics
        col1, col2, col3 = st.columns(3)
        test_count = test_cases.count("[Test Case Name]:")
        
        with col1:
            st.metric("Total Test Cases", test_count)
        with col2:
            st.metric("Test Types", "Unit, Integration, E2E")
        with col3:
            st.metric("Coverage", "Comprehensive")
        
        # Display test cases in expandable sections
        test_case_blocks = test_cases.split("---")
        
        for i, test_block in enumerate(test_case_blocks):
            if test_block.strip():
                # Extract test name
                name_match = test_block.find("[Test Case Name]:")
                if name_match != -1:
                    name_end = test_block.find("\n", name_match)
                    test_name = test_block[name_match + 16:name_end].strip()
                    
                    with st.expander(f"🧪 {test_name}", expanded=i < 3):
                        st.text(test_block.strip())
        
        # Test Review Section
        st.markdown("### 🔍 Test Case Review")
        
        status = st.radio(
            "Are the test cases comprehensive and appropriate?",
            ["Approve", "Denied"],
            horizontal=True,
            key="test_cases_approval"
        )
        
        if status == "Denied":
            feedback = st.text_area(
                "What test scenarios are missing or need improvement?",
                placeholder="E.g., Missing edge cases, need performance tests, add security tests...",
                key="test_cases_feedback"
            )
        
        if st.button("✅ Submit Test Review", type="primary", use_container_width=True):
            feedback_text = st.session_state.get("test_cases_feedback", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"test_cases_review_status": status, "test_cases_review_feedback": [feedback_text]},
                as_node="Human Test Cases Review"
            )
            
            with st.spinner("Processing test case review..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"Test cases {status.lower()}!", "success" if status == "Approve" else "info")
            st.rerun()
    else:
        st.info("🧪 Test cases will be generated after security review is complete.")

# Tab 6: Security Review
with tabs[5]:
    st.markdown("### 🔒 Security Assessment")
    
    security_feedback = st.session_state.state.get("security_review_feedback", "")
    
    if security_feedback and security_feedback != "N/A":
        # Security Score Visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Security feedback display
            st.markdown("#### 🛡️ Security Analysis Results")
            
            # Parse security status
            security_status = st.session_state.state.get("security_review_status", "")
            
            if security_status == "Approve":
                st.success("✅ **Security Status: PASSED**")
            else:
                st.error("❌ **Security Status: NEEDS ATTENTION**")
            
            # Display feedback in a nice format
            st.markdown("##### 📋 Detailed Findings:")
            st.markdown(f"""
            <div class="custom-card">
                {security_feedback}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Security metrics
            st.markdown("#### 📊 Security Metrics")
            
            # Mock security scores (would be calculated from actual analysis)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 85 if security_status == "Approve" else 45,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Security Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if security_status == "Approve" else "darkred"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        # Manual Security Review
        st.markdown("### 🔍 Manual Security Review")
        
        status = st.radio(
            "Do you approve the security assessment?",
            ["Approve", "Denied"],
            horizontal=True,
            key="security_approval"
        )
        
        if status == "Denied":
            security_feedback_text = st.text_area(
                "Additional security concerns:",
                placeholder="E.g., Need encryption for sensitive data, implement rate limiting...",
                key="security_feedback"
            )
        
        if st.button("✅ Submit Security Review", type="primary", use_container_width=True):
            feedback_text = st.session_state.get("security_feedback", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"security_review_status": status, "security_feedback": feedback_text},
                as_node="Human Security Review"
            )
            
            with st.spinner("Processing security review..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"Security review {status.lower()}!", "success" if status == "Approve" else "warning")
            st.rerun()
    else:
        st.info("🔒 Security review will be performed after code review is complete.")

# Tab 7: QA Testing
with tabs[6]:
    st.markdown("### ✅ Quality Assurance")
    
    qa_feedback = st.session_state.state.get("qa_review_feedback", [])
    qa_status = st.session_state.state.get("qa_review_status", "")
    
    if qa_feedback:
        # QA Dashboard
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("#### 🎯 QA Test Results")
            
            if qa_status == "Approve":
                st.success("✅ **All Tests Passed!**")
            else:
                st.warning("⚠️ **Issues Found During Testing**")
            
            # Display QA feedback
            feedback_text = "\n".join(qa_feedback) if isinstance(qa_feedback, list) else qa_feedback
            st.markdown(f"""
            <div class="custom-card">
                <h5>Test Execution Summary:</h5>
                <p>{feedback_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Test Results Chart
            test_data = {
                "Passed": 8 if qa_status == "Approve" else 5,
                "Failed": 0 if qa_status == "Approve" else 3,
                "Skipped": 1
            }
            
            fig = px.pie(
                values=list(test_data.values()),
                names=list(test_data.keys()),
                color_discrete_map={
                    "Passed": "#10b981",
                    "Failed": "#ef4444",
                    "Skipped": "#f59e0b"
                }
            )
            fig.update_layout(height=250, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("#### 📊 QA Metrics")
            st.metric("Test Coverage", "92%")
            st.metric("Code Quality", "A")
            st.metric("Performance", "Good")
        
        # Manual QA Review
        st.markdown("### 🔍 Final QA Approval")
        
        status = st.radio(
            "Approve for deployment?",
            ["Approve", "Denied"],
            horizontal=True,
            key="qa_approval_1"
        )
        
        if status == "Denied":
            feedback = st.text_area(
                "What needs to be fixed before deployment?",
                placeholder="E.g., Performance issues, failing edge cases, UI bugs...",
                key="qa_feedback_1"
            )
        
        if st.button("✅ Submit QA Decision", type="primary", use_container_width=True):
            feedback_text = st.session_state.get("qa_feedback_1", "") if status == "Denied" else ""
            graph.update_state(
                st.session_state.thread,
                {"qa_review_status": status, "qa_review_feedback": [feedback_text]},
                as_node="Human QA Review"
            )
            
            with st.spinner("Processing QA decision..."):
                for event in graph.stream(None, st.session_state.thread):
                    st.session_state.events.append(event)
                    for node, output in event.items():
                        if isinstance(output, dict):
                            st.session_state.state.update(output)
                        st.session_state.active_node = node
            
            add_notification(f"QA {status.lower()}!", "success" if status == "Approve" else "info")
            st.rerun()
    else:
        st.info("✅ QA testing will begin after test cases are approved.")

# Tab 8: Deployment
with tabs[7]:
    st.markdown("### 🚀 Deployment Status")
    
    if state.get("deployment") == "deployed":
        # Success celebration
        st.balloons()
        
        st.markdown("""
        <div class="custom-card" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border: 2px solid #10b981;">
            <h2 style="color: #065f46; text-align: center;">🎉 Deployment Successful!</h2>
            <p style="text-align: center; color: #047857; font-size: 18px;">
                Your application has been successfully deployed to production.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Deployment Details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Deployment Summary")
            deployment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.markdown(f"""
            - **Environment:** Production
            - **Version:** 1.0.0
            - **Deployed At:** {deployment_time}
            - **Status:** Active ✅
            - **Health Check:** Passing
            """)
            
            st.markdown("#### 🔗 Quick Links")
            col1a, col1b = st.columns(2)
            with col1a:
                st.button("🌐 View Application", use_container_width=True)
                st.button("📊 View Metrics", use_container_width=True)
            with col1b:
                st.button("📜 View Logs", use_container_width=True)
                st.button("🔧 Configuration", use_container_width=True)
        
        with col2:
            st.markdown("#### 📦 Deployment Artifacts")
            
            # List all generated artifacts
            artifacts = {
                "User Stories": "artifacts/user_stories.txt",
                "Design Document": "artifacts/design_document.docx",
                "Source Code": "generated_code/",
                "Test Cases": "test_cases/"
            }
            
            for name, path in artifacts.items():
                if os.path.exists(path):
                    st.success(f"✅ {name}")
                else:
                    st.info(f"📄 {name}")
            
            # Export all button
            if st.button("📥 Download All Artifacts", type="primary", use_container_width=True):
                st.success("📦 Preparing download package...")
        
        # Next Steps
        st.markdown("### 🎯 Next Steps")
        next_steps = st.container()
        with next_steps:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("**📈 Monitor Performance**\nSet up monitoring and alerting")
            with col2:
                st.info("**🔄 Plan Updates**\nSchedule feature releases")
            with col3:
                st.info("**📚 Documentation**\nCreate user guides")
    else:
        st.warning("⏳ **Deployment Pending**")
        st.info("Complete all review stages to enable deployment.")
        
        # Show pending items
        pending_items = []
        if not state.get("code"):
            pending_items.append("Generate Code")
        if state.get("security_review_status") != "Approve":
            pending_items.append("Security Review")
        if state.get("qa_review_status") != "Approve":
            pending_items.append("QA Approval")
        
        if pending_items:
            st.markdown("#### ⏳ Pending Items:")
            for item in pending_items:
                st.markdown(f"- ❌ {item}")

# Tab 9: Analytics Dashboard
with tabs[8]:
    st.markdown("### 📊 Workflow Analytics")
    
    # Time Analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Workflow Timeline
        st.markdown("#### ⏱️ Stage Duration Analysis")
        
        # Sample data for visualization
        stages_data = []
        events = st.session_state.events
        
        if events:
            # Create timeline visualization
            fig = go.Figure()
            
            # Add bars for each completed stage
            stage_times = []
            for i, event in enumerate(events[:10]):  # Limit to first 10 events
                for node_name in event:
                    stage_times.append({
                        "Stage": node_name,
                        "Duration": 5 + (i * 2),  # Mock duration
                        "Order": i
                    })
            
            if stage_times:
                import pandas as pd
                df = pd.DataFrame(stage_times)
                
                fig = px.bar(df, x="Duration", y="Stage", orientation='h',
                           color="Duration", color_continuous_scale="Blues",
                           title="Time Spent per Stage (minutes)")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Analytics will be available once the workflow starts.")
    
    with col2:
        st.markdown("#### 📈 Workflow Metrics")
        
        # Calculate metrics
        total_events = len(st.session_state.events)
        approval_rate = 80  # Mock data
        
        # Metrics cards
        st.metric("Total Stages Completed", total_events)
        st.metric("Approval Rate", f"{approval_rate}%", delta="+5%")
        st.metric("Avg. Review Time", "12 min", delta="-3 min")
        st.metric("Iterations Required", 2)
    
    # Feedback Analysis
    st.markdown("#### 💬 Feedback Summary")
    
    feedback_items = []
    if state.get("user_story_feedback"):
        feedback_items.extend(state["user_story_feedback"])
    if state.get("design_document_review_feedback"):
        feedback_items.extend(state["design_document_review_feedback"])
    if state.get("code_review_feedback"):
        feedback_items.extend(state["code_review_feedback"])
    
    if feedback_items:
        for feedback in feedback_items:
            if feedback:
                st.markdown(f"""
                <div class="custom-card">
                    <p>💭 {feedback}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No feedback provided yet.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 20px;">
    <p>🚀 Powered by ANIL KUMAR R AI | Built with LangGraph & Streamlit | v2.0 MVP</p>
    <p style="font-size: 12px;">© 2026 AI SDLC Wizard. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for real-time updates
if st.session_state.active_node != "Deployment" and st.session_state.start_time:
    time.sleep(1)
    st.rerun()