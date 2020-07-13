import pyodbc 
import config

# configuration
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SERVER+';DATABASE='+config.DATABASE+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

# create new portfolio in the database
def addPortfolio(name, owner):
    """
    create a new portfolio in the sql database table
    params
        name: string - desired name of portfolio
        owner: string - owner of the portfolio (discord name)
    return
        resulting message
    """
    try:
        cursor.execute("INSERT INTO PORTFOLIOS (NAME, OWNER) VALUES ('{}', '{}');".format(name, owner))
        cnxn.commit()
        return '{} has been created.'.format(name)
    except:
        return 'Error! This name is taken or you already have a portfolio.'

# remove a portfolio from the database
def deletePortfolio(name, owner):
    """
    deletes a given portfolio from the sql table
    params
        name: string - name of portfolio
        owner: string - owner of the portfolio (discord name)
    """
    cursor.execute("DELETE FROM PORTFOLIOS WHERE NAME = '{}' AND OWNER = '{}';".format(name, owner))
    cnxn.commit()

def searchPortfolio(name):
    """Search the sql table for a specific portfolio 
    params
        name: string - name of portfolio
        owner: string - owner of the portfolio (discord name)
    """
    portfolios = []
    cursor.execute("SELECT Name, Owner FROM PORTFOLIOS WHERE NAME = '{}' or OWNER = '{}';".format(name, name))
    row = cursor.fetchone() 
    while row: 
        portfolios.append(row)
        row = cursor.fetchone()
    return portfolios
 
# list all current portfolios
def getAllPortfolios():
    """
    return all portfolios from the sql table
    returns
        portfolios: array - all portfolios in the sql table
    """
    portfolios = []
    cursor.execute("SELECT Name, Owner from PORTFOLIOS")
    row = cursor.fetchone() 
    while row: 
        portfolios.append(row)
        row = cursor.fetchone()
    return portfolios
    
# add a stock to a portfolio
def addStock(portfolio, stockSymbol):
    """Add a given stock to the user's portfolio
    params
        portfolio: string - name of portfolio to add stock to
        stockSymbol = string - stock symbol to be added
    """
    cursor.execute("INSERT INTO STOCKS (PORTFOLIO, STOCK) VALUES ('{}', '{}');".format(portfolio, stockSymbol)) # insert row into table
    cnxn.commit()

def removeStock(stock, portfolioName):
    """Removes a stock from a given portfolio
    params
        stock: string - symbol of stock to remove
        portfolio: string - name of portfolio to use in query (author's portfolio)
    """
    cursor.execute("DELETE FROM STOCKS WHERE STOCK = '{}' AND PORTFOLIO = '{}';".format(stock, portfolioName))
    cnxn.commit()

def openPortfolio(portfolio):
    """Return all the stocks in a given portfolio
    params
        portfolio: string - name of portfolio to use in query
    """
    stocks = []
    cursor.execute("SELECT STOCK FROM STOCKS WHERE PORTFOLIO = '{}'".format(portfolio))
    row = cursor.fetchone() 
    while row: 
        stocks.append(row)
        row = cursor.fetchone()
    return stocks    

def checkStock(portfolio, stockSymbol):
    """Check to see if a stock exists in a portfolio
    params
        portfolio: string - name of portfolio to check
        stockSymbol: string - stock to check
    returns
        stocks: list - results from query
    """
    stocks = []
    cursor.execute("SELECT PORTFOLIO, STOCK FROM STOCKS WHERE PORTFOLIO = '{}' AND STOCK = '{}'".format(portfolio, stockSymbol))
    row = cursor.fetchone() 
    while row: 
        stocks.append(row)
        row = cursor.fetchone()
    return stocks

def emptyPortfolio(portfolioName):
    """Deletes all stock records for a given portfolio (call when a user deletes their portfolio)
    params
        portfolioName: string - name of the author's portfolio
    """
    cursor.execute("DELETE FROM STOCKS WHERE PORTFOLIO = '{}';".format(portfolioName))
    cnxn.commit()