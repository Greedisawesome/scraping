import requests
import json
import csv
from pandas import DataFrame

auction_url = 'https://bidspirit-portal.global.ssl.fastly.net//services/portal/getAuctionItems?cacheVersion=2019-06-20_20-14-09&cdnSubDomain=ru&intKey={auction_code}'
for i in range (161, 9999):
    r = requests.get (auction_url.format(auction_code=i))
    parsed_json = r.json()
    if parsed_json:
        auction_id = parsed_json[0]['auctionId']
        print(auction_id)
        prices = requests.get('https://ru.bidspirit.com/services/account/getAccountActionsForAuction?auctionId=' + str(auction_id))
        parsed_prices = prices.json()
        with open ('input_%s.json' % i, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent = 2, ensure_ascii=False)
        with open ('prices_%s.json' % i, 'w', encoding='utf-8') as f_1:
            json.dump(parsed_prices, f_1, indent = 2, ensure_ascii=False)
        for listing in parsed_json:
            try:
              listingID = listing['id']
            except:
              listingID = ''
            try:
              auctionCode = listing['ownerKey']
            except:
              auctionCode = ''
            try:
              item_index = listing['itemIndex']
            except:
              item_index = ''
            try:
              region = listing['region']
            except:
              region = ''
            try:
              name_ru = listing['name']['ru']
            except:
              name_ru = ''
            try:
              name_he = listing['name']['he']
            except:
              name_he = ''
            try:
              name_en = listing['name']['en']
            except:
              name_en = ''
            try:
              description_ru = listing['description']['ru']
            except:
              description_ru = ''
            try:
              description_he = listing['description']['he']
            except:
              description_he = ''
            try:
              description_en = listing['description']['en']
            except:
              description_en = ''
            try:
              artist_ru = listing['artist']['ru']
            except:
              artist_ru = ''
            try:
              artist_he = listing['artist']['he']
            except:
              artist_he = ''
            try:
              artist_en = listing['artist']['en']
            except:
              artist_en = ''
            try:
              details_ru = listing['details']['ru']
            except:
              details_ru = ''
            try:
              details_he = listing['details']['he']
            except:
              details_he = ''
            try:
              details_en = listing['details']['en']
            except:
              details_en = ''
            try:
              estimatedPrice = listing['estimatedPrice']
            except:
              estimatedPrice = ''
            try:
              startPrice = listing['startPrice']
            except:
              startPrice = ''
            try:
              valuePrice = listing['valuePrice']
            except:
              valuePrice = ''
            try:
              auctionDate = listing['auctionData']
            except:
              auctionData = ''
            try:
              houseCode = listing['houseCode']
            except:
              houseCode = ''
            data = {'listingID':listingID,
                    'auctionCode':auctionCode,
                    'item_index': item_index,
                    'region':region,
                    'name_ru':name_ru,
                    'name_he': name_he,
                    'name_en': name_en,
                    'description_ru':description_ru,
                    'description_he':description_he,
                    'description_en':description_en,
                    'artist_ru':artist_ru,
                    'artist_he':artist_he,
                    'artist_en':artist_en,
                    'details_ru': details_ru,
                    'details_he': details_he,
                    'details_en':details_en,
                    'estimatedPrice': estimatedPrice,
                    'startPrice': startPrice,
                    'valuePrice':valuePrice,
                    'auctionDate':auctionData,
                    'houseCode':houseCode}
            print(data)
            with open('fullproducts.csv', 'a', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerow( (data['listingID'], data['auctionCode'], data['item_index'], data['region'], data['name_ru'], data['name_he'], data['name_en'], data['description_ru'],
                                data['description_he'], data['description_en'], data['artist_ru'], data['artist_he'],data['artist_en'],data['details_ru'], data['details_he'], data['details_en'],
                                data['estimatedPrice'], data['startPrice'], data['valuePrice'], data['auctionDate'], data['houseCode']))
      #      for g in parsed_json:
      #          csvfile.writerow(g.keys())
      #          csvfile.writerow(g.values())
      #  df = DataFrame(parsed_json)
      #  dp = DataFrame(parsed_prices)
      #  print(df)
