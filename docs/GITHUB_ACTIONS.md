# GitHub Actions CI/CD Setup

This project uses GitHub Actions for continuous integration and deployment. Here's what each workflow does:

## Workflows

### 1. CI (`.github/workflows/ci.yml`)
**Triggered on**: Push to main/develop, Pull Requests

**What it does**:
- **Multi-platform testing**: Tests on Ubuntu, Windows, and macOS
- **Multi-version testing**: Tests Python 3.9, 3.10, 3.11, and 3.12
- **Code quality**: Runs linting, type checking, and formatting checks
- **Documentation**: Builds documentation to ensure it compiles
- **Security**: Runs security scans with safety and bandit
- **Package building**: Builds the package and validates it
- **Integration testing**: Tests against a real Olog service in Docker

### 2. Release (`.github/workflows/release.yml`)
**Triggered on**: GitHub releases, manual dispatch

**What it does**:
- Builds the package
- Publishes to PyPI (on release)
- Publishes to Test PyPI (manual dispatch)
- Uploads release artifacts to GitHub

### 3. Code Quality (`.github/workflows/quality.yml`)
**Triggered on**: Push, PRs, weekly schedule

**What it does**:
- Runs pre-commit hooks
- Security scanning (bandit, safety, pip-audit)
- Code complexity analysis
- Generates quality reports

### 4. Dependency Updates (`.github/workflows/dependencies.yml`)
**Triggered on**: Weekly schedule, manual dispatch

**What it does**:
- Checks for dependency updates
- Creates PR with updated dependencies
- Automated dependency management

## Setup Instructions for Your Boss

### 1. Repository Settings
Enable the following in your GitHub repository settings:

1. **Actions**: Enable GitHub Actions
2. **Branch Protection**: Require PR reviews and status checks
3. **Secrets**: Add the following repository secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token for publishing
   - `TEST_PYPI_API_TOKEN`: Your Test PyPI API token

### 2. Branch Protection Rules
Recommended settings for `main` branch:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Required status checks:
  - `test (ubuntu-latest, 3.12)`
  - `lint`
  - `docs`

### 3. PyPI Publishing Setup

#### Get PyPI API Tokens:
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Create API token with scope for this project
3. Go to [Test PyPI](https://test.pypi.org/manage/account/) and repeat

#### Add to GitHub Secrets:
1. Go to Repository → Settings → Secrets and variables → Actions
2. Add `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN`

### 4. Making a Release

1. **Update version**: The version is automatically managed by `hatch-vcs` based on git tags
2. **Create release**: Go to GitHub → Releases → Create a new release
3. **Tag**: Use semantic versioning (e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`)
4. **Publish**: The workflow will automatically build and publish to PyPI

## Development Workflow

### For Developers:
```bash
# Install development dependencies
pip install -e .[dev]

# Run tests locally
nox -s test

# Run all quality checks
nox -s lint mypy safety

# Format code
nox -s format
```

### For Contributors:
1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run local quality checks: `nox -s lint test`
5. Submit a pull request
6. GitHub Actions will automatically test your changes

## Quality Gates

The CI pipeline enforces these quality standards:
- ✅ All tests must pass on all supported Python versions
- ✅ Code coverage must be maintained
- ✅ No linting errors (ruff)
- ✅ No type checking errors (mypy)
- ✅ No security vulnerabilities (bandit, safety)
- ✅ Documentation must build successfully
- ✅ Package must build and install correctly

## Monitoring

- **Test Results**: Visible in PR checks and Actions tab
- **Coverage Reports**: Uploaded to Codecov (if configured)
- **Security Reports**: Available as downloadable artifacts
- **Package Health**: Monitored through automated dependency updates

This setup provides enterprise-grade CI/CD with comprehensive testing, security scanning, and automated publishing.
