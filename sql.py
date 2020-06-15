import pyodbc 
import config

# configuration
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SERVER+';DATABASE='+config.DATABASE+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

# create new portfolio in the database
def addPortfolio(name, owner, server):
    """
    params
        name: string - desired name of portfolio
        owner: int - the user creating the portfolio (ID)
        server: int - server that the user resides on (ID)
    return
        resulting message
    """
    try:
        cursor.execute("INSERT INTO PORTFOLIOS (NAME, OWNER, SERVER) VALUES ('{}', '{}', '{}');".format(name, owner, server))
        cnxn.commit()
        return '{} has been created.'.format(name)
    except:
        return '{} Error! Either this portfolio name is taken or you already have one created.'

# remove a portfolio from the database
def deletePortfolio(name, owner):
    """
    deletes a given portfolio from the sql table
    params
        name: string - name of portfolio
    """
    cursor.execute("DELETE FROM PORTFOLIOS WHERE PORTFOLIOS.NAME = '{}' AND PORTFOLIOS.OWNER = '{}';".format(name, owner))
    cnxn.commit()
 
# list all current portfolios
def allPortfolios():
    """
    return all portfolios from the sql table
    returns
        ports: array - all portfolios in the sql table
    """
    ports = []
    cursor.execute("SELECT Name, Owner, Server from PORTFOLIOS")
    row = cursor.fetchone() 
    while row: 
        ports.append(row)
        row = cursor.fetchone()
    return ports
    
# list the contents of a portfolio
def openPortfolio():
    cursor.execute("")
    cnxn.commit()

# add a stock to a portfolio
def addStock():
    cursor.execute("")
    cnxn.commit()

# remove a stock from a portfolio
def removeStock():
    cursor.execute("")
    cnxn.commit()
    



