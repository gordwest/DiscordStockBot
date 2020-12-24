import discord, config, sql
from discord.ext import commands
from stocksAPI import currencyFormat, getStockData, stockSearch
from sql import addPortfolio, getAllPortfolios, deletePortfolio, searchPortfolio, addStock, checkStock, openPortfolio, removeStock, emptyPortfolio

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
    msg.add_field(name="!view <portfolio name>", value='Display contents of a portfolio', inline=False)
    msg.add_field(name="!all", value='Display all current portfolios', inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def search(ctx, keyword:str):
    """Get information for a given stock
    params
        keyword: string - the keyword used to search for a stock
    returns
        response: all current information on stock (open, high, low, price, change %, etc..)
    """
    try:
        stock_data = stockSearch(keyword)
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
    """Creates a portfolio with a given name - store in SQL db
    params
        name: string - name of the portfolio you want to create
    return
        response: string - resulting output of the operation (success/failed)
    """
    response = addPortfolio(name, ctx.author)
    await ctx.send(response)

@bot.command()
async def delete(ctx, name):
    """Deletes a given portfolio if the author is the owner
    param
        name: string - name of the portfolio to delete
    """
    results = searchPortfolio(name) # search for portfolio name
    if len(results) == 1:
        if results[0][1] == str(ctx.author): # check if author is the owner
            deletePortfolio(name, ctx.author)
            emptyPortfolio(name) # remove all stocks from table that are linked to the portfolio
            response = '{} has been deleted.'.format(name)
        else: # portfolio exists and author is not owner
            response = "Error! Not allowed to delete another user's portfolio." 
    else: # portfolio name doesn't exist
        response = 'Error! Please verify the portfolio name.' 
    await ctx.send(response)

@bot.command()
async def all(ctx):
    """Displays all the portfolios on the server
    returns
        response: msg - list of all portfolios from the current server
    """
    allPortfolios = getAllPortfolios()

    msg = discord.Embed(title='Current Portfolios', color=0x000000)
    for portfolio in allPortfolios:
        msg.add_field(name=portfolio[0], value=portfolio[1], inline=False)
    await ctx.send(embed = msg)

@bot.command()
async def add(ctx, stock):
    """Adds a given stock to the author's portfolio
    params
        stock: string - name of stock to search, adds the stock that is returned from the search
    """
    try:
        stock_symbol = stockSearch(stock)['1. symbol'] # return stock symbol from author's search
        try:
            portfolioName = searchPortfolio(ctx.author)[0][0] # get name of the author's portfolio
            if len(checkStock(portfolioName, stock_symbol)) == 0: # check if stock already exists in portfolio
                addStock(portfolioName, stock_symbol) # add new row to stock table with author's portfolio and stock symbol
                response = '{} has been added to {}'.format(stock_symbol, portfolioName)
            else:
                response = 'Error! This stock is already in your portfolio!'
        except:
            response = 'Error! You need a portfolio before you can add stocks!'
    except:
        response = "Error! I couldn't find that stock!"
    await ctx.send(response)

@bot.command()
async def remove(ctx, stockSymbol):
    """Removes a given stock from the author's portfolio
    params
        stockSymbol: string - symbol of the stock that will be removed
    """
    #check if stock is in portfolio
    portfolioName = searchPortfolio(ctx.author)[0][0] # get name of the author's portfolio
    if len(checkStock(portfolioName, stockSymbol)) > 0: # check if stock is currently in portfolio
        removeStock(stockSymbol, portfolioName) # execute sql query
        msg = discord.Embed(title='{} has been removed from your portfolio.'.format(stockSymbol), color=0x000000)
    else:
        msg = discord.Embed(title='Error! {} is not in your portfolio.'.format(stockSymbol), color=0x000000)
    await ctx.send(embed = msg)

@bot.command()
async def view(ctx, portfolioName=''): 
    """Display the contents of a given portfolio
    params
        portfolioName: string - name of portfolio to query
    """
    if portfolioName == '': # use authors portfolio is none is specified
        portfolioName = searchPortfolio(ctx.author)[0][0] 

    results = searchPortfolio(portfolioName) # search for portfolio name
    if len(results) == 1:
        stocks = openPortfolio(portfolioName) # query stocks from table
        if len(stocks) > 0:
            msg = discord.Embed(title=portfolioName, color=0x000000)
            for stock in stocks:
                msg.add_field(name=stock[0], value='0 Shares', inline=True) 
        else:
            msg = discord.Embed(title='This portfolio is emtpy!', color=0x000000)
    else: # portfolio doesn't exist
        msg = discord.Embed(title="There is no portfolio named '{}'".format(portfolioName), color=0x000000)
    await ctx.send(embed = msg)

bot.run(config.TOKEN)