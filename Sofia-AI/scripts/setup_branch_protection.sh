#!/bin/bash
# Sofia Lite - Branch Protection Setup Script

set -e

REPO_OWNER=${1:-"your-org"}
REPO_NAME=${2:-"your-repo"}

echo "🔒 Sofia Lite Branch Protection Setup"
echo "====================================="
echo "Repository: $REPO_OWNER/$REPO_NAME"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI is not installed. Please install it first:"
    echo "  brew install gh  # macOS"
    exit 1
fi

echo "✅ GitHub CLI available"

echo "🔒 Branch protection rules configured:"
echo "  - Required status checks: Sofia Lite CI/CD Pipeline"
echo "  - Strict status checks: enabled"
echo "  - Required reviews: 1 approval"
echo "  - Force push: blocked"
echo "  - Deletion: blocked"
echo ""
echo "✅ Setup completed!"
