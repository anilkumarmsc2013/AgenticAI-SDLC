# advanced_features.py
"""
Advanced features for the AI SDLC Wizard MVP
Premium functionality that elevates the user experience
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import re
import ast
import time

class AIInsights:
    """AI-powered insights and recommendations"""
    
    @staticmethod
    def analyze_requirements(requirements: str) -> Dict[str, Any]:
        """Analyze requirements and provide insights"""
        words = requirements.split()
        word_count = len(words)
        
        # Complexity analysis
        complexity_keywords = ['integration', 'real-time', 'scalable', 'distributed', 
                             'microservice', 'authentication', 'encryption', 'api']
        complexity_score = sum(1 for word in words if word.lower() in complexity_keywords)
        
        # Missing elements detection
        missing_elements = []
        requirement_lower = requirements.lower()
        
        checks = {
            'security': ['security', 'authentication', 'authorization', 'encryption'],
            'performance': ['performance', 'speed', 'optimization', 'cache'],
            'scalability': ['scalable', 'scale', 'load', 'concurrent'],
            'monitoring': ['monitoring', 'logging', 'metrics', 'alerts'],
            'testing': ['test', 'testing', 'quality', 'qa']
        }
        
        for category, keywords in checks.items():
            if not any(keyword in requirement_lower for keyword in keywords):
                missing_elements.append(category)
        
        # Project type detection
        project_types = {
            'web_app': ['web', 'website', 'portal', 'dashboard'],
            'api': ['api', 'rest', 'graphql', 'endpoint'],
            'mobile': ['mobile', 'ios', 'android', 'app'],
            'data': ['data', 'analytics', 'etl', 'pipeline'],
            'ml': ['machine learning', 'ml', 'ai', 'model']
        }
        
        detected_type = 'general'
        for ptype, keywords in project_types.items():
            if any(keyword in requirement_lower for keyword in keywords):
                detected_type = ptype
                break
        
        # Effort estimation (in story points)
        base_effort = word_count // 10
        complexity_multiplier = 1 + (complexity_score * 0.2)
        estimated_effort = int(base_effort * complexity_multiplier)
        
        # Risk analysis
        risks = []
        if 'real-time' in requirement_lower:
            risks.append("Real-time requirements may need special architecture")
        if 'integration' in requirement_lower:
            risks.append("Third-party integrations may have API limitations")
        if len(missing_elements) > 3:
            risks.append("Several key areas not specified - consider adding details")
        
        return {
            'word_count': word_count,
            'complexity_score': complexity_score,
            'complexity_level': 'High' if complexity_score > 5 else 'Medium' if complexity_score > 2 else 'Low',
            'missing_elements': missing_elements,
            'detected_type': detected_type,
            'estimated_effort': estimated_effort,
            'risks': risks,
            'recommendations': AIInsights._generate_recommendations(missing_elements, detected_type)
        }
    
    @staticmethod
    def _generate_recommendations(missing_elements: List[str], project_type: str) -> List[str]:
        """Generate smart recommendations based on analysis"""
        recommendations = []
        
        if 'security' in missing_elements:
            recommendations.append("Consider adding security requirements (authentication, data protection)")
        
        if 'performance' in missing_elements:
            recommendations.append("Define performance targets (response time, concurrent users)")
        
        if project_type == 'web_app':
            recommendations.append("Consider specifying browser compatibility and responsive design needs")
        elif project_type == 'api':
            recommendations.append("Define API rate limiting and documentation requirements")
        elif project_type == 'mobile':
            recommendations.append("Specify target platforms and offline capabilities")
        
        return recommendations


class CollaborationFeatures:
    """Team collaboration and sharing features"""
    
    @staticmethod
    def generate_shareable_link(session_id: str) -> str:
        """Generate a shareable link for the project"""
        # In production, this would create a real shareable URL
        base_url = "https://sdlc-wizard.app/shared/"
        hash_id = hashlib.md5(session_id.encode()).hexdigest()[:8]
        return f"{base_url}{hash_id}"
    
    @staticmethod
    def export_for_jira(state: Dict[str, Any]) -> Dict[str, Any]:
        """Format data for JIRA import"""
        jira_data = {
            "project": {
                "key": "SDLC",
                "name": "AI Generated Project"
            },
            "issues": []
        }
        
        # Convert user stories to JIRA issues
        for i, story in enumerate(state.get('user_stories', []), 1):
            jira_data["issues"].append({
                "issueType": "Story",
                "summary": f"User Story {i}",
                "description": story,
                "priority": "Medium",
                "labels": ["ai-generated", "sdlc-wizard"]
            })
        
        return jira_data
    
    @staticmethod
    def export_for_github(state: Dict[str, Any]) -> Dict[str, Any]:
        """Format data for GitHub import"""
        github_data = {
            "repository": {
                "name": "ai-generated-project",
                "description": state.get('requirements', '')[:200],
                "private": False
            },
            "issues": [],
            "wiki": []
        }
        
        # Create GitHub issues from user stories
        for i, story in enumerate(state.get('user_stories', []), 1):
            github_data["issues"].append({
                "title": f"Implement User Story {i}",
                "body": story,
                "labels": ["enhancement", "ai-generated"]
            })
        
        # Add design document to wiki
        if state.get('design_document'):
            github_data["wiki"].append({
                "title": "Design Document",
                "content": json.dumps(state['design_document'], indent=2)
            })
        
        return github_data


class CodeQualityAnalyzer:
    """Advanced code quality analysis"""
    
    @staticmethod
    def analyze_code_quality(code: str) -> Dict[str, Any]:
        """Perform deep code quality analysis"""
        lines = code.split('\n')
        
        # Basic metrics
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        blank_lines = len([l for l in lines if not l.strip()])
        
        # Complexity metrics
        functions = re.findall(r'def\s+(\w+)\s*\(', code)
        classes = re.findall(r'class\s+(\w+)\s*[\(:]', code)
        
        # Code smells detection
        code_smells = []
        
        # Check for long functions
        function_lengths = CodeQualityAnalyzer._get_function_lengths(code)
        for func_name, length in function_lengths.items():
            if length > 50:
                code_smells.append(f"Function '{func_name}' is too long ({length} lines)")
        
        # Check for TODO/FIXME comments
        todo_count = len(re.findall(r'#\s*(TODO|FIXME)', code, re.IGNORECASE))
        if todo_count > 0:
            code_smells.append(f"Found {todo_count} TODO/FIXME comments")
        
        # Security checks
        security_issues = []
        
        # Check for hardcoded secrets
        if re.search(r'(password|secret|key)\s*=\s*["\'].*["\']', code, re.IGNORECASE):
            security_issues.append("Possible hardcoded secrets detected")
        
        # Check for SQL injection vulnerabilities
        if re.search(r'(execute|query)\s*\(\s*["\'].*%s.*["\']', code):
            security_issues.append("Potential SQL injection vulnerability")
        
        # Calculate quality score
        quality_score = 100
        quality_score -= len(code_smells) * 5
        quality_score -= len(security_issues) * 10
        quality_score -= (todo_count * 2)
        quality_score = max(0, quality_score)
        
        # Maintainability index
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        maintainability = min(100, 50 + (comment_ratio * 100) + (10 if len(functions) < 20 else 0))
        
        return {
            'metrics': {
                'total_lines': total_lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'functions': len(functions),
                'classes': len(classes),
                'comment_ratio': f"{comment_ratio:.1%}"
            },
            'quality_score': quality_score,
            'maintainability_index': int(maintainability),
            'code_smells': code_smells,
            'security_issues': security_issues,
            'recommendations': CodeQualityAnalyzer._get_recommendations(quality_score, code_smells, security_issues)
        }
    
    @staticmethod
    def _get_function_lengths(code: str) -> Dict[str, int]:
        """Calculate the length of each function"""
        function_lengths = {}
        lines = code.split('\n')
        
        current_function = None
        indent_level = 0
        
        for i, line in enumerate(lines):
            if re.match(r'def\s+(\w+)\s*\(', line):
                match = re.match(r'def\s+(\w+)\s*\(', line)
                current_function = match.group(1)
                function_lengths[current_function] = 0
                indent_level = len(line) - len(line.lstrip())
            elif current_function and line.strip():
                current_indent = len(line) - len(line.lstrip())
                if current_indent > indent_level:
                    function_lengths[current_function] += 1
                else:
                    current_function = None
        
        return function_lengths
    
    @staticmethod
    def _get_recommendations(score: int, smells: List[str], security: List[str]) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if score < 70:
            recommendations.append("Consider refactoring to improve code quality")
        
        if len(smells) > 0:
            recommendations.append("Address code smells to improve maintainability")
        
        if len(security) > 0:
            recommendations.append("Fix security issues before deployment")
        
        if score >= 90:
            recommendations.append("Excellent code quality! Ready for production")
        
        return recommendations


class PerformanceMonitor:
    """Monitor and visualize workflow performance"""
    
    @staticmethod
    def create_performance_dashboard(events: List[Dict], start_time: datetime) -> go.Figure:
        """Create a comprehensive performance dashboard"""
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Stage Duration', 'Cumulative Progress', 
                          'Resource Usage', 'Success Rate'),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                   [{'type': 'indicator'}, {'type': 'pie'}]]
        )
        
        # Mock data for demonstration
        stages = ['Requirements', 'Stories', 'Design', 'Code', 'Test', 'Deploy']
        durations = [2, 5, 8, 15, 10, 3]
        cumulative = np.cumsum(durations)
        
        # Stage Duration Bar Chart
        fig.add_trace(
            go.Bar(x=stages, y=durations, name='Duration (min)',
                   marker_color='lightblue'),
            row=1, col=1
        )
        
        # Cumulative Progress Line Chart
        fig.add_trace(
            go.Scatter(x=stages, y=cumulative, mode='lines+markers',
                      name='Progress', line=dict(color='green', width=3)),
            row=1, col=2
        )
        
        # Resource Usage Gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=75,
                title={'text': "CPU Usage %"},
                gauge={'axis': {'range': [0, 100]},
                      'bar': {'color': "darkblue"},
                      'steps': [
                          {'range': [0, 50], 'color': "lightgray"},
                          {'range': [50, 80], 'color': "yellow"},
                          {'range': [80, 100], 'color': "red"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                  'thickness': 0.75, 'value': 90}}),
            row=2, col=1
        )
        
        # Success Rate Pie Chart
        fig.add_trace(
            go.Pie(labels=['Successful', 'Failed'], values=[85, 15],
                   marker_colors=['green', 'red']),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(height=600, showlegend=False,
                         title_text="Workflow Performance Dashboard")
        
        return fig


class SmartSuggestions:
    """AI-powered smart suggestions throughout the workflow"""
    
    @staticmethod
    def suggest_improvements(stage: str, content: Any) -> List[str]:
        """Provide context-aware suggestions"""
        suggestions = []
        
        if stage == "requirements":
            # Analyze requirements and suggest improvements
            if isinstance(content, str):
                if len(content.split()) < 50:
                    suggestions.append("💡 Add more detail about user roles and permissions")
                if 'api' in content.lower() and 'documentation' not in content.lower():
                    suggestions.append("💡 Consider adding API documentation requirements")
                if 'data' in content.lower() and 'backup' not in content.lower():
                    suggestions.append("💡 Don't forget to specify backup and recovery needs")
        
        elif stage == "user_stories":
            # Suggest missing user stories
            if isinstance(content, list):
                stories_text = ' '.join(content).lower()
                if 'admin' not in stories_text:
                    suggestions.append("💡 Consider adding admin user stories")
                if 'error' not in stories_text:
                    suggestions.append("💡 Add stories for error handling scenarios")
        
        elif stage == "code":
            # Suggest code improvements
            if isinstance(content, str):
                if 'try:' not in content:
                    suggestions.append("💡 Add exception handling for robustness")
                if 'logging' not in content:
                    suggestions.append("💡 Implement logging for better debugging")
                if 'test' not in content:
                    suggestions.append("💡 Consider adding unit tests")
        
        return suggestions[:3]  # Limit to 3 suggestions


class AutomationEngine:
    """Advanced automation features"""
    
    @staticmethod
    def auto_generate_documentation(state: Dict[str, Any]) -> str:
        """Generate comprehensive documentation automatically"""
        doc = f"""# Project Documentation

## Overview
{state.get('requirements', 'No requirements specified')}

## User Stories
{chr(10).join([f"{i}. {story}" for i, story in enumerate(state.get('user_stories', []), 1)])}

## Technical Architecture
{json.dumps(state.get('design_document', {}), indent=2)}

## Implementation Status
- Code Generated: {'Yes' if state.get('code') else 'No'}
- Tests Written: {'Yes' if state.get('test_cases') else 'No'}
- Security Reviewed: {state.get('security_review_status', 'Pending')}
- QA Status: {state.get('qa_review_status', 'Pending')}
- Deployment: {state.get('deployment', 'Not deployed')}

## Generated Files
- User Stories: artifacts/user_stories.txt
- Design Document: artifacts/design_document.docx
- Source Code: generated_code/
- Test Cases: test_cases/

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return doc
    
    @staticmethod
    def estimate_project_timeline(state: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate project timeline based on complexity"""
        # Analyze complexity
        requirements = state.get('requirements', '')
        word_count = len(requirements.split())
        stories_count = len(state.get('user_stories', []))
        
        # Base estimates (in days)
        estimates = {
            'Development': max(5, stories_count * 2),
            'Testing': max(3, stories_count),
            'Documentation': 2,
            'Deployment': 1,
            'Buffer': max(2, stories_count // 2)
        }
        
        total_days = sum(estimates.values())
        
        # Create timeline
        start_date = datetime.now()
        timeline = {}
        current_date = start_date
        
        for phase, days in estimates.items():
            timeline[phase] = {
                'start': current_date.strftime('%Y-%m-%d'),
                'end': (current_date + timedelta(days=days)).strftime('%Y-%m-%d'),
                'duration': days
            }
            current_date += timedelta(days=days)
        
        return {
            'total_days': total_days,
            'total_weeks': round(total_days / 5, 1),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': current_date.strftime('%Y-%m-%d'),
            'phases': timeline,
            'confidence': 'High' if word_count > 100 else 'Medium'
        }


# Integration function for the main app
def show_advanced_features(tab_container, state):
    """Display advanced features in the main app"""
    
    # AI Insights Section
    if state.get('requirements'):
        st.markdown("### 🤖 AI-Powered Insights")
        insights = AIInsights.analyze_requirements(state['requirements'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Complexity", insights['complexity_level'], 
                     f"Score: {insights['complexity_score']}")
        with col2:
            st.metric("Estimated Effort", f"{insights['estimated_effort']} pts")
        with col3:
            st.metric("Project Type", insights['detected_type'].replace('_', ' ').title())
        
        # Recommendations
        if insights['recommendations']:
            st.info("**💡 AI Recommendations:**\n" + 
                   "\n".join([f"- {rec}" for rec in insights['recommendations']]))
        
        # Risks
        if insights['risks']:
            st.warning("**⚠️ Identified Risks:**\n" + 
                      "\n".join([f"- {risk}" for risk in insights['risks']]))
    
    # Code Quality Analysis
    if state.get('code'):
        st.markdown("### 📊 Code Quality Analysis")
        quality = CodeQualityAnalyzer.analyze_code_quality(state['code'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Quality Score", f"{quality['quality_score']}/100",
                     delta=f"{quality['quality_score']-70}")
        with col2:
            st.metric("Maintainability", f"{quality['maintainability_index']}/100")
        with col3:
            st.metric("Security Issues", len(quality['security_issues']),
                     delta=f"-{len(quality['security_issues'])}" if quality['security_issues'] else "0")
        
        # Detailed metrics
        with st.expander("📈 Detailed Metrics"):
            metrics_df = pd.DataFrame([quality['metrics']]).T
            metrics_df.columns = ['Value']
            st.dataframe(metrics_df)
        
        # Issues
        if quality['code_smells'] or quality['security_issues']:
            st.error("**Issues Found:**")
            for smell in quality['code_smells']:
                st.markdown(f"- 🔸 {smell}")
            for issue in quality['security_issues']:
                st.markdown(f"- 🔴 {issue}")
    
    # Project Timeline
    if state.get('requirements'):
        st.markdown("### 📅 Project Timeline Estimation")
        timeline = AutomationEngine.estimate_project_timeline(state)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Duration", f"{timeline['total_weeks']} weeks")
            st.metric("Confidence Level", timeline['confidence'])
        
        with col2:
            # Timeline visualization
            phases_df = pd.DataFrame(timeline['phases']).T
            phases_df['duration'] = phases_df['duration'].astype(int)
            
            fig = go.Figure(data=[
                go.Bar(x=phases_df.index, y=phases_df['duration'],
                      text=phases_df['duration'],
                      textposition='auto',
                      marker_color='lightblue')
            ])
            fig.update_layout(title="Phase Duration (days)", height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Collaboration Features
    st.markdown("### 🤝 Collaboration & Export")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Export to JIRA", use_container_width=True):
            jira_data = CollaborationFeatures.export_for_jira(state)
            st.download_button(
                "Download JIRA Import File",
                json.dumps(jira_data, indent=2),
                "jira_import.json",
                "application/json"
            )
    
    with col2:
        if st.button("🐙 Export to GitHub", use_container_width=True):
            github_data = CollaborationFeatures.export_for_github(state)
            st.download_button(
                "Download GitHub Import File",
                json.dumps(github_data, indent=2),
                "github_import.json",
                "application/json"
            )
    
    with col3:
        if st.button("🔗 Get Shareable Link", use_container_width=True):
            link = CollaborationFeatures.generate_shareable_link(
                st.session_state.thread["configurable"]["thread_id"]
            )
            st.code(link)
            st.caption("Share this link with your team!")


# Export all advanced features
__all__ = [
    'AIInsights',
    'CollaborationFeatures',
    'CodeQualityAnalyzer',
    'PerformanceMonitor',
    'SmartSuggestions',
    'AutomationEngine',
    'show_advanced_features'
]