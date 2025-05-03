# Contributing to Signal Messenger Python API

Thank you for considering contributing to the Signal Messenger Python API! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/signal-messenger-python-api.git
   cd signal-messenger-python-api
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. Run code quality checks:
   ```bash
   black .
   isort .
   flake8
   mypy signal_messenger
   ```

5. Commit your changes:
   ```bash
   git commit -m "Add your meaningful commit message here"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request from your fork to the main repository

## Adding New Modules

To add a new module for a Signal API endpoint:

1. Create a new file in the `signal_messenger/modules/` directory
2. Define a module class that implements the API endpoints
3. Update the `signal_messenger/modules/__init__.py` file to import and expose the new module
4. Update the `signal_messenger/client.py` file to inherit from the new module
5. Add the module initialization in the `_init_modules()` method
6. Write tests for the new module in the `tests/` directory

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all classes and methods
- Keep lines under 88 characters (Black's default)
- Use descriptive variable names

## Testing

- Write tests for all new functionality
- Aim for 100% test coverage for new code
- Run the test suite before submitting a pull request

## Documentation

- Update the README.md file with any new features or changes
- Document all public methods and classes
- Include examples for new functionality

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
