from discord.ext import commands
import discord, config, sql
from stocks import currency, stockData, symbolSearch

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)

@bot.command()
async def help(ctx):
    """Help function to list all bot commands"""
    msg = discord.Embed(title='Commands', color=0xC0C0C0)
    msg.add_field(name="!info <stock>", value='Display stock overview', inline=False)
    msg.add_field(name="!price <stock>", value="Get the stock's current price", inline=False)
    msg.add_field(name="!add <stock", value='Add a stock to your portfolio', inline=False)
    msg.add_field(name="!remove <stock>", value='Remove a stock from your portfolio', inline=False)
    msg.add_field(name="!portfolio <portfolio name>", value='Display contents of a portfolio', inline=False)
    msg.add_field(name="!create <portfolio name>", value='Create a portfolio', inline=False)
    msg.add_field(name="!delete <portfolio name>", value='Delete your portfolio', inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def price(ctx, keyword:str):
    """get stock price"""
    try:
        stock_data = stockData(symbolSearch(keyword))['Global Quote']
    except:
        await ctx.send("I couldn't find anything for '" + keyword + "'. Try using a different keyword!")
        return
    # create message
    response = stock_data['01. symbol'] + ' - ' + currency(stock_data['05. price'])
    await ctx.send(response)

@bot.command()
async def info(ctx, keyword:str):
    """get all stock info"""
    try:
        stock_data = stockData(symbolSearch(keyword))['Global Quote']
    except:
        await ctx.send("I couldn't find anything for '" + keyword + "'. Try using a different keyword!")
        return
    # create message
    msg = discord.Embed(title=stock_data['01. symbol'], color=0x000000)
    msg.add_field(name="Price", value=currency(stock_data['05. price']), inline=False)
    msg.add_field(name="Open", value=currency(stock_data['02. open']), inline=True)
    msg.add_field(name="High", value=currency(stock_data['03. high']), inline=True)
    msg.add_field(name="Low", value=currency(stock_data['04. low']), inline=True)
    msg.add_field(name="Prev close", value=currency(stock_data['08. previous close']), inline=True)
    msg.add_field(name="Change", value=currency(stock_data['09. change']), inline=True)
    msg.add_field(name="Change %", value=stock_data['10. change percent'], inline=True)
    await ctx.send(embed = msg)

@bot.command()
async def create(ctx):
    """creates a portfolio with a given name - store in SQL db"""
    await ctx.send(response)

@bot.command()
async def portfolio(ctx):
    """displays the contents of a given portfolio - default is your portfolio"""
    await ctx.send(response)

@bot.command()
async def delete(ctx):
    """deletes your current portfolio"""
    await ctx.send(response)

@bot.command()
async def remove(ctx):
    """removes a given stock from your portfolio"""
    await ctx.send(response)

@bot.command()
async def add(ctx):
    """adds a given stock from your portfolio"""
    await ctx.send(response)


bot.run(config.TOKEN)