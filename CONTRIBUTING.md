# Contributing to QuantumFacts

First off, thank you for considering contributing to QuantumFacts! ❤️ It's people like you that make open source projects great.

## Code of Conduct

This project and everyone participating in it is governed by respect, kindness, and collaboration. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, etc.)
- **Describe the behavior you observed** and what you expected
- **Include your environment details**:
  - OS and version
  - Python version
  - FFmpeg version
  - Package versions (`pip list`)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar features** in other projects

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes**:
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation
3. **Test your changes** thoroughly
4. **Commit your changes** with clear messages
5. **Push to your fork** and submit a pull request

#### Pull Request Guidelines

- Follow PEP 8 style guide for Python code
- Write clear, concise commit messages
- Update README.md if needed
- Add tests for new features
- Keep pull requests focused (one feature/fix per PR)

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/QuantumFacts.git
cd QuantumFacts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Check code style
flake8 src/
black --check src/
```

## Style Guide

### Python Code

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add type hints where helpful

```python
def generate_script(fact: str, max_length: int = 150) -> Dict[str, Any]:
    """
    Generate an engaging script from a fact.
    
    Args:
        fact: The factto base the script on
        max_length: Maximum script length in words
        
    Returns:
        Dictionary containing script, title, and metadata
    """
    # Implementation...
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

```
Add word-by-word caption animation

- Implement per-word timing calculation
- Add smooth fade transitions
- Update subtitle style configuration

Fixes #123
```

### Documentation

- Update README.md for user-facing changes
- Update SETUP.md for setup process changes
- Add inline comments for complex logic
- Keep documentation clear and concise

## Project Structure

```
src/viral_shorts/
├── content_sourcing/    # Fetch facts and extract keywords
├── scripting/           # AI script generation
├── narration/           # Text-to-speech conversion
├── video_assembly/      # Video editing and captions
├── publishing/          # YouTube upload functionality
├── utils/               # Shared utilities
└── config.py            # Configuration management
```

## Testing

- Write tests for new features
- Maintain test coverage above 70%
- Use pytest for all tests
- Mock external API calls

```python
def test_extract_keywords():
    parser = FactParser()
    keywords = parser.extract_keywords("Mars is red planet")
    assert "mars" in [k.lower() for k in keywords]
    assert len(keywords) <= 5
```

## Areas for Contribution

### High Priority

- [ ] Multi-language support
- [ ] Advanced caption animations
- [ ] Video templates/themes
- [ ] Batch video generation
- [ ] Performance optimizations

### Medium Priority

- [ ] Web dashboard
- [ ] Analytics integration
- [ ] Scheduled publishing
- [ ] A/B testing for titles
- [ ] Custom fact sources

### Good First Issues

- [ ] Improve error messages
- [ ] Add more unit tests
- [ ] Documentation improvements
- [ ] Bug fixes
- [ ] Code cleanup

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making QuantumFacts better! 🎉
