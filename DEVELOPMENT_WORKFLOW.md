# Trendit Development Workflow

This document defines the complete development ceremony for the Trendit platform, including git submodule management, feature development, code review integration, and human-AI collaboration protocols.

## 🏗️ Repository Architecture

```
trendit/ (ROOT REPO - jpotterlabs/trendit)
├── backend/          → jpotterlabs/trendit-backend (SUBMODULE)
├── frontend/         → jpotterlabs/trendit-frontend (SUBMODULE)  
├── mobile/           → jpotterlabs/trendit-mobile (SUBMODULE)
└── docs/             → Documentation and deployment guides
```

**Key Principle**: Each submodule is an independent repository that can be developed and deployed separately, coordinated through the root repository.

## 🎯 Development Decision Matrix

### Small Changes (Direct to Main)
**Criteria**: One-line changes, documentation updates, obvious bug fixes, no functional risk

**Examples**:
- Fix typo in component comment
- Update package.json version number
- Add missing import statement
- Fix linting errors
- Update README documentation

**Trigger Phrases**:
```bash
"Quick fix to main branch: [description]"
"Small change in [submodule]: [description]"  
"Fix [simple issue] directly in main"
```

### Feature Development (Feature Branch Required)
**Criteria**: New functionality, behavior changes, multiple files, needs review

**Examples**:
- Add new components or pages
- Modify API endpoints or database schema
- Change authentication flows
- Update styling systems or themes
- Add new dependencies
- Refactor existing functionality

**Trigger Phrases**:
```bash
"Create feature branch for [description] in [frontend/backend/mobile]"
"Add [feature name] to the [submodule] submodule"
"Implement [feature] in [submodule] and create PR"
"Follow the submodule workflow for [description]"
```

## 🔄 Standardized Git Submodule Workflow

### Phase 1: Pre-Work Verification
**ALWAYS execute before starting any work**:

```bash
pwd                           # Verify current directory  
git remote -v                 # Confirm which repository
git status                    # Check branch and state
git submodule status          # Check all submodule states
```

**Critical Rules**:
- ⚠️ **NEVER** assume your location - always verify with `pwd`
- ⚠️ **ALWAYS** use absolute paths for navigation
- ⚠️ **NEVER** ignore detached HEAD warnings - fix immediately

### Phase 2: Submodule Development

#### Step 1: Navigate to Submodule
```bash
# Use ABSOLUTE paths only
cd /home/jason/projects/jpotterlabs/trendit/[frontend|backend|mobile]
```

#### Step 2: Create Feature Branch (if needed)
```bash
git status                    # Must show clean working tree
git checkout -b feature/[descriptive-name]
```

#### Step 3: Implement and Commit
```bash
# ... make your changes ...
git add .
git commit -m "Descriptive commit message

- Detailed description of changes
- Impact and context
- Any breaking changes noted

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push -u origin feature/[feature-name]  # First push sets upstream
# OR
git push  # Subsequent pushes to existing branch
```

### Phase 3: Root Repository Update

#### Step 1: Navigate to Root
```bash
cd /home/jason/projects/jpotterlabs/trendit
```

#### Step 2: Ensure Clean State
```bash
git checkout main             # Switch to stable branch
git submodule update          # Reset submodules if needed (optional)
```

#### Step 3: Point to New Submodule State
```bash
cd [submodule]
git checkout [target-branch]  # feature branch or main
cd ..
```

#### Step 4: Update Root Repository Pointer
```bash
git add [submodule]
git commit -m "Update [submodule] submodule: [description]

Points to [branch-name] with changes:
- Brief summary of what was added/changed
- Context for the update

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 📋 Code Review & Collaboration Workflow

### Step 1: Claude Creates PR
When feature development is complete:

1. **Feature implemented** in submodule with commits and push
2. **PR created automatically** using `gh pr create` CLI command
3. **Root repository updated** to point to feature branch (if applicable)
4. **PR link and summary provided** of all changes made

**PR Creation Command**:
```bash
gh pr create --title "[Descriptive title]" --body "$(cat <<'EOF'
## Summary
- [Change 1]
- [Change 2]
- [Change 3]

## Test plan
- [ ] [Test item 1]
- [ ] [Test item 2]
- [ ] [Test item 3]

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

### Step 2: Automated Review (CodeRabbit)
- CodeRabbit automatically analyzes the PR
- Generates code review comments and suggestions
- Flags potential issues, improvements, best practices

### Step 3: Review Response (Human Choice)

#### Option A: Bulk Review
**Human triggers**:
```
"Read the CodeRabbit PR comments and implement warranted suggestions"
```

**Claude will**:
- Fetch and analyze all CodeRabbit feedback
- Implement suggestions deemed technically sound
- Commit fixes to the same feature branch (updates existing PR)
- Provide summary of changes made vs skipped with reasoning

#### Option B: Individual Review
**Human triggers**:
```
"CodeRabbit suggests: [paste specific suggestion text]"
```

**Claude will**:
- Assess the specific suggestion
- Implement if technically warranted
- Commit to same feature branch
- Explain reasoning for implementation or rejection

### Step 4: Review Fix Implementation
**Critical**: All review fixes go to the **same branch, same PR**

```bash
# Stay on existing feature branch
git status  # Verify on correct feature branch

# Make CodeRabbit suggested fixes
# ... implement changes ...

git add .
git commit -m "Address CodeRabbit feedback: [specific improvements made]

- Fix prop validation issues
- Improve type safety
- Optimize performance as suggested
- Add missing error handling

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push  # Updates existing PR automatically
```

### Step 5: Human Control & Cleanup
**Human responsibilities** (Claude never does these):

1. ✅ **Review final PR** and approve changes
2. ✅ **Merge the PR** when satisfied with all changes
3. ✅ **Delete the feature branch** after merge
4. ✅ **Inform Claude**: `"PR merged and branch deleted"`

### Step 6: Post-Merge Sync
When informed of merge completion, Claude will:
- Update understanding of repository state
- Note changes are now in main branch
- Reset mental model for next development cycle

## 🚨 Critical Workflow Rules

### Absolute Prohibitions
- ❌ **NEVER** create branches in root repo for submodule changes
- ❌ **NEVER** assume relative paths will work - use absolute paths only
- ❌ **NEVER** ignore detached HEAD states - fix immediately
- ❌ **NEVER** create new branches for CodeRabbit review fixes
- ❌ **NEVER** merge PRs or delete branches (Human-only responsibility)

### Required Practices
- ✅ **ALWAYS** verify location with `pwd` and `git remote -v` before git operations
- ✅ **ALWAYS** work in submodule first, root repo second
- ✅ **ALWAYS** use absolute paths for navigation between repositories
- ✅ **ALWAYS** commit review fixes to the same feature branch
- ✅ **ALWAYS** include Claude Code attribution in commit messages

### Pull Request Strategy
1. **Create submodule PR first**: `jpotterlabs/trendit-[submodule]`
2. **Create root repo PR second**: `jpotterlabs/trendit` (includes submodule update)
3. **Merge order**: Submodule PR first, then root repo PR

## 🎭 Human-AI Collaboration Boundaries

### Claude Responsibilities
- 🤖 **Feature implementation** in submodules
- 🤖 **Branch creation and management** during development
- 🤖 **Commit creation** with proper messages and attribution
- 🤖 **CodeRabbit feedback assessment** and implementation
- 🤖 **PR creation assistance** and providing GitHub links
- 🤖 **Repository state analysis** and workflow guidance

### Human Responsibilities  
- 👤 **Final PR review** and approval decisions
- 👤 **PR merging** when satisfied with changes
- 👤 **Feature branch deletion** after merge
- 👤 **Workflow completion notification** to Claude
- 👤 **Strategic decisions** about feature direction and priorities

### Shared Responsibilities
- 🤝 **Code review discussion** - Human interprets, Claude implements
- 🤝 **Quality assurance** - CodeRabbit flags, Claude fixes, Human approves
- 🤝 **Documentation updates** - Claude writes, Human reviews

## 🔍 Example Workflows

### Example 1: Small Fix (Direct Main)
```bash
# Human: "Quick fix to main branch: Fix typo in SignIn component"

# Claude executes:
cd /home/jason/projects/jpotterlabs/trendit/frontend
git checkout main
# ... fix typo ...
git add .
git commit -m "Fix: Correct typo in SignIn component placeholder text"
git push
cd /home/jason/projects/jpotterlabs/trendit
git add frontend
git commit -m "Update frontend submodule: Fix SignIn component typo"
```

### Example 2: Feature Development (Full Workflow)
```bash
# Human: "Add user dashboard improvements to frontend"

# Claude executes full workflow:
# 1. Navigate to frontend submodule
# 2. Create feature/user-dashboard-improvements branch  
# 3. Implement changes
# 4. Commit and push feature branch
# 5. Update root repo pointer
# 6. Provide PR creation link
```

### Example 3: CodeRabbit Review Response
```bash
# Human: "Read the CodeRabbit PR comments and implement warranted suggestions"

# Claude executes:
# 1. Analyze all CodeRabbit feedback
# 2. Implement technically sound suggestions
# 3. Commit fixes to same feature branch (updates existing PR)
# 4. Provide summary of changes made vs skipped
```

## 🎯 Success Metrics

A successful workflow execution includes:

- ✅ **Clean git history** with atomic, well-described commits
- ✅ **Proper submodule coordination** between repos
- ✅ **Comprehensive code review** with automated and human oversight
- ✅ **Clear collaboration boundaries** with human control over merging
- ✅ **Efficient development cycle** with minimal back-and-forth
- ✅ **Complete documentation** of all changes and decisions

## 🚀 Quick Reference

### Trigger Phrases Summary
```bash
# Small changes (main branch)
"Quick fix to main branch: [description]"
"Small change in [submodule]: [description]"

# Feature development (feature branch)  
"Add [feature] to [frontend/backend/mobile]"
"Create feature branch for [description] in [submodule]"
"Follow the submodule workflow for [description]"

# Code review responses
"Read the CodeRabbit PR comments and implement warranted suggestions"
"CodeRabbit suggests: [specific suggestion]"

# Workflow completion
"PR merged and branch deleted"
```

### Essential Commands
```bash
# Pre-work verification
pwd && git remote -v && git status && git submodule status

# Absolute navigation
cd /home/jason/projects/jpotterlabs/trendit/[submodule]
cd /home/jason/projects/jpotterlabs/trendit

# Emergency recovery
git checkout main && git submodule update
```

---

This workflow ensures consistent, high-quality development practices across all Trendit platform development while maintaining clear human oversight and control.