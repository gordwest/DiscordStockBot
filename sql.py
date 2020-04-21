import pyodbc 
import config

# configuration

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SERVER+';DATABASE='+config.DATABASE+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

# create new portfolio in the database
def addPortfolio():
    cursor.execute("INSERT INTO teams(name, owner, server) VALUES ('', '', '')")
    cnxn.commit()

# remove a portfolio from the database
def deletePortfolio():
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
    
# list the contents of a portfolio
def showPortfolio():
    cursor.execute("")
    cnxn.commit()


