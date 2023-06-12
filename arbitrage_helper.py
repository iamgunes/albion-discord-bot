import aiohttp

async def arbitrage(item_name):
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            bm_data = []
            others_data = []
            results = []
            for item in json_data:
                if 'city' in item and 'sell_price_min' in item and 'quality' in item:
                    city = item['city']
                    price = item['sell_price_min']
                    quality = item['quality']
                    if int(price) != 0:
                        if city == 'Black Market':
                            bm_data.append((price,quality, city))
                        if city != 'Black Market':
                            others_data.append((price, quality, city))
            for i in bm_data:
                for k in others_data:
                    if i[1] == k[1] and i[0] - k[0] > 0:
                        bm_price = i[0]
                        #bm_quality = i[1]
                        others_price = k[0]
                        others_city = k[2]
                        profit = bm_price - others_price
                        #qualities = k[3]
                        results.append((bm_price,others_price,others_city,profit))
            if results:
                return results
            else:
                return None