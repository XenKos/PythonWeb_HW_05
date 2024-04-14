import aiohttp
import asyncio
from datetime import datetime, timedelta

async def get_exchange_rate_for_date(selected_date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={selected_date.strftime('%d.%m.%Y')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['exchangeRate']
            else:
                raise ValueError(f"Failed to fetch exchange rates for {selected_date}") 
                       
async def get_exchange_rates(last_n_days):
    dates = [datetime.now() - timedelta(days=i) for i in range(last_n_days)]
    tasks = [get_exchange_rate_for_date(date) for date in dates]
    return await asyncio.gather(*tasks)
    
def print_exchange_rates(exchange_rates):
    for rate in exchange_rates:
        print(f"Date: {rate['date']}, USD: {rate['USD']}, EUR: {rate['EUR']}")

async def main():
    try:
        last_n_days = 10  
        exchange_rates = await get_exchange_rates(last_n_days)
        print_exchange_rates(exchange_rates)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
