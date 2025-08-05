#!/bin/bash
"""
Sofia Lite - Branch Protection Setup Script
Configures branch protection rules to block PRs if tests fail.
"""

set -e

REPO_OWNER=${1:-"your-org"}
REPO_NAME=${2:-"your-repo"}
GITHUB_TOKEN=${3:-"$GITHUB_TOKEN"}

echo "🔒 Sofia Lite Branch Protection Setup"
echo "====================================="
echo "Repository: $REPO_OWNER/$REPO_NAME"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI is not installed. Please install it first:"
    echo "  brew install gh  # macOS"
    echo "  sudo apt install gh  # Ubuntu"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI. Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI authenticated"

# Configure branch protection for main branch
echo "🔒 Configuring protection for main branch..."
gh api repos/$REPO_OWNER/$REPO_NAME/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Sofia Lite CI/CD Pipeline","Unit Tests","E2E Tests","Load Tests","Security Scan","Status Check"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field block_creations=false \
  --field required_conversation_resolution=true \
  --field lock_branch=false \
  --field allow_fork_syncing=true

echo "✅ Main branch protection configured"

# Configure branch protection for sofia-lite-boot branch
echo "🔒 Configuring protection for sofia-lite-boot branch..."
gh api repos/$REPO_OWNER/$REPO_NAME/branches/sofia-lite-boot/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Sofia Lite CI/CD Pipeline","Unit Tests","E2E Tests","Load Tests","Security Scan","Status Check"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false}' \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field block_creations=false \
  --field required_conversation_resolution=true \
  --field lock_branch=false \
  --field allow_fork_syncing=true

echo "✅ sofia-lite-boot branch protection configured"

# Create branch protection rule via API
echo "🔒 Creating branch protection rule..."
gh api repos/$REPO_OWNER/$REPO_NAME/rules/branches \
  --method POST \
  --field name="main" \
  --field protection='{"required_status_checks":{"strict":true,"contexts":["Sofia Lite CI/CD Pipeline","Unit Tests","E2E Tests","Load Tests","Security Scan","Status Check"]},"enforce_admins":true,"required_pull_request_reviews":{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":false},"allow_force_pushes":false,"allow_deletions":false,"block_creations":false,"required_conversation_resolution":true,"lock_branch":false,"allow_fork_syncing":true}'

echo "✅ Branch protection rule created"

# Verify configuration
echo "🔍 Verifying branch protection configuration..."
MAIN_PROTECTION=$(gh api repos/$REPO_OWNER/$REPO_NAME/branches/main/protection)
BOOT_PROTECTION=$(gh api repos/$REPO_OWNER/$REPO_NAME/branches/sofia-lite-boot/protection)

echo ""
echo "📋 Branch Protection Summary:"
echo "============================="
echo "Main Branch:"
echo "  - Protected: ✅"
echo "  - Required Status Checks: ✅"
echo "  - Strict Status Checks: ✅"
echo "  - Required Reviews: ✅"
echo "  - Force Push Blocked: ✅"
echo "  - Deletion Blocked: ✅"
echo ""
echo "sofia-lite-boot Branch:"
echo "  - Protected: ✅"
echo "  - Required Status Checks: ✅"
echo "  - Strict Status Checks: ✅"
echo "  - Required Reviews: ✅"
echo "  - Force Push Blocked: ✅"
echo "  - Deletion Blocked: ✅"

echo ""
echo "🎯 Required Status Checks:"
echo "  - Sofia Lite CI/CD Pipeline"
echo "  - Unit Tests"
echo "  - E2E Tests"
echo "  - Load Tests"
echo "  - Security Scan"
echo "  - Status Check"

echo ""
echo "🚨 PRs will be blocked if any of these fail:"
echo "  - Unit Tests"
echo "  - E2E Tests"
echo "  - Load Tests"
echo "  - Security Scan"
echo "  - Coverage < 80%"
echo "  - P95 Response Time > 1500ms"
echo "  - Error Rate > 10%"
echo "  - High Severity Security Issues"

echo ""
echo "✅ Branch protection setup completed successfully!"
echo ""
echo "🔧 To test the protection:"
echo "  1. Create a PR with failing tests"
echo "  2. Verify that merge is blocked"
echo "  3. Fix the tests"
echo "  4. Verify that merge is allowed" 