import discord
import json
import os
import datetime as dt
from discord.ext import commands
from csstatsgg import get_result, get_result_over
import asyncio
import random

with open(r"discord_token.txt", "r") as file:
    bot_token = file.read()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command('help')

users = {}
bets = []
active_bet = None
available_metrics = ['K', 'D', 'A', 'HS%', 'ADR']
metric_upper_limits = {'K': float(35),
                       'D': float(20),
                       'A': float(15),
                       'HS%': float(90),
                       'ADR': float(120)}

metric_lower_limits = {'K': float(8),
                       'D': float(10),
                       'A': float(0),
                       'HS%': float(30),
                       'ADR': float(50)}

def save_user():
    users_dict = {user_id: user.to_dict() for user_id, user in users.items()}
    with open('users.json', 'w') as file:
            json.dump(users_dict, file, indent=4)

class User:
    def __init__(self, id, credits = 1000, wins = 0 , losses = 0, current_bet = None, times_begged = 0, amount_begged = 0, last_begged = None):
        self.id = id
        self.credits = credits
        self.wins = wins
        self.losses = losses
        self.current_bet = current_bet
        self.times_begged = times_begged
        self.amount_begged = amount_begged
        self.last_begged = last_begged

    def to_dict(self):
        if self.last_begged is None:
            self.last_begged = None
        elif isinstance(self.last_begged, str):
            self.last_begged = self.last_begged
        else:
            self.last_begged = self.last_begged.isoformat()

        return {
            "id": self.id,
            "credits": self.credits,
            "wins": self.wins,
            "losses": self.losses,
            "current_bet": self.current_bet,
            "times_begged": self.times_begged,
            "amount_begged": self.amount_begged,
            "last_begged": self.last_begged
    
        }
    @classmethod
    def from_dict(cls, data):
        if data.get("last_begged") is None:
            last_begged = None
        else:
            last_begged = dt.datetime.fromisoformat(data.get("last_begged"))
        return cls(
            id=data.get("id"),
            credits=data.get("credits"),
            wins=data.get("wins"),
            losses=data.get("losses"),
            current_bet=data.get("current_bet"),
            times_begged = data.get("times_begged"),
            amount_begged = data.get("ammount_begged"),
            last_begged = last_begged
        )
    
class Bet:
    def __init__(self, type = 'win', metric = None):
        self.active = True
        self.resolved = False
        self.bets_for = {}
        self.bets_against = {}
        self.created = dt.datetime.now()
        self.type = type
        self.metric = metric

if os.path.exists('users.json'):
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        users = {int(user_id): User.from_dict(user_data) for user_id, user_data in users_data.items()}
else:
    users = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='register')
async def register(ctx):
    if ctx.author.id not in users:
        users[ctx.author.id] = User(ctx.author.id)
        await ctx.send(f"{ctx.author.name} has been registered with 1000 credits!")
        save_user()
    else:
        await ctx.send(f"{ctx.author.name}, you are already registered.")

@bot.command(name='user_info')
async def user_info(ctx):
    user = users.get(ctx.author.id)
    if user is None:
        await ctx.send("You need to register first with !register.")
    else:
        await ctx.send(f"User: {ctx.author.name}\ncredits: {user.credits}\nwins: {user.wins}\nlosses: {user.losses}\ntimes_begged: {user.times_begged}\namount_begged: {user.amount_begged}\nlast_begged: {user.last_begged}")

@bot.command(name='help')
async def help(ctx):
    await ctx.send("""$register - register yourself to participate in betting
                   \n$user_info - show your credits, wins and losses
                   \n$newbet - create a new bet for the most recent game, this will track if epasts has won or lost the game
                   \n$newbetover [metric] [amount] - create an over bet for the most recent epasts game for these metrics: Kills (K), Deaths (D), Assists (A), Headshot percentage (HS%), ADR (ADR)
                   \n$betfor [amount] - bet for the current active bet. For $newbet you are betting for a game Win. For $newbetover you are betting for a larger value than the entered amount
                   \n$betagainst [amount] - bet for the current active bet. For $newbet you are betting for a game Loss or Draw. For $newbetover you are betting for a smaller or equal value than the entered amount
                   \n$resolvebet - resolve the current active bet
                   \n$beg - beg for a blessing if you are out of credits. You can do this once every 18 hours""")
    return

@bot.command(name='beg')
async def beg(ctx):
    user = users.get(ctx.author.id)
    if user.last_begged is not None:
        if user.last_begged + dt.timedelta(hours = 18) > dt.datetime.now():
            await ctx.send("You have already received your blessing today.")
            return
        
    blessing_amount = random.randint(10,100)
    user.credits += blessing_amount
    if user.amount_begged is None:
        user.amount_begged = blessing_amount
    else:
        user.amount_begged += blessing_amount
    user.times_begged += 1
    user.last_begged = dt.datetime.now()

    await ctx.send(f"{ctx.author.name} has been blessed with {blessing_amount} credits")
    return

@bot.command(name='newbet')
async def new_bet(ctx):
    global active_bet
    if active_bet is not None and active_bet.active:
        await ctx.send("A bet is already active. Wait until betting ends and resolve the current bet before creating a new one!")
        return
    elif active_bet is not None and  not active_bet.resolved:
        await ctx.send("Please resolve the previous bet before creating a new one!")
        return
    
    active_bet = Bet('win')
    bets.append(active_bet)
    await ctx.send("A new bet has been created! You can bet using $betfor if you expect a Win or $betagainst if you expect a loss. You have 3 minutes to place the bet")
    await asyncio.sleep(120)
    await ctx.send("You have 1 minute left until the bet is closed")
    await asyncio.sleep(60)
    active_bet.active = False
    await ctx.send("Betting has been closed.")

@bot.command(name='newbetover')
async def new_bet(ctx, betmetric : str, amount : float):
    global active_bet
    if active_bet is not None and active_bet.active:
        await ctx.send("A bet is already active. Wait until betting ends and resolve the current bet before creating a new one!")
        return
    elif active_bet is not None and  not active_bet.resolved:
        await ctx.send("Please resolve the previous bet before creating a new one!")
        return
    
    if betmetric not in available_metrics:
        await ctx.send("Please enter a valid metric! Available metrics " + " ".join(map(str, available_metrics)))
        return
    
    if amount > metric_upper_limits[betmetric] or amount < metric_lower_limits[betmetric]:
        await ctx.send(f"Over amount is out of range, acceptable range for {betmetric} is from {metric_lower_limits[betmetric]} to {metric_upper_limits[betmetric]}")
        return
    
    active_bet = Bet(betmetric, amount)
    bets.append(active_bet)
    await ctx.send(f"A new bet has been created! You can bet using $betfor if you expect {betmetric} to be over {amount} or $betagainst if you expect {betmetric} to be under or equal {amount}. You have 3 minutes to place the bet")
    await asyncio.sleep(120)
    await ctx.send("You have 1 minute left until the bet is closed")
    await asyncio.sleep(60)
    active_bet.active = False
    await ctx.send("Betting has been closed.")


@bot.command(name='betfor')
async def bet_for(ctx, amount: int):
    global active_bet
    if active_bet is None or not active_bet.active:
        await ctx.send("There is no active bet right now.")
        return

    user = users.get(ctx.author.id)
    if user is None:
        await ctx.send("You need to register first with $register.")
        return

    if user.current_bet is not None:
        await ctx.send("You can only place one bet per active bet.")
        return

    if user.credits < amount:
        await ctx.send("You do not have enough credits to place this bet.")
        return

    user.credits -= amount
    user.current_bet = ('for', amount)
    active_bet.bets_for[ctx.author.id] = amount
    await ctx.send(f"{ctx.author.name} bet {amount} credits for a win.")

@bot.command(name='betagainst')
async def bet_against(ctx, amount: int):
    global active_bet
    if active_bet is None or not active_bet.active:
        await ctx.send("There is no active bet right now.")
        return

    user = users.get(ctx.author.id)
    if user is None:
        await ctx.send("You need to register first with $register.")
        return

    if user.current_bet is not None:
        await ctx.send("You can only place one bet per active bet.")
        return

    if user.credits < amount:
        await ctx.send("You do not have enough credits to place this bet.")
        return

    user.credits -= amount
    user.current_bet = ('against', amount)
    active_bet.bets_against[ctx.author.id] = amount
    await ctx.send(f"{ctx.author.name} bet {amount} credits for a loss.")

@bot.command(name='resolvebet')
async def resolve_bet(ctx):
    global active_bet
    if active_bet is None:
        await ctx.send("There is no active bet to resolve.")
        return
    if active_bet.active:
        await ctx.send("The current bet is still active")
        return

    if active_bet.type == 'win':
        result = await get_result(active_bet.created)
        
        while result == 'Pending':
            await ctx.send("Match still in progress, checking again in 10 minutes")
            await asyncio.sleep(600)
            result = await get_result(active_bet.created)
        
        
        if result == "DQ":

            for user_id, amount in active_bet.bets_against.items():
                users[user_id].credits += amount
            
            for user_id, amount in active_bet.bets_for.items():
                users[user_id].credits += amount
            await ctx.send("Invalid bet: Posted too soon. Refunds are issued")
            return

        # Resolve the bet
        winners = []
        losers = []
        if result == "W":
            winners = active_bet.bets_for
            losers = active_bet.bets_against
        elif result == "L" or result == 'D':
            winners = active_bet.bets_against
            losers = active_bet.bets_for

        # Payouts to winners
        for user_id, amount in winners.items():
            users[user_id].credits += 2 * amount
            users[user_id].wins += 1
            users[user_id].current_bet = None

        # Losses recorded for losers
        for user_id, amount in losers.items():
            users[user_id].losses += 1
            users[user_id].current_bet = None

        winners_name = []
        losers_name = []

        for user_id, amount in losers.items():
            username = await bot.fetch_user(user_id)
            losers_name.append(username)

        for user_id, amount in winners.items():
            username = await bot.fetch_user(user_id)
            winners_name.append(username)

        active_bet.resolved = True
        await ctx.send(f"The bet has been resolved. Result: {result}. Winners:" + " ".join(map(str, winners_name)) + ". Losers: " + " ".join(map(str, losers_name)))
        save_user()

    else:
        result = await get_result_over(active_bet.created, active_bet.type)
        
        while result == 'Pending':
            await ctx.send("Match still in progress, checking again in 10 minutes")
            await asyncio.sleep(600)
            result = await get_result_over(active_bet.created, active_bet.type)
        
        
        if result == "DQ":

            for user_id, amount in active_bet.bets_against.items():
                users[user_id].credits += amount
            
            for user_id, amount in active_bet.bets_for.items():
                users[user_id].credits += amount
            await ctx.send("Invalid bet: Posted too soon. Refunds are issued")
            return

        # Resolve the bet
        winners = []
        losers = []
        if result > active_bet.metric:
            winners = active_bet.bets_for
            losers = active_bet.bets_against
        elif result <= active_bet.metric:
            winners = active_bet.bets_against
            losers = active_bet.bets_for

        # Payouts to winners
        for user_id, amount in winners.items():
            users[user_id].credits += 2 * amount
            users[user_id].wins += 1
            users[user_id].current_bet = None

        # Losses recorded for losers
        for user_id, amount in losers.items():
            users[user_id].losses += 1
            users[user_id].current_bet = None

        winners_name = []
        losers_name = []

        for user_id, amount in losers.items():
            username = await bot.fetch_user(user_id)
            losers_name.append(username)

        for user_id, amount in winners.items():
            username = await bot.fetch_user(user_id)
            winners_name.append(username)

        active_bet.resolved = True
        await ctx.send(f"The bet has been resolved. Result: {result}. Winners:" + " ".join(map(str, winners_name)) + ". Losers: " + " ".join(map(str, losers_name)))
        save_user()

bot.run(bot_token)