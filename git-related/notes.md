# Git Bisect: Quick Notes

**What:** Binary search through commits to find the first one that introduced a bug. ~log₂(N) steps (1,000 commits ≈ 10 tests).

**Memory aid:** Bad now, good then, bisect between.

## Use when
- It worked before, broken now (regression)
- You know one good commit/tag and one bad commit
- Bug is easy to test (script or quick check)

## Don't use when
- Bug always existed (no good commit)
- Bug is flaky/intermittent
- Commits are huge or messy

## Commands

| Command | Purpose |
|---|---|
| `git bisect start` | Begin session |
| `git bisect bad [commit]` | Mark broken (default: current) |
| `git bisect good [commit]` | Mark working |
| `git bisect run <cmd>` | Automate testing |
| `git bisect skip` | Skip untestable commit |
| `git bisect log` | Show progress |
| `git bisect reset` | End session, return to branch |

## Manual flow

    git bisect start
    git bisect bad
    git bisect good <old-commit-or-tag>
    # test, then mark good/bad, repeat
    git bisect reset
    git show <hash>

## Automated flow

    git bisect start HEAD <good-commit>
    git bisect run python3 -m unittest test_file
    git bisect reset

## Exit codes (for `run`)
- `0` = good
- `1-127` (except 125) = bad
- `125` = skip

## Remember
1. Keep a late-written test **untracked** so it survives checkouts
2. Test only features present in all commits
3. Start with a clean working tree
4. Always `git bisect reset` at the end
5. Commit the test with the fix as a regression test



# Git Power Commands: Quick Notes

**Memory aid:** Find it (blame, log -S, bisect) → Save it (stash, worktree) → Fix it (reflog, restore, cherry-pick).

## Find issues fast

| Command | Use it to |
|---|---|
| `git bisect` | Find the commit that broke something |
| `git blame <file>` | See who changed each line and when |
| `git blame -L 10,30 <file>` | Blame only lines 10-30 |
| `git log -S"text"` | Find commits that added/removed that exact text |
| `git log -G"regex"` | Same, but matches a regex |
| `git log -p <file>` | Show full change history of a file |
| `git log --follow <file>` | Track history across renames |
| `git log -L :func_name:file.py` | History of one function only |
| `git log --oneline --graph --all` | Visual branch map |
| `git show <hash>` | Inspect one commit |
| `git grep "text"` | Fast search in tracked files |
| `git diff main...feature` | What the feature branch changed vs main |

## Save time while working

| Command | Use it to |
|---|---|
| `git stash -u` | Shelve changes (incl. untracked) to switch tasks |
| `git stash pop` | Restore shelved changes |
| `git switch -` | Jump back to the previous branch |
| `git worktree add ../dir branch` | Work on 2 branches at once, no stashing |
| `git commit --fixup <hash>` | Mark a commit as a fix for an older one |
| `git rebase -i --autosquash` | Clean up/squash commits before PR |
| `git commit --amend --no-edit` | Add forgotten changes to last commit |
| `git add -p` | Stage changes piece by piece |
| `git pull --rebase` | Pull without messy merge commits |
| `git cherry-pick <hash>` | Copy one commit to the current branch |

## Undo mistakes (safety nets)

| Command | Use it to |
|---|---|
| `git reflog` | See everything HEAD did; recover "lost" commits |
| `git reset --hard <reflog-hash>` | Jump back to a previous state |
| `git restore <file>` | Discard changes in a file |
| `git restore --staged <file>` | Unstage a file |
| `git revert <hash>` | Safely undo a commit with a new commit |
| `git reset --soft HEAD~1` | Undo last commit, keep changes staged |
| `git clean -fd` | Delete untracked files (use `-n` first to preview) |

## Useful config / aliases

    git config --global alias.lg "log --oneline --graph --all --decorate"
    git config --global pull.rebase true
    git config --global rerere.enabled true   # remember conflict resolutions
    git config --global push.autoSetupRemote true

## Typical debugging combo
1. `git log -S"suspect"` → narrow down when it appeared
2. `git blame -L` → see who/why
3. `git bisect run <test>` → pin the exact commit
4. `git show <hash>` → read the change
5. Fix + commit test with the fix

## Golden rules
- `git reflog` rescues almost any mistake (if committed once)
- Preview before destroying: `git clean -n`, `git diff`
- Never rewrite history (`reset --hard`, `rebase`, `--amend`) on pushed shared branches
- Prefer `git revert` for shared branches, `reset` for local only


<br>

# Git Strategy for Shipping Features to Production (High Level)

**Memory aid:** Branch small → Review → Merge to main → Tag → Deploy → Roll back fast.

## 1. Pick a branching model

| Model | How it works | Best for |
|---|---|---|
| **Trunk-based** | Short-lived branches (hours to 2 days), merge to `main` often, hide unfinished work behind feature flags | Fast-moving teams, continuous deployment (most modern teams) |
| **GitHub Flow** | `main` is always deployable; one branch per feature, PR, merge, deploy | Web apps, small/medium teams |
| **Git Flow** | `main` + `develop` + `release/*` + `hotfix/*` branches | Scheduled releases, versioned products, mobile apps |

If unsure, start with **GitHub Flow**.

## 2. Feature lifecycle

    main (always deployable)
      |
      +-- feature/login-validation   (branch off main)
      |        commit, commit, commit
      |        open Pull Request
      |        CI runs tests + review approval
      +--------> merge (squash or rebase) to main
      |
      tag v1.4.0  -> deploy to staging -> prod

Commands:

    git switch main && git pull --rebase
    git switch -c feature/login-validation
    # work, commit small and focused (git add -p)
    git fetch && git rebase origin/main     # stay up to date
    git push -u origin feature/login-validation
    # open PR, get review, CI green, merge

## 3. Core principles

| Principle | Why |
|---|---|
| **`main` is always deployable** | Any commit can ship at any time |
| **Small branches, small PRs** | Easier review, fewer conflicts, easier `bisect` and `revert` |
| **Protect `main`** | No direct pushes; require PR, review, and passing CI |
| **Feature flags** | Merge unfinished code safely; turn on in prod when ready |
| **One idea per commit** | Clean history, easy rollback |
| **Squash merge** (or rebase) | Linear, readable history on `main` |

## 4. Release pipeline

1. **PR checks:** lint, unit tests, security scan
2. **Merge to `main`:** auto-deploy to **staging**
3. **Smoke test** on staging
4. **Tag** a release: `git tag -a v1.4.0 -m "Release 1.4.0"`
5. **Deploy tag** to prod (CI/CD triggers on `v*` tags)
6. **Monitor**, then gradually roll out (canary / percentage rollout)

## 5. When things break in prod

| Situation | Action |
|---|---|
| Bad release, need fast fix | **Roll back**: redeploy previous tag (`v1.3.2`) |
| Bad commit on `main` | `git revert <hash>` (never rewrite shared history) |
| Urgent fix needed | `hotfix/*` branch off the **tag or main**, PR, tag `v1.4.1`, deploy |
| Hotfix must reach other branches | `git cherry-pick <hash>` |
| Don't know which commit broke it | `git bisect run <test>` |

## 6. Hotfix flow

    git switch -c hotfix/payment-crash v1.4.0
    # fix + test
    git commit -am "Fix payment crash"
    git tag -a v1.4.1 -m "Hotfix 1.4.1"
    git push origin hotfix/payment-crash v1.4.1
    # merge back into main so the fix isn't lost

## 7. Team rules worth enforcing
- Branch naming: `feature/`, `bugfix/`, `hotfix/`, `release/`
- Conventional commits: `feat:`, `fix:`, `chore:` (enables auto changelogs)
- Semantic versioning: `vMAJOR.MINOR.PATCH`
- Never force-push to `main` or shared branches
- Delete merged branches: `git push origin --delete <branch>`
- Delete flags once a feature is fully rolled out

## Where our practice commands fit

| Command | Role in this flow |
|---|---|
| `git stash` | Switch to a hotfix mid-feature |
| `git add -p` | Keep commits clean for review |
| `git rebase -i --autosquash` | Tidy commits before PR |
| `git tag` | Mark releases, trigger deploys, enable rollback |
| `git bisect` | Find the commit behind a regression |
| `git reflog` | Recover from local mistakes |
| `git revert` | Safely undo a bad merge on `main` |