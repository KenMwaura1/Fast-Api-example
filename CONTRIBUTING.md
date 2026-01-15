# Contributing to Fast API Example

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building this project together.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Avoid duplicates
2. **Create a detailed bug report** including:
   - Clear description of the bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment info (Python version, OS, dependencies)
   - Error messages and stack traces

**Example:**
```
Title: API returns 500 error when creating note with special characters

Steps to reproduce:
1. POST to /notes with title containing emoji: "My Note 🎉"
2. Server returns 500 Internal Server Error

Expected: Note should be created successfully
Actual: 500 Error returned

Environment: Python 3.13, PostgreSQL 14, FastAPI 0.115.8
```

### Suggesting Enhancements

1. **Check existing discussions** - Avoid duplicates
2. **Provide clear motivation** - Why would this be useful?
3. **Suggest implementation** - How would this work?
4. **Include examples** - Show the desired behavior

**Example:**
```
Feature: Add note categories/tags

Motivation: Users need to organize notes by category

Suggestion: 
- Add optional 'category' field to notes
- Filter by category in GET /notes endpoint
- Return categories in list endpoint

Example usage:
POST /notes with {"title": "...", "category": "work"}
GET /notes?category=work
```

## Pull Request Process

### Before You Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Set up development environment (see [DEVELOPMENT.md](DEVELOPMENT.md))

### Making Changes

1. **Follow code style** (see [DEVELOPMENT.md](DEVELOPMENT.md#code-style-guidelines))
2. **Write/update tests** for all changes
3. **Update documentation** (README, API.md, docstrings)
4. **Keep commits clean and descriptive**

### Before Submitting PR

```bash
# Run tests
pytest src -v

# Check coverage
pytest src --cov=src/app

# Lint code
pylint src/app

# Format code
black src/app
isort src/app
```

### Submitting PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```

2. **Create Pull Request** with:
   - Clear title describing changes
   - Detailed description explaining what and why
   - Reference to related issues
   - Screenshots/examples if applicable

3. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Related Issues
   Fixes #123

   ## Testing
   Describe how you tested this change

   ## Checklist
   - [ ] Tests pass
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No new warnings
   ```

### PR Review Process

1. Maintainers will review your PR
2. We may request changes or ask questions
3. Once approved, your PR will be merged
4. Your contribution will be recognized!

## Types of Contributions

### Documentation
- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Update guides and tutorials

**How to contribute:**
- Edit markdown files directly
- Submit PR with your improvements
- Help translate documentation

### Bug Fixes
- Fix reported bugs
- Improve error handling
- Performance improvements
- Security fixes

**How to contribute:**
1. Pick an issue labeled `bug`
2. Create a fix
3. Add test case to prevent regression
4. Submit PR

### Features
- New endpoints
- Enhanced filtering/searching
- Performance optimization
- Code refactoring

**How to contribute:**
1. Discuss in issue first (especially for large changes)
2. Implement the feature
3. Add comprehensive tests
4. Update documentation
5. Submit PR

### Tests
- Increase test coverage
- Add edge case tests
- Improve test structure
- Add integration tests

**How to contribute:**
- Review existing tests
- Identify gaps
- Write new tests
- Submit PR

## Code Quality Standards

### Python Code

✅ **Do:**
- Use type hints
- Write docstrings
- Handle exceptions properly
- Write clean, readable code
- Follow PEP 8 style guide
- Write tests for new code

```python
async def get_note(note_id: int) -> Optional[NoteDB]:
    """
    Retrieve a note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        Note object if found, None otherwise
        
    Raises:
        HTTPException: If database query fails
    """
    try:
        return await crud.get(note_id)
    except Exception as e:
        logger.error(f"Failed to get note: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

❌ **Don't:**
- Ignore type hints
- Skip error handling
- Write cryptic variable names
- Commit commented-out code
- Create large functions without breaking them down

```python
# Bad example
async def fn(id):
    # This is bad code
    x = await db.fetch_one("SELECT * FROM notes WHERE id = ?", (id,))
    # TODO: fix this later
    return x
```

### Tests

✅ **Do:**
- Test happy path and error cases
- Use descriptive test names
- Mock external dependencies
- Keep tests focused
- Use parametrized tests for multiple scenarios

```python
@pytest.mark.parametrize("title,description,expected", [
    ("Short", "Valid description", True),
    ("a", "Too short", False),
    ("x" * 300, "Too long", False),
])
def test_note_validation(title, description, expected):
    """Test note field validation"""
    # test implementation
```

❌ **Don't:**
- Test implementation details
- Create brittle tests
- Skip edge cases
- Write untestable code
- Make tests dependent on each other

### Documentation

✅ **Do:**
- Use clear, concise language
- Include examples
- Document assumptions
- Keep documentation up-to-date
- Add code comments for complex logic

❌ **Don't:**
- Assume reader knowledge
- Leave documentation outdated
- Skip examples
- Write unclear explanations

## Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, etc

### Scope
- `api`: API endpoints
- `db`: Database layer
- `models`: Data models
- `tests`: Test files
- `docs`: Documentation

### Examples

```
feat(api): add filtering by category to notes endpoint

Implement filtering mechanism for notes based on category field.
- Add category field to NoteSchema
- Update get_notes CRUD operation
- Add filter tests

Fixes #123
```

```
fix(db): handle connection timeout gracefully

Catch DatabaseError when connection times out and return
appropriate error response to client.
```

```
docs: improve API documentation examples
```

## Review Checklist

When reviewing PRs, ensure:

- [ ] Code follows project style guide
- [ ] All tests pass
- [ ] Code coverage hasn't decreased
- [ ] Documentation is updated
- [ ] Commits are clean and well-described
- [ ] No hardcoded values or secrets
- [ ] Error handling is appropriate
- [ ] Performance is considered

## Development Environment

### Required Tools
- Python 3.13+
- PostgreSQL 12+
- Git

### Optional Tools
- Docker & Docker Compose
- IDE/Editor with Python support
- Postman or similar API testing tool
- Database client (pgAdmin, DBeaver)

### Setup Steps
See [DEVELOPMENT.md](DEVELOPMENT.md#local-development-setup)

## Common Mistakes to Avoid

1. **Not running tests before submitting PR**
   ```bash
   pytest src -v  # Always run this!
   ```

2. **Mixing unrelated changes**
   - One feature per PR
   - Keep scope focused

3. **Forgetting to update documentation**
   - README.md (if relevant)
   - API.md (if adding endpoints)
   - Docstrings (always)

4. **Hardcoding values**
   ```python
   # Bad
   DB_URL = "postgresql://user:pass@localhost/db"
   
   # Good
   DB_URL = os.getenv("DATABASE_URL", "postgresql://...")
   ```

5. **Ignoring edge cases**
   - Empty strings
   - Null/None values
   - Special characters
   - Large values

## Getting Help

- **Questions?** Open a discussion
- **Stuck?** Ask in the PR or issue
- **Feedback?** We're here to help!

## Recognition

Contributors are recognized in:
- README.md (Contributors section)
- GitHub contributors page
- Release notes

Thank you for contributing! 🎉

---

**Last Updated:** January 2026
