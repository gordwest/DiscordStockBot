from discord.ext import commands
import discord, config, sql
from stocks import currency, stockData, symbolSearch
from sql import addPortfolio, allPortfolios, deletePortfolio

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)

@bot.command()
async def help(ctx):
    """Help function to list all bot commands"""
    msg = discord.Embed(title='Commands', color=0xC0C0C0)
    msg.add_field(name="!info <search keyword>", value='Stock complete overview', inline=False)
    msg.add_field(name="!price <search keyword>", value="Current price of a stock", inline=False)
    msg.add_field(name="!add <stock symbol>", value='Add a stock to your portfolio', inline=False)
    msg.add_field(name="!remove <stock symbol>", value='Remove a stock from your portfolio', inline=False)
    msg.add_field(name="!view <portfolio name>", value='Display contents of a portfolio', inline=False)
    msg.add_field(name="!create <portfolio name>", value='Create a portfolio', inline=False)
    msg.add_field(name="!delete <portfolio name>", value='Delete your portfolio', inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def price(ctx, keyword:str):
    """
    Get the current price of a stock
    params
        keyword: string - search keyword to find stock
    returns
        response: current price of stock 
    """
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
    """
    Get information of a stock
    params
        keyword: string - search keyword to find stock
    returns
        response: all current information on stock (open, high, low, price, change %, etc..)
    """
    try:
        stock_data = stockData(symbolSearch(keyword))['Global Quote']
    except:
        await ctx.send("I couldn't find anything for '" + keyword + "'. Please try again with a different keyword.")
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
async def create(ctx, name):
    """
    creates a portfolio with a given name - store in SQL db
    params
        name: string - name of the portfolio you are creating
    return
        response: string - resulting output of the operation (success/failed)
    """
    response = addPortfolio(name, ctx.author.id, 11213245)
    await ctx.send(response)

@bot.command()
async def delete(ctx, name):
    """
    deletes your current portfolio
    param
        name: string - name
    """
    deletePortfolio(name, ctx.author.id)
    response = '{} has been deleted.'.format(name)
    await ctx.send(response)

@bot.command()
async def all(ctx):
    """
    Displays all the portfolios on the server
    returns
        response: string - list of all portfolios from the current server
    """
    allPorts = allPortfolios()
    t = 'CURRENT PORTFOLIOS: \n'
    ports = []
    for p in allPorts:
        ports.append(p[0])
    response = t + '\n\t '.join(ports)
    await ctx.send(response)

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