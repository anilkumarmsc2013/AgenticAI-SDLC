# ui_utils.py
"""
Utility functions for enhanced UI components and features
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import zipfile
from pathlib import Path
import shutil
from docx import Document
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class WorkflowAnalytics:
    """Analytics and visualization utilities for the SDLC workflow"""
    
    @staticmethod
    def create_workflow_gantt(events, start_time):
        """Create a Gantt chart of the workflow stages"""
        if not events or not start_time:
            return None
        
        tasks = []
        current_time = start_time
        
        for i, event in enumerate(events):
            for node_name in event:
                duration = timedelta(minutes=5 + (i * 2))  # Mock duration
                tasks.append({
                    'Task': node_name,
                    'Start': current_time,
                    'Finish': current_time + duration,
                    'Resource': 'AI' if 'Auto' in node_name or 'Generate' in node_name else 'Human'
                })
                current_time += duration
        
        df = pd.DataFrame(tasks)
        
        fig = px.timeline(
            df, 
            x_start="Start", 
            x_end="Finish", 
            y="Task",
            color="Resource",
            title="Workflow Timeline",
            color_discrete_map={'AI': '#667eea', 'Human': '#764ba2'}
        )
        
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def create_approval_funnel(state):
        """Create a funnel chart showing approval rates"""
        stages = [
            ('Requirements', 100),
            ('User Stories', 90 if state.get('user_story_status') == 'Approve' else 70),
            ('Design Document', 80 if state.get('design_document_review_status') == 'Approve' else 60),
            ('Code Review', 70 if state.get('code_review_status') == 'Approve' else 50),
            ('Security', 60 if state.get('security_review_status') == 'Approve' else 40),
            ('QA Testing', 50 if state.get('qa_review_status') == 'Approve' else 30),
            ('Deployment', 40 if state.get('deployment') == 'deployed' else 0)
        ]
        
        fig = go.Figure(go.Funnel(
            y=[s[0] for s in stages],
            x=[s[1] for s in stages],
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": ["#667eea", "#7c3aed", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#ede9fe"]},
        ))
        
        fig.update_layout(title="Workflow Progress Funnel", height=400)
        return fig
    
    @staticmethod
    def create_code_complexity_chart(code):
        """Analyze and visualize code complexity"""
        if not code:
            return None
        
        # Simple complexity metrics
        lines = code.split('\n')
        metrics = {
            'Total Lines': len(lines),
            'Code Lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'Comment Lines': len([l for l in lines if l.strip().startswith('#')]),
            'Functions': code.count('def '),
            'Classes': code.count('class '),
            'Imports': len([l for l in lines if l.strip().startswith(('import ', 'from '))]),
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color=['#667eea', '#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe']
            )
        ])
        
        fig.update_layout(
            title="Code Metrics Analysis",
            xaxis_title="Metric",
            yaxis_title="Count",
            height=300
        )
        
        return fig


class ExportManager:
    """Handle exporting of artifacts in various formats"""
    
    @staticmethod
    def export_to_pdf(state, filename="sdlc_report.pdf"):
        """Export complete SDLC report to PDF"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        story.append(Paragraph("AI SDLC Workflow Report", title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Metadata
        metadata = [
            ['Generated Date:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Session ID:', st.session_state.thread["configurable"]["thread_id"][:8]],
            ['Status:', 'Completed' if state.get('deployment') == 'deployed' else 'In Progress']
        ]
        
        t = Table(metadata)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(t)
        story.append(Spacer(1, 0.5*inch))
        
        # Requirements
        story.append(Paragraph("Requirements", styles['Heading2']))
        story.append(Paragraph(state.get('requirements', 'No requirements specified'), styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # User Stories
        if state.get('user_stories'):
            story.append(Paragraph("User Stories", styles['Heading2']))
            for i, story_text in enumerate(state['user_stories'], 1):
                story.append(Paragraph(f"{i}. {story_text}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        return filename
    
    @staticmethod
    def export_all_artifacts(state):
        """Create a ZIP file with all artifacts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"sdlc_artifacts_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Add existing artifact files
            artifact_paths = [
                "artifacts/user_stories.txt",
                "artifacts/design_document.docx",
            ]
            
            for path in artifact_paths:
                if os.path.exists(path):
                    zipf.write(path, os.path.basename(path))
            
            # Add generated code
            if os.path.exists("generated_code"):
                for root, dirs, files in os.walk("generated_code"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, ".")
                        zipf.write(file_path, arcname)
            
            # Add test cases
            if os.path.exists("test_cases"):
                for root, dirs, files in os.walk("test_cases"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, ".")
                        zipf.write(file_path, arcname)
            
            # Create and add summary JSON
            summary = {
                "session_id": st.session_state.thread["configurable"]["thread_id"],
                "timestamp": timestamp,
                "requirements": state.get("requirements", ""),
                "status": "deployed" if state.get("deployment") == "deployed" else "in_progress",
                "statistics": {
                    "user_stories_count": len(state.get("user_stories", [])),
                    "files_generated": len(os.listdir("generated_code")) if os.path.exists("generated_code") else 0,
                    "test_cases_count": len(os.listdir("test_cases")) if os.path.exists("test_cases") else 0,
                }
            }
            
            zipf.writestr("summary.json", json.dumps(summary, indent=2))
        
        return zip_filename


class NotificationManager:
    """Enhanced notification system with persistence and styling"""
    
    @staticmethod
    def show_notification(message, type="info", duration=3):
        """Display a styled notification"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        colors = {
            "info": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
        
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 80px;
            right: 20px;
            background: white;
            border-left: 4px solid {colors.get(type, colors['info'])};
            padding: 16px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        ">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 20px; margin-right: 10px;">{icons.get(type, icons['info'])}</span>
                <span style="font-weight: 500;">{message}</span>
            </div>
        </div>
        
        <style>
        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def clear_old_notifications():
        """Remove notifications older than 30 seconds"""
        if 'notifications' in st.session_state:
            cutoff_time = datetime.now() - timedelta(seconds=30)
            st.session_state.notifications = [
                n for n in st.session_state.notifications 
                if n['timestamp'] > cutoff_time
            ]


class ThemeManager:
    """Handle theme switching and custom styling"""
    
    @staticmethod
    def apply_dark_theme():
        """Apply dark theme styles"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        .custom-card {
            background: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        .main-header {
            background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background: #2d2d2d !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_light_theme():
        """Apply light theme styles (default)"""
        pass  # Light theme is already the default


class ValidationHelper:
    """Input validation and error handling utilities"""
    
    @staticmethod
    def validate_requirements(requirements):
        """Validate user requirements input"""
        errors = []
        warnings = []
        
        word_count = len(requirements.split())
        
        if word_count < 10:
            errors.append("Requirements must be at least 10 words long")
        elif word_count < 50:
            warnings.append("Consider adding more detail for better results (50+ words recommended)")
        
        if word_count > 1000:
            warnings.append("Requirements are very long. Consider breaking into phases.")
        
        # Check for common missing elements
        elements_to_check = {
            'user': "Consider mentioning user roles or personas",
            'feature': "Include specific features or functionality",
            'data': "Mention data or database requirements if applicable",
            'security': "Consider mentioning security requirements",
            'performance': "Include performance requirements if relevant"
        }
        
        requirements_lower = requirements.lower()
        for key, suggestion in elements_to_check.items():
            if key not in requirements_lower:
                warnings.append(suggestion)
        
        return errors, warnings[:3]  # Limit warnings to 3
    
    @staticmethod
    def validate_code_syntax(code):
        """Basic Python syntax validation"""
        try:
            compile(code, '<string>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"


# Export all utilities
__all__ = [
    'WorkflowAnalytics',
    'ExportManager',
    'NotificationManager',
    'ThemeManager',
    'ValidationHelper'
]