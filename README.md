# Discord Betting Bot

## Overview
This bot allows users to participate in a betting system for competitive gaming matches. Users can register, place bets on match outcomes or specific performance metrics, and resolve bets based on actual results. The bot manages user balances, tracks wins and losses, and provides a credit-begging feature for those who run out of credits.

## Features
- **User Registration:** Users can register to start betting.
- **Bet Placement:** Users can place bets on match outcomes (win/loss) or performance metrics (Kills, Deaths, Assists, HS%, ADR).
- **Automated Bet Resolution:** The bot fetches match results and resolves bets accordingly.
- **Credit Management:** Users gain or lose credits based on bet results.
- **Begging System:** Users who run out of credits can beg for a small amount once every 18 hours.

## Commands
| Command | Description |
|---------|-------------|
| `$register` | Registers the user with an initial credit balance of 1000. |
| `$user_info` | Displays the user's current credit balance, wins, losses, and betting history. |
| `$newbet` | Starts a new bet on whether "epasts" wins or loses the most recent game. |
| `$newbetover [metric] [amount]` | Starts a bet on whether a certain performance metric exceeds a given amount. Metrics: K, D, A, HS%, ADR. |
| `$betfor [amount]` | Places a bet in favor of the current active bet. |
| `$betagainst [amount]` | Places a bet against the current active bet. |
| `$resolvebet` | Resolves the current bet based on real match data. |
| `$beg` | Allows users to request additional credits if they have run out. Can only be used once every 18 hours. |

## Betting System
### Available Metrics for `$newbetover`
- **K (Kills):** Number of kills in a match.
- **D (Deaths):** Number of deaths in a match.
- **A (Assists):** Number of assists in a match.
- **HS% (Headshot Percentage):** Percentage of headshots in a match.
- **ADR (Average Damage per Round):** Damage dealt per round.

### Betting Rules
- Each user can place only one bet per active betting session.
- Bets must be placed within the 3-minute betting window.
- The system ensures fair payouts, doubling the credits for winning bets.
- If the match is still in progress, the bot will check periodically until a result is available.
- Invalid bets due to early placement will result in a refund.

## Installation
1. Install dependencies:
   ```sh
   pip install discord.py csstatsgg
   ```
2. Place your Discord bot token inside `discord_token.txt`.
3. Run the bot:
   ```sh
   python bot.py
   ```

## Configuration
- The bot reads user data from `users.json`. If the file does not exist, it will be created automatically.
- Modify `metric_upper_limits` and `metric_lower_limits` in the script to adjust acceptable bet ranges for different metrics.
- In csstatsgg.py functions enter a link to a player you want to use for tracking and betting

## Future Improvements
- Add logging for better tracking of bet resolutions.
- Add the ability to bet on multiple players
- Introduce leaderboards for the highest earners.
- Expand betting options for more in-depth analytics.

## License
This project is open-source and available for modification and contribution.

