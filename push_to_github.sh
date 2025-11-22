#!/bin/bash

# Script to push develop and main branches to GitHub
# This script handles authentication and branch pushing

echo "🚀 Pushing Resume Analyzer to GitHub..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Function to push branch
push_branch() {
    local branch=$1
    echo "📤 Pushing $branch branch..."
    
    git checkout $branch
    if [ $? -ne 0 ]; then
        echo "❌ Failed to checkout $branch"
        return 1
    fi
    
    git push -u origin $branch
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed $branch branch!"
        return 0
    else
        echo "❌ Failed to push $branch branch"
        echo ""
        echo "💡 Authentication required. Choose one:"
        echo ""
        echo "Option 1: Use Personal Access Token"
        echo "  1. Go to: https://github.com/settings/tokens"
        echo "  2. Generate new token (classic) with 'repo' scope"
        echo "  3. Run: git push -u origin $branch"
        echo "  4. Use token as password when prompted"
        echo ""
        echo "Option 2: Use SSH (recommended)"
        echo "  1. Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
        echo "  2. Add to GitHub: https://github.com/settings/keys"
        echo "  3. Change remote: git remote set-url origin git@github.com:haritmandaliya/resume_analyzer.git"
        echo "  4. Run this script again"
        return 1
    fi
}

# Push develop branch
echo "Step 1: Pushing develop branch..."
push_branch develop

if [ $? -eq 0 ]; then
    echo ""
    echo "Step 2: Merging develop into main..."
    git checkout main
    git merge develop --no-edit
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully merged develop into main"
        echo ""
        echo "Step 3: Pushing main branch..."
        push_branch main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 All done! Both branches pushed successfully!"
            echo ""
            echo "📋 Summary:"
            echo "  ✅ develop branch pushed"
            echo "  ✅ develop merged into main"
            echo "  ✅ main branch pushed"
            echo ""
            echo "🌐 View on GitHub: https://github.com/haritmandaliya/resume_analyzer"
        fi
    else
        echo "❌ Failed to merge develop into main"
    fi
fi

