# GoalBet
website: https://goalbet-frontend-prod.s3.amazonaws.com/about

MVP backend (FastAPI). Start: `uvicorn app.main:app --reload --port 8080`

Goalbet is where goals meet accountability. We solve procrastination by making your goals public, fun, and fueled by community bets.

# Core idea of the business
- the problem we're solving:
  Most people fail their goals because:
  1. No accountability (nobody cares if you quit)
  2. Low motivation (hard to push alone)
  3. No excitement (goals feel boring/private)
- Our solution:
  Public accountability -> when people are watching, you're more likely to finish (such as marathon)
  Gamification -> betting turns goals into a fun, competitive game.
  Social engagement -> spectators participate, not just watch.
- Business Core:
  We create a social accountability + gamified betting platform
  The currency economy keeps user engaged and give us monetization (coins purchase, ad-free, vouchers)
  Unlike habit apps (boring) or gambling apps (risk), we combine fun + productivity

# App functions:
1. Post a goal: Set your own goal + deadline; stake virtual coins to prove commitment; others bet for/against you.
2. Betting system: community bets coins on your success/failure; if you succeed -> you and supporters win; if you fail -> doubters win
3. Proof of completion: upload proof; if it is a built-in goal, you should provide the proof as required; if it is a customed goal, it need mannually check if your goal is completed or not.
4. Coin Economy:
  Earn coins by: Completing your goal, winning bets, finishing bounty missions from others.
  Spend coins on: Ad-free experience, in-app perks (badges, boosts, premium roles)
  Redeem vouchers/partner rewards
5. Bounty missions
  You can post a mission (e.g., "run a marathon")
  Set the bounty to reward
  Others accept -> submit proof
  Once verified, they earn the bounty
  Once they failed, they have to pay back their coins
6. Community Features:
  leaderboards: Top achievers, best bettors, bounty hunters
  trending challenges feed
  follow + comment system
