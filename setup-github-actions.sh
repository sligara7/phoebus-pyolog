#!/bin/bash
# Setup script for GitHub Actions CI/CD

echo "🚀 Setting up GitHub Actions CI/CD for phoebus-pyolog"
echo "=================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Check if we have the required files
required_files=(
    ".github/workflows/ci.yml"
    ".github/workflows/release.yml" 
    ".github/workflows/quality.yml"
    ".github/workflows/dependencies.yml"
    "pyproject.toml"
    "noxfile.py"
)

echo "✅ Checking required files..."
all_files_exist=true
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        all_files_exist=false
    else
        echo "✅ Found: $file"
    fi
done

if [ "$all_files_exist" = false ]; then
    echo "❌ Some required files are missing. Please ensure all workflow files are created."
    exit 1
fi

echo ""
echo "📋 Next Steps for Your Boss:"
echo "============================"
echo ""
echo "1. 🔧 Repository Settings:"
echo "   - Go to GitHub repository Settings → Actions → General"
echo "   - Enable 'Allow all actions and reusable workflows'"
echo ""
echo "2. 🔒 Add PyPI API Tokens:"
echo "   - Go to Settings → Secrets and variables → Actions"
echo "   - Add PYPI_API_TOKEN (from https://pypi.org/manage/account/)"
echo "   - Add TEST_PYPI_API_TOKEN (from https://test.pypi.org/manage/account/)"
echo ""
echo "3. 🛡️ Branch Protection (recommended):"
echo "   - Go to Settings → Branches"
echo "   - Add rule for 'main' branch:"
echo "     ✅ Require a pull request before merging"
echo "     ✅ Require status checks to pass before merging"
echo "     ✅ Required status checks: test, lint, docs"
echo ""
echo "4. 🚀 Test the Setup:"
echo "   - Push this code to GitHub"
echo "   - Check the Actions tab for running workflows"
echo "   - Create a test PR to see all checks in action"
echo ""
echo "5. 📦 Making Releases:"
echo "   - Create a new release with a version tag (e.g., v1.0.0)"
echo "   - The package will automatically be published to PyPI"
echo ""
echo "✨ Your modern Python package is ready for enterprise development!"

# Check if we can run a quick test
echo ""
echo "🧪 Quick Local Test:"
echo "==================="
if command -v nox &> /dev/null; then
    echo "✅ nox is available"
    echo "   Try: nox -s lint test"
else
    echo "⚠️  nox not found. Install with: pip install nox"
fi

if command -v pre-commit &> /dev/null; then
    echo "✅ pre-commit is available"
    echo "   Try: pre-commit run --all-files"
else
    echo "⚠️  pre-commit not found. Install with: pip install pre-commit"
fi

echo ""
echo "📚 Documentation: See docs/GITHUB_ACTIONS.md for detailed information"
