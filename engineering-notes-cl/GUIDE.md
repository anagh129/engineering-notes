# Building a Stake Engine slot: step by step

Everything below was actually run in a sandbox (Python 3.12, Rust 1.85, Node 22, pnpm 10.5).
Result: a working game `my_first_slot` at **96.00% RTP in both modes**, max win 5000x, all math checks passing.

## How Stake Engine works (30-second version)
- Games are **stateless and pre-computed**. Your math code simulates thousands of rounds ("books") ahead of time.
- Each book = a list of **events** (reveal, winInfo, setWin, finalWin...) + a payout multiplier.
- A **lookup table** CSV gives every book a weight. The RGS (server) picks a book by weight when the player bets.
- Your **frontend** never computes results. It only plays back the events the RGS returns from `/wallet/play`.
- So a game = **Math files** (index.json + lookUpTable CSV + books .jsonl.zst) + **Frontend build** (static site).

## Step 0: Sandbox
Docker (recommended):
    docker build -t stake-sandbox .
    docker run -it -v "$PWD/work:/workspace" -p 3001:3001 stake-sandbox
    stake-setup                # clones + installs math-sdk and web-sdk
Or on your own machine: install Python >= 3.12, **Rust >= 1.76** (Ubuntu's default 1.75 fails), Node >= 22.16, pnpm 10.5, then run `./setup.sh`.
GitHub Codespaces also works: open the folder, run `./setup.sh`.

## Step 1: Run the sample game first
    ./run_game.sh 0_0_lines
This simulates, optimizes to the RTP target, runs analysis and verification. Output lands in `math-sdk/games/<game>/library/`.
- `publish_files/`  -> what you upload to Stake Engine
- `statistics_summary.json`, `*_full_statistics.xlsx` -> RTP, hit rate, volatility, PAR-style data

## Step 2: Create your own game
    ./new_game.sh my_slot          # copies the lines sample
Then edit `math-sdk/games/my_slot/`:
| File | What you change |
|---|---|
| `game_config.py` | game_id, name, `rtp`, `wincap`, grid size, `paytable`, `paylines`, scatter/free-spin triggers, bet modes (base, buy-bonus), distribution quotas |
| `reels/*.csv` | reel strips (one column per reel). Symbol frequency here is the main RTP/volatility lever |
| `game_calculations.py`, `gamestate.py`, `game_executables.py` | game logic: wins, free spins, multipliers, tumbles |
| `game_optimization.py` | per-criteria RTP targets for the optimizer. **They must sum to the mode RTP** (e.g. 0.001 + 0.592 + 0.367 = 0.960) |
| `run.py` | simulation counts, threads, which pipeline stages run |

Other templates: `0_0_cluster`, `0_0_ways`, `0_0_scatter`, `0_0_expwilds`, `fifty_fifty` (simplest), `template` (blank).

## Step 3: Simulate, optimize, verify
    ./run_game.sh my_slot
Pipeline: `create_books` (simulate) -> Rust optimizer (reweights outcomes to hit target RTP) -> `create_stat_sheet` -> `execute_all_tests`.
Start with small sim counts (1e4) while iterating, then use 1e5-1e6 for the final run.
Approval-oriented checks to watch (verify exact limits in the current docs): RTP between roughly 90% and 98%, small RTP gap between modes, max-win frequency, volatility limits.
Debug loop: change reels/paytable -> rerun -> read `stats_summary.json`. If optimizer can't hit the target, adjust reels, quotas, or optimizer conditions.

## Step 4: Frontend
    cd web-sdk
    pnpm install
    pnpm turbo run build --filter=./apps/lines      # build via turbo from root, not inside the app
Output: `web-sdk/apps/lines/build/` (static site with index.html).
- Copy `apps/lines` to `apps/my_slot` and edit `src/game/` (symbols, assets, layout, book-event handlers).
- Book events from your math (`reveal`, `winInfo`, `setWin`, `finalWin`, plus any custom ones) map to handlers in the frontend. Adding a new event means: define it in math -> add its type in the frontend book-event types -> write its handler/animation. See `web-sdk/documentation`.
- Live dev: `pnpm dev` in the app folder (port 3001), storybook via `pnpm storybook`.
- Dev-mode connection uses URL params: `?sessionID=...&rgs_url=...&lang=en&currency=USD`.
  You get real values by launching your uploaded game from the ACP Developer page and copying the query string.

## Step 5: Publish to Stake Engine (Admin Control Panel)
1. Create/log in to your Stake Engine account and create a game in the ACP.
2. **Files -> Math**: upload everything in `games/<game>/library/publish_files/` (index.json + lookUpTable CSVs + books .jsonl.zst). Preliminary format checks run automatically. Publish -> Math.
3. **Files -> Front End**: upload the whole `build` folder. Publish -> Front End.
4. **Developer** page: Start game session -> Launch in New Tab. This is a live staging build.
5. Copy the query string from that URL to develop locally against the real RGS.

RGS flow your frontend uses: `/wallet/authenticate` (on load) -> `/wallet/play` (bet) -> animate events -> `/wallet/end-round`.
The `stake-engine-client` npm package wraps these calls if you build your own frontend.

## Step 6: Submit for review
Rules from the approval guidelines: strictly stateless (no jackpots, gamble features, continuation, early cashout); original IP only; you must provide a short theme/mechanics blurb + description tag. Review applies to a specific frontend + math version, and after approval the math cannot change.

## Gotchas I hit (so you don't)
1. Run `run.py` from the **math-sdk root** (`python games/x/run.py`), otherwise stats files fail to write.
2. Rust >= 1.76 required: `toml_parser` fails to compile on 1.75.
3. Optimizer targets that don't sum to the game RTP trigger `Optimization RTP does not match betmode RTP`.
4. The optimizer rewrites `optimization_program/src/setup.toml` for the active game; that is expected.
5. Frontend: `pnpm build` inside an app fails (workspace packages unbuilt). Use `pnpm turbo run build --filter=./apps/<app>` from web-sdk root.
6. Optimization on a 1-core machine is slow (minutes); use more cores for large sim counts.
7. Simulation with `run_optimization=False` shows RTP violations by design: unoptimized books are not weighted to target.
8. Before regenerating books or changing modes, re-check hardcoded frontend values (mode names, RTP text, max win).
