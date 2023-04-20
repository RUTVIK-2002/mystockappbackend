import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockapp.settings')
django.setup()
import pandas as pd
from base.models import Stock
from base import variablesetter


df = pd.read_csv('shifts_years_finder.csv')

id_list = [stock.id for stock in Stock.objects.all()]
print(id_list)

for i in id_list:
    stock = Stock.objects.get(id=i)
    shifts, years = variablesetter.setter(str(stock.name.ticker))
    # stock.name.shifts = shifts
    # stock.name.years = years
    #print(stock.name.ticker,stock.name.shifts,stock.name.years)
    #stock.save()
    #stock.refresh_from_db()  # Reload the stock object from the database
    new_data = {'ticker': stock.name.ticker, 'shifts': shifts, 'years': years}
    
    # Set the 'name' column as the DataFrame index
    df.set_index('ticker', inplace=True)

    # Update or add the row in the DataFrame
    df.loc[new_data['ticker']] = new_data

    # Reset the index of the DataFrame
    df.reset_index(inplace=True)

    # Print the updated DataFrame
    df.to_csv('shifts_years_finder.csv')