# Git Setup Instructions

## Current Status

✅ Git repository initialized
✅ All files committed
✅ `develop` branch created
✅ `main` branch ready
✅ Remote repository configured: `https://github.com/haritmandaliya/resume_analyzer.git`

## Next Steps: Push to GitHub

### Option 1: Using Personal Access Token (Recommended)

1. **Generate a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control)
   - Copy the token

2. **Push using token:**
   ```bash
   # Push develop branch
   git checkout develop
   git push -u origin develop
   
   # Push main branch
   git checkout main
   git push -u origin main
   ```
   
   When prompted for password, use your **Personal Access Token** instead.

### Option 2: Using SSH (More Secure)

1. **Set up SSH key** (if not already done):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Add to GitHub: Settings > SSH and GPG keys
   ```

2. **Change remote URL:**
   ```bash
   git remote set-url origin git@github.com:haritmandaliya/resume_analyzer.git
   ```

3. **Push branches:**
   ```bash
   git checkout develop
   git push -u origin develop
   
   git checkout main
   git push -u origin main
   ```

### Option 3: Using GitHub CLI

```bash
# Install GitHub CLI if needed
# Then authenticate
gh auth login

# Push branches
git checkout develop
git push -u origin develop

git checkout main
git push -u origin main
```

## Verify Push

After pushing, verify on GitHub:
- Visit: https://github.com/haritmandaliya/resume_analyzer
- Check that both `main` and `develop` branches are visible
- Verify all files are present

## Branch Workflow

- **`develop`**: Development branch for new features
- **`main`**: Production-ready code

### Workflow:
1. Create feature branch from `develop`
2. Make changes and commit
3. Merge feature branch into `develop`
4. Test on `develop`
5. Merge `develop` into `main` when ready for production

## Quick Commands

```bash
# Check current branch
git branch

# Switch branches
git checkout develop
git checkout main

# View remote
git remote -v

# Check status
git status

# View commit history
git log --oneline
```

