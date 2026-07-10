# config.py
"""
Configuration settings for the AI SDLC Wizard MVP
"""

import os
from typing import Dict, List, Any

class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = "AI SDLC Wizard - Enterprise Edition"
    APP_VERSION = "2.0.0"
    APP_ICON = "🚀"
    
    # UI Configuration
    THEME_COLORS = {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    # Workflow Configuration
    WORKFLOW_STAGES = [
        {
            "name": "User Requirements",
            "icon": "📋",
            "description": "Define project requirements",
            "type": "input"
        },
        {
            "name": "Auto-generate User Stories",
            "icon": "🤖",
            "description": "AI generates user stories",
            "type": "ai"
        },
        {
            "name": "Human User Story Approval",
            "icon": "👥",
            "description": "Review and approve stories",
            "type": "human"
        },
        {
            "name": "Create Design Document",
            "icon": "📐",
            "description": "Generate technical design",
            "type": "ai"
        },
        {
            "name": "Human Design Document Review",
            "icon": "🔍",
            "description": "Review design document",
            "type": "human"
        },
        {
            "name": "Generate Code",
            "icon": "💻",
            "description": "AI writes the code",
            "type": "ai"
        },
        {
            "name": "Human Code Review",
            "icon": "👨‍💻",
            "description": "Review generated code",
            "type": "human"
        },
        {
            "name": "Security Review",
            "icon": "🔒",
            "description": "Automated security check",
            "type": "ai"
        },
        {
            "name": "Human Security Review",
            "icon": "🛡️",
            "description": "Manual security review",
            "type": "human"
        },
        {
            "name": "Write Test Cases",
            "icon": "🧪",
            "description": "Generate test cases",
            "type": "ai"
        },
        {
            "name": "Human Test Cases Review",
            "icon": "✔️",
            "description": "Review test cases",
            "type": "human"
        },
        {
            "name": "QA Testing",
            "icon": "🎯",
            "description": "Run quality assurance",
            "type": "ai"
        },
        {
            "name": "Human QA Review",
            "icon": "✅",
            "description": "Final QA approval",
            "type": "human"
        },
        {
            "name": "Deployment",
            "icon": "🚀",
            "description": "Deploy to production",
            "type": "deployment"
        }
    ]
    
    # File Paths
    ARTIFACTS_DIR = "artifacts"
    CODE_OUTPUT_DIR = "generated_code"
    TEST_CASES_DIR = "test_cases"
    EXPORTS_DIR = "exports"
    
    # LLM Settings
    DEFAULT_LLM_MODEL = "gemma2-9b-it"
    AVAILABLE_MODELS = [
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]
    
    # Validation Settings
    MIN_REQUIREMENT_WORDS = 10
    RECOMMENDED_REQUIREMENT_WORDS = 50
    MAX_REQUIREMENT_WORDS = 1000
    
    # Export Settings
    EXPORT_FORMATS = ["PDF", "Word", "ZIP", "JSON"]
    PDF_PAGE_SIZE = "letter"  # or "A4"
    
    # Notification Settings
    NOTIFICATION_DURATION = 3  # seconds
    MAX_NOTIFICATIONS = 10
    
    # Analytics Settings
    ENABLE_ANALYTICS = True
    TRACK_TIMING = True
    TRACK_ERRORS = True
    
    # Security Settings
    ENABLE_SECURITY_SCAN = True
    SECURITY_RULES = [
        "no_hardcoded_secrets",
        "input_validation",
        "sql_injection_prevention",
        "xss_prevention",
        "authentication_required",
        "authorization_checks",
        "encryption_for_sensitive_data"
    ]
    
    # Performance Settings
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # 1 hour
    MAX_CONCURRENT_REQUESTS = 5
    
    # Feature Flags
    FEATURES = {
        "dark_mode": True,
        "export_analytics": True,
        "advanced_code_analysis": True,
        "auto_save": True,
        "collaboration": False,  # Future feature
        "version_control": False,  # Future feature
        "ci_cd_integration": False,  # Future feature
        "custom_templates": True,
        "ai_suggestions": True,
        "real_time_updates": True
    }
    
    # Templates
    REQUIREMENT_TEMPLATES = {
        "E-commerce Platform": {
            "description": "Online shopping platform with full e-commerce capabilities",
            "template": """Create an e-commerce platform with the following features:
- User authentication and profile management
- Product catalog with categories and search
- Shopping cart and wishlist functionality
- Secure payment processing with multiple payment methods
- Order management and tracking
- Admin dashboard for inventory and sales management
- Email notifications for order updates
- Mobile-responsive design
- Product reviews and ratings
- Recommendation engine"""
        },
        "SaaS Dashboard": {
            "description": "Analytics dashboard for Software-as-a-Service applications",
            "template": """Build a SaaS analytics dashboard with:
- Multi-tenant architecture with organization management
- User roles and permissions (Admin, Manager, Viewer)
- Real-time data visualization with charts and graphs
- Custom dashboard creation and widget management
- Data export in multiple formats (CSV, Excel, PDF)
- API integration for data ingestion
- Automated reporting and alerts
- Audit logs and activity tracking
- Billing and subscription management
- Two-factor authentication"""
        },
        "Mobile App Backend": {
            "description": "RESTful API backend for mobile applications",
            "template": """Develop a REST API backend for a mobile app with:
- JWT-based authentication and token refresh
- User profile management with avatar upload
- Push notification service integration
- Real-time chat/messaging functionality
- Social media integration (login and sharing)
- Geolocation services and mapping
- File upload and media management
- Offline data synchronization
- Rate limiting and API throttling
- Comprehensive API documentation"""
        },
        "API Service": {
            "description": "Microservice API with enterprise features",
            "template": """Create a microservice API with:
- RESTful endpoints following OpenAPI specification
- CRUD operations for core entities
- Advanced filtering, sorting, and pagination
- API key authentication and OAuth2 support
- Rate limiting per user/API key
- Request/response validation
- Error handling with proper HTTP status codes
- API versioning support
- Webhook functionality for event notifications
- Health check and monitoring endpoints"""
        }
    }
    
    @classmethod
    def get_stage_by_name(cls, name: str) -> Dict[str, Any]:
        """Get workflow stage configuration by name"""
        for stage in cls.WORKFLOW_STAGES:
            if stage["name"] == name:
                return stage
        return None
    
    @classmethod
    def is_feature_enabled(cls, feature: str) -> bool:
        """Check if a feature is enabled"""
        return cls.FEATURES.get(feature, False)
    
    @classmethod
    def get_theme_color(cls, color_type: str) -> str:
        """Get theme color by type"""
        return cls.THEME_COLORS.get(color_type, "#000000")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [
            cls.ARTIFACTS_DIR,
            cls.CODE_OUTPUT_DIR,
            cls.TEST_CASES_DIR,
            cls.EXPORTS_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Environment-specific overrides
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    CACHE_ENABLED = False
    TRACK_ERRORS = True


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    CACHE_ENABLED = True
    TRACK_ERRORS = True
    MAX_CONCURRENT_REQUESTS = 20


# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("APP_ENV", "development")
    
    if env == "production":
        return ProductionConfig
    else:
        return DevelopmentConfig


# Export the active configuration
ActiveConfig = get_config()