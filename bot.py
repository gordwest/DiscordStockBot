from discord.ext import commands
import discord, config, sql
from stocksAPI import currencyFormat, getStockData, symbolSearch
from sql import addPortfolio, getAllPortfolios, deletePortfolio

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)

@bot.command()
async def help(ctx):
    """Help function to list all bot commands"""
    msg = discord.Embed(title='Commands', color=0xC0C0C0)
    msg.add_field(name="!search <search keyword>", value='Stock overview', inline=False)
    msg.add_field(name="!create <portfolio name>", value='Create a portfolio', inline=False)
    msg.add_field(name="!delete <portfolio name>", value='Delete your portfolio', inline=False)
    msg.add_field(name="!add <stock symbol>", value='Add a stock to your portfolio', inline=False)
    msg.add_field(name="!remove <stock symbol>", value='Remove a stock from your portfolio', inline=False)
    msg.add_field(name="!open <portfolio name>", value='Display contents of a portfolio', inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def search(ctx, keyword:str):
    """
    Get information of a stock
    params
        keyword: string - search keyword to find stock
    returns
        response: all current information on stock (open, high, low, price, change %, etc..)
    """
    try:
        stock_data = symbolSearch(keyword)
        quote_data = getStockData(stock_data['1. symbol'])
    except:
        await ctx.send("I couldn't find anything for '" + keyword + "'. Please try again with a different keyword.")
        return
    # create message
    msg = discord.Embed(title=stock_data['2. name'], color=0x000000)
    msg.add_field(name="Ticker", value=quote_data['01. symbol'], inline=True)
    msg.add_field(name="Price", value=currencyFormat(quote_data['05. price']), inline=True)
    msg.add_field(name="Currency", value=stock_data['8. currency'], inline=True)
    msg.add_field(name="Open", value=currencyFormat(quote_data['02. open']), inline=True)
    msg.add_field(name="High", value=currencyFormat(quote_data['03. high']), inline=True)
    msg.add_field(name="Low", value=currencyFormat(quote_data['04. low']), inline=True)
    msg.add_field(name="Prev close", value=currencyFormat(quote_data['08. previous close']), inline=True)
    msg.add_field(name="Change", value=currencyFormat(quote_data['09. change']), inline=True)
    msg.add_field(name="Change %", value=quote_data['10. change percent'], inline=True)
    await ctx.send(embed = msg)

@bot.command()
async def create(ctx, name):
    """
    creates a portfolio with a given name - store in SQL db
    params
        name: string - name of the portfolio you are creating
    return
        response: string - resulting output of the operation (success/failed)
    """
    response = addPortfolio(name, ctx.author, 11213245)
    await ctx.send(response)

@bot.command()
async def delete(ctx, name):
    """
    deletes your current portfolio
    param
        name: string - name
    """
    deletePortfolio(name, ctx.author)
    response = '{} has been deleted.'.format(name)
    await ctx.send(response)

@bot.command()
async def all(ctx):
    """
    Displays all the portfolios on the server
    returns
        response: string - list of all portfolios from the current server
    """
    allPortfolios = getAllPortfolios()

    msg = discord.Embed(title='Current Portfolios', color=0x000000)
    for portfolio in allPortfolios:
        msg.add_field(name=portfolio[0], value=ctx.author, inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def open(ctx, name):
    """displays the contents of a given portfolio - default is your portfolio"""
    await ctx.send(response)

@bot.command()
async def remove(ctx, stock):
    """removes a given stock from your portfolio"""
    await ctx.send(response)

@bot.command()
async def add(ctx, stock):
    """adds a given stock from your portfolio"""
    await ctx.send(response)


bot.run(config.TOKEN)