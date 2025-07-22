# Linear + GitHub Integration Workflow

This repository uses automated workflows to keep Linear issues in sync with GitHub pull requests.

## How It Works

### 1. **Creating a PR automatically updates Linear**
When you create a PR with a Linear issue ID in the title or branch name:
- Linear issue gets automatically updated to "In Review" status
- PR gets a comment linking to the Linear issue

### 2. **Merging a PR completes the Linear issue**
When a PR is merged:
- Linear issue is automatically marked as "Done"
- PR gets a completion comment with Linear issue link

## Setup Instructions

### Branch Naming Convention
Use Linear issue ID in your branch name:
```bash
git checkout -b feature/man-33-your-feature-description
# or
git checkout -b man-33-short-description
```

### PR Title Convention
Include Linear issue ID in your PR title:
```
feat: Your feature description (MAN-33)
# or
MAN-33: Your feature description
```

### Required Secrets
Add these to your GitHub repository secrets:

1. **LINEAR_API_KEY**: Your Linear API key
   - Go to Linear → Settings → API → Create new key
   - Add to GitHub: Settings → Secrets and variables → Actions → New repository secret

## Workflow Examples

### Example 1: Feature Branch
```bash
# 1. Create branch with Linear ID
git checkout -b feature/man-42-swipeable-cards

# 2. Make your changes and commit
git add .
git commit -m "feat: Implement swipeable card interface (MAN-42)"

# 3. Push and create PR
git push -u origin feature/man-42-swipeable-cards
gh pr create --title "feat: Swipeable Card Interface (MAN-42)" --body "..."

# Result: Linear issue MAN-42 automatically moved to "In Review"
```

### Example 2: PR Merge
```bash
# When PR is merged (via GitHub UI or CLI):
gh pr merge 1 --squash

# Result: Linear issue automatically marked as "Done"
```

## Benefits

✅ **Automatic Status Updates**: No manual Linear status changes needed  
✅ **Traceability**: Clear links between PRs and Linear issues  
✅ **Team Visibility**: Everyone sees progress in both tools  
✅ **Reduced Overhead**: Focus on coding, not project management  

## Troubleshooting

### Linear issue not updating?
1. Check if LINEAR_API_KEY is set in GitHub secrets
2. Verify Linear issue ID format (MAN-XX) in PR title or branch name
3. Check GitHub Actions logs for error details

### Manual override needed?
You can always manually update Linear issue status if needed.

## Workflow Files

- `.github/workflows/linear-integration.yml` - Main automation workflow
- `.github/LINEAR_WORKFLOW.md` - This documentation