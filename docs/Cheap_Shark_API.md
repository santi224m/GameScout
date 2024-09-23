#Cheap_Shark_API.md

## API URLS

** List of Deals ** : https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15
** Deal Lookup ** : https://www.cheapshark.com/api/1.0/deals?id=X8sebHhbc1Ga0dTkgg59WgyM506af9oNZZJLU9uSrX8%3D


** List of Games ** : https://www.cheapshark.com/api/1.0/games?title=batman
** Game Lookup ** : https://www.cheapshark.com/api/1.0/games?id=612
** Multiple Game Lookup ** : https://www.cheapshark.com/api/1.0/games?ids=128,129,130

** Stores Info ** : https://www.cheapshark.com/api/1.0/stores
** Stores Last Change ** : https://www.cheapshark.com/api/1.0/stores?lastChange=


** Edit Alert ** : https://www.cheapshark.com/api/1.0/alerts?action=set&email=someone@example.org&gameID=59&price=14.99
** Manage Alert ** : https://www.cheapshark.com/api/1.0/alerts?action=manage&email=address-with-alerts@example.org
** Get Alerts** :https://www.cheapshark.com/api/1.0/alerts?action=get&key=example-key-value


## Parameters Used
**List of Deals **
* storeID 
* pageNumber
* pageSize
* sortBy
* desc
* lowerPrice
* upperPrice
* metacritic - min metacritic rating for a game
* steamRating - min steam reviews rating for a game
* maxAge
* steamAppID
* title
* exact 
* AAA - flag deals that are > $29
* steamworks - flag deals only on steam
* onSale - flag games that are on sale
* output - output deals in RSS format

**Deal Lookup**
* id -> Encoded Deal ID


**List of Games**
* title
* steamAppID
* limit
* exact

**Game Lookup**
* id

**Multiple Game Lookup**
*ids - comma separated list of GameID's
*format - array

**Stores info**
curl --location 'https://www.cheapshark.com/api/1.0/stores'

**Stores Last Change**
* lastChange -> curl --location 'https://www.cheapshark.com/api/1.0/stores?lastChange='


## Example for Deal Lookup

```python
curl --location 'https://www.cheapshark.com/api/1.0/deals?id=X8sebHhbc1Ga0dTkgg59WgyM506af9oNZZJLU9uSrX8%253D'
```

```json
{
  "gameInfo": {
    "storeID": "1",
    "gameID": "93503",
    "name": "BioShock Infinite",
    "steamAppID": "8870",
    "salePrice": "29.99",
    "retailPrice": "29.99",
    "steamRatingText": "Very Positive",
    "steamRatingPercent": "93",
    "steamRatingCount": "98477",
    "metacriticScore": "94",
    "metacriticLink": "/game/pc/bioshock-infinite",
    "releaseDate": 1364169600,
    "publisher": "N/A",
    "steamworks": "1",
    "thumb": "https://cdn.cloudflare.steamstatic.com/steam/apps/8870/capsule_sm_120.jpg?t=1602794480"
  },
  "cheaperStores": [
    {
      "dealID": "vb3EqB4KpKbSyV83DXQYAZCSBS60LaOMgLCXSt8pQxw%3D",
      "storeID": "23",
      "salePrice": "5.89",
      "retailPrice": "29.99"
    },
    {
      "dealID": "boC2N0Q7SMCKxv6UKjRw%2BLFY6%2BNLEeWM2Bf1i80clx0%3D",
      "storeID": "21",
      "salePrice": "5.99",
      "retailPrice": "29.99"
    },
    {
      "dealID": "tbqfs8HsmHWn0mMk2QRCPd7KWLidkHrIYZX3FbYCyk0%3D",
      "storeID": "30",
      "salePrice": "7.19",
      "retailPrice": "29.99"
    },
    {
      "dealID": "r%2FGHYdW6GKpZfaqR4DQrjKD7vBoWiFPP7npVpVw4350%3D",
      "storeID": "34",
      "salePrice": "7.20",
      "retailPrice": "29.99"
    },
    {
      "dealID": "OVrkWmI7sl5RN61pxpA44euybrH826w%2FjvlV%2BYKc2oA%3D",
      "storeID": "2",
      "salePrice": "7.49",
      "retailPrice": "29.99"
    },
    {
      "dealID": "5ptxhcM1fatjVrZSnNNpbSz6okheevZEhcBAZm4AUfU%3D",
      "storeID": "35",
      "salePrice": "7.50",
      "retailPrice": "29.99"
    },
    {
      "dealID": "DQ%2BYLI9do4mm0H2%2BDUd6npgoQoK8bseNvyjJe%2B%2F3dEo%3D",
      "storeID": "15",
      "salePrice": "26.28",
      "retailPrice": "29.99"
    },
    {
      "dealID": "kj2H%2FvwfkyU40jW9s2g88CAW4PuR0etKlYvkQLitgvQ%3D",
      "storeID": "29",
      "salePrice": "26.99",
      "retailPrice": "29.99"
    },
    {
      "dealID": "fq0cNHiR3Z4TpZyV7WH865C1%2BCBlmufYUc%2Bu2HqyUHE%3D",
      "storeID": "27",
      "salePrice": "26.99",
      "retailPrice": "29.99"
    }
  ],
  "cheapestPrice": {
    "price": "4.49",
    "date": 1682548425
  }
}
```

