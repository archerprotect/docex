# Contributing to DocEx

Thank you for your interest in contributing to DocEx! We welcome contributions from the community.

## Development Setup

1. **Install Poetry**: `pip install poetry`
2. **Clone the repository**: `git clone https://github.com/archerprotect/docex.git`
3. **Navigate to the project directory**: `cd docex`
4. **Install dependencies**: `poetry install`

## Development Workflow

### Running Tests

```bash
poetry run pytest
```

### Linting and Type Checking

```bash
# Run type checking (using pyright)
poetry run poe lint
```

## Making Changes

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and add tests
4. **Run tests and linting**: `poetry run poe test && poetry run poe lint`
5. **Commit your changes**: `git commit -m "Add your feature"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request** on GitHub

## Adding New Features

### Adding a New Loader

1. Create a new file in `docex/loaders/`
2. Inherit from `BaseLoader`
3. Implement the `load` method
4. Add tests in `tests/loaders/`

### Adding a New Processor

1. Create a new file in `docex/processors/`
2. Inherit from `BaseProcessor`
3. Implement the `process` method
4. Add tests in `tests/processors/`

## Code Style

- Use type hints throughout
- Write docstrings for public methods
- Keep functions focused and small
- Add tests for new functionality

## Submitting Issues

When submitting issues, please include:

- Python version
- DocEx version
- Operating system
- Minimal code example that reproduces the issue
- Full error traceback

## Questions?

Feel free to open an issue for questions or join our discussions! 