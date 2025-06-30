# Contributing to Sofia-AI

Thank you for your interest in contributing to Sofia-AI! 🤖 We welcome contributions from developers, AI researchers, legal professionals, and domain experts.

## 🌟 Ways to Contribute

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new capabilities and improvements  
- **💻 Code Contributions**: Submit pull requests for fixes and features
- **📚 Documentation**: Improve guides, tutorials, and API docs
- **🌍 Localization**: Add support for additional languages
- **🧪 Testing**: Help improve test coverage and quality
- **🔧 Integrations**: Build connectors for new platforms

## 🚀 Getting Started

### **Prerequisites**
- Python 3.11+
- Git and GitHub account
- Basic understanding of AI/ML concepts
- Familiarity with FastAPI and LangChain (helpful but not required)

### **Development Setup**
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/your-username/sofia-ai.git
cd sofia-ai

# 3. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Install pre-commit hooks
pre-commit install

# 6. Copy environment template
cp .env.example .env
# Edit .env with your configuration

# 7. Run tests to verify setup
python -m pytest
```

## 🔧 Development Workflow

### **1. Create a Feature Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### **2. Make Your Changes**
- Follow our coding standards (see below)
- Write tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### **3. Code Quality Checks**
```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
mypy app/

# Run tests
python -m pytest tests/ -v --cov=app
```

### **4. Commit Your Changes**
```bash
git add .
git commit -m "feat: add new language detection algorithm"
```

We follow [Conventional Commits](https://conventionalcommits.org/):
- `feat:` new features
- `fix:` bug fixes  
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding/updating tests
- `chore:` maintenance tasks

### **5. Submit a Pull Request**
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots/demos if applicable
- Updated tests and documentation

## 📋 Coding Standards

### **Python Code Style**
- **PEP 8** compliance with Black formatting
- **Type hints** for all function parameters and returns
- **Docstrings** for all public functions and classes
- **Maximum line length**: 88 characters (Black default)

### **Code Example**
```python
from typing import Optional, Dict, Any
from pydantic import BaseModel

class UserMessage(BaseModel):
    """Represents a message from a user.
    
    Args:
        phone: User's phone number in international format
        body: Message content
        language: Detected or specified language code
        metadata: Optional additional context
    """
    phone: str
    body: str
    language: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

async def process_message(message: UserMessage) -> Dict[str, str]:
    """Process an incoming user message and generate a response.
    
    Args:
        message: The user message to process
        
    Returns:
        Dict containing the generated response and metadata
        
    Raises:
        ValidationError: If message format is invalid
        AIProcessingError: If AI processing fails
    """
    # Implementation here
    pass
```

### **Testing Standards**
- **Minimum 90% test coverage** for new code
- **Unit tests** for individual functions
- **Integration tests** for API endpoints
- **Mock external services** (OpenAI, Twilio, etc.)
- **Test naming**: `test_function_name_expected_behavior`

### **Documentation Standards**
- **Clear, concise comments** for complex logic
- **README updates** for new features
- **API documentation** using FastAPI automatic docs
- **Inline code comments** for business logic

## 🧪 Testing Guidelines

### **Running Tests**
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_chains.py -v

# Run tests matching pattern
python -m pytest -k "test_language_detection"
```

### **Test Categories**
- **Unit Tests**: `tests/unit/` - Individual function testing
- **Integration Tests**: `tests/integration/` - API and service testing  
- **Performance Tests**: `tests/performance/` - Load and speed testing
- **End-to-End Tests**: `tests/e2e/` - Complete workflow testing

### **Writing Good Tests**
```python
import pytest
from unittest.mock import Mock, patch
from app.chains.detect_language import detect_language

class TestLanguageDetection:
    """Test suite for language detection functionality."""
    
    @pytest.mark.asyncio
    async def test_detect_language_italian_text(self):
        """Should correctly identify Italian text."""
        # Arrange
        text = "Ciao, ho bisogno di aiuto con il permesso di soggiorno"
        mock_llm = Mock()
        mock_llm.invoke.return_value.content = "it"
        
        # Act
        result = detect_language(text, mock_llm)
        
        # Assert
        assert result == "it"
        mock_llm.invoke.assert_called_once()
        
    @pytest.mark.parametrize("text,expected", [
        ("Hello, I need help", "en"),
        ("Bonjour, j'ai besoin d'aide", "fr"),
        ("Hola, necesito ayuda", "es"),
    ])
    async def test_detect_language_multiple_languages(self, text, expected):
        """Should correctly identify multiple languages."""
        # Test implementation here
        pass
```

## 🌍 Internationalization

### **Adding New Languages**
1. **Update language configuration** in `app/utils/language_detection.py`
2. **Add language code** to `SUPPORTED_LANGUAGES` 
3. **Create test cases** for the new language
4. **Update documentation** and README

### **Language Code Standards**
- Use **ISO 639-1** codes (e.g., `en`, `fr`, `it`)
- For regional variants, use **ISO 639-1 + ISO 3166-1** (e.g., `en-US`, `fr-CA`)

## 🔒 Security Guidelines

### **Security Best Practices**
- **Never commit secrets** or API keys
- **Validate all inputs** from external sources
- **Sanitize user content** before processing
- **Use parameterized queries** for database operations
- **Follow OWASP guidelines** for web security

### **Reporting Security Issues**
Please **DO NOT** create public issues for security vulnerabilities. Instead:
1. Email `security@sofia-ai.com`
2. Include detailed description and reproduction steps
3. Allow 90 days for response before public disclosure

## 📦 Release Process

### **Version Management**
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### **Release Checklist**
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version bumped in `__init__.py`
- [ ] CHANGELOG.md updated
- [ ] Security review completed
- [ ] Performance benchmarks run

## 🏷️ Issue Labels

We use the following labels for organization:

### **Type Labels**
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to docs
- `performance` - Performance improvements
- `security` - Security-related issues

### **Priority Labels**  
- `priority: high` - Critical issues
- `priority: medium` - Important improvements
- `priority: low` - Nice-to-have features

### **Component Labels**
- `component: ai` - AI/ML related
- `component: api` - API endpoints
- `component: ui` - User interface
- `component: database` - Data storage
- `component: deployment` - DevOps/deployment

## 🤝 Community Guidelines

### **Code of Conduct**
We are committed to providing a welcoming and inclusive environment. Please:
- **Be respectful** and professional in all interactions
- **Be inclusive** and considerate of different perspectives
- **Be collaborative** and help others learn and grow
- **Be patient** with newcomers and questions

### **Communication Channels**
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time community discussion
- **Email**: Direct communication with maintainers

## 🏆 Recognition

Contributors who make significant contributions will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Invited to join the core team** (for ongoing contributors)
- **Eligible for bounties** on priority issues

## 📞 Getting Help

### **Development Questions**
- Check existing **GitHub Issues** and **Discussions**
- Join our **Discord community** for real-time help
- Email `developers@sofia-ai.com` for specific questions

### **Before You Start**
1. **Search existing issues** to avoid duplicates
2. **Read the documentation** thoroughly
3. **Check our roadmap** to align with project direction
4. **Discuss major changes** before implementing

---

## 🙏 Thank You!

Every contribution makes Sofia-AI better for everyone. Whether you're fixing a typo, adding a feature, or reporting a bug, your help is invaluable to our mission of transforming professional service communication with AI.

**Happy coding!** 🚀

---

*This contributing guide is inspired by open-source best practices and is continuously updated based on community feedback.* 