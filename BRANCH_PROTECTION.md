# GitHub Branch Protection Setup Guide

This guide explains how to set up branch protection rules for the `main` branch to enforce code quality standards and CI/CD requirements.

## Branch Protection Configuration

### Step 1: Access Repository Settings

1. Go to your GitHub repository: https://github.com/thequantumturtle/QuantumAdventCalendar
2. Click **Settings** (top right)
3. Select **Branches** from the left sidebar
4. Click **Add rule** under "Branch protection rules"

### Step 2: Configure the Rule

**Branch name pattern**: `main`

### Step 3: Enable Required Protections

#### ✅ Require a pull request before merging
- [x] **Require pull request reviews before merging**
  - Number of required approvals: `1`
  - [x] **Require review from code owners** (optional)
  - [x] **Dismiss stale pull request approvals when new commits are pushed**

#### ✅ Require status checks to pass before merging
- [x] **Require branches to be up to date before merging**
- [x] **Require status checks to pass before merging**
  
**Required status checks** (check all of these):
- `backend-tests` (from GitHub Actions)
- `frontend-build` (from GitHub Actions)

#### ✅ Enforce administrators
- [x] **Include administrators** (optional but recommended)

#### ✅ Restrict who can push to matching branches
- [x] **Restrict who can push to matching branches** (optional)
  - Allow specific users/teams to bypass these requirements

#### ✅ Require a conversation resolution before merging
- [x] **Require all conversations on code to be resolved before merging**

### Step 4: Save Rules

Click **Create** to apply the branch protection rule.

---

## What This Protects

✅ **Prevents direct commits to main** - All changes must go through PRs
✅ **Enforces code review** - At least 1 approval required
✅ **Enforces CI/CD** - Blocks merge if tests fail
✅ **Prevents stale reviews** - Review becomes invalid if new commits are pushed
✅ **Requires conversations** - Must resolve all PR comments before merge

---

## Recommended Additional Steps

### 1. Enable Auto-merge (Optional)
When setting is available:
- [ ] Allow auto-merge (when PR is approved + CI passes)

### 2. Configure Default Branch
- Ensure `main` is set as the default branch

### 3. Enable Require Branches to Be Up to Date
- Prevents merge if branch is behind `main` by commits
- Click the checkbox during rule creation

### 4. Set Up CODEOWNERS (Optional)
Create `.github/CODEOWNERS` file:

```
# Backend
/backend/ @thequantumturtle

# Frontend  
/frontend/ @thequantumturtle

# Workflows
/.github/workflows/ @thequantumturtle

# All
* @thequantumturtle
```

---

## Workflow After Protection is Enabled

### Creating a Feature

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: description"

# Push branch
git push origin feature/your-feature

# Go to GitHub and create a Pull Request
```

### PR Review Process

1. **Developer** creates PR with clear description
2. **CI checks** run automatically (tests, build, linting)
3. **Code reviewer** reviews and approves (1 approval required)
4. **Merge conflicts** must be resolved
5. **PR author** addresses feedback if needed
6. **Reviewer** re-approves after changes
7. **Merge** button becomes available when all checks pass

---

## Bypass Scenarios

### When You Need to Bypass Protection

**Emergency hotfix** (with admin access):
```bash
# Not recommended, but possible with admin token
git push --force origin main
```

**Revert a bad merge** (same as above)

### Best Practice
- Never commit directly to main
- Always use feature branches
- Always go through PR process
- Use admin bypass only for emergencies

---

## Verify Protection is Active

1. Try to commit directly to main:
   ```bash
   git checkout main
   git commit --allow-empty -m "test"
   git push origin main
   ```
   
   **Expected**: Push rejected with message about branch protection

2. Create a PR without all checks passing:
   **Expected**: Merge button disabled, showing failing checks

---

## Monitoring & Maintenance

### Weekly
- Review open PRs
- Monitor CI/CD status
- Check for failed tests

### Monthly
- Analyze branch protection rule effectiveness
- Review protection rule settings
- Update CODEOWNERS if team changes

---

## Current CI/CD Status

Your GitHub Actions workflows are already configured:

- **Backend Tests**: `pytest backend/tests/ -v --cov`
- **Frontend Build**: `npm run build`
- **Coverage Reports**: Generated and uploaded

These will automatically run on every push and pull request.

---

## Troubleshooting

### "Required status check is expected"

The workflow hasn't run yet. Push any change to trigger it, or manually run from Actions tab.

### "Dismissing stale reviews" not working

Make sure this checkbox is enabled in the branch protection rule.

### Can't merge despite all checks passing

1. Verify all required approvals are present
2. Check that branch is up to date with main
3. Verify all conversations are resolved
4. Refresh the page

---

## Next Steps

1. ✅ Set up the branch protection rule as described above
2. ✅ Create `.github/CODEOWNERS` file (optional)
3. ✅ Test by creating a PR and verifying protection works
4. ✅ Update team documentation
5. ✅ Train team members on new PR workflow

