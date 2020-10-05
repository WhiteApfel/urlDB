# urlDB
Tool for nice work with storing data in URL

### Install
pip:k
```
python -m pip install --update urlDB
```

Source code:
```
git clone https://github.com/WhiteApfel/urlDB
cd urlDB
python setup.py install
```

Usage
-----

You can work with this class as with a dictionary.
The data will be automatically added to the link and available through the UrlDB.url attribute.
**Attention! Compression does not support** ``int`` **as a key**

```python
from urldb import UrlDB

# Uncompressed standard link
udb = UrlDB()

udb[2] = "two"
udb.url
# https://urldb.pfel.cc/data?2=%22two%22#n

udb["like"] = [248733366, "id212332030"]
udb.url
# https://urldb.pfel.cc/data?2=%22two%22&%22like%22=
# %5B248733366%2C%22id212332030%22%5D#n

# Custom link with data compression
udb = UrlDB(base="https://example.com", compress=True)
for i in range(10):
    udb[i] = str(i**2)*i
udb.url
# https://example.com?x%9C%5D%8CI%0E%800%0C%03%FF%E23%07%D2%A6%A1%E1k%88%BFw
# %2A%84X4%07%DB%13%29%87V%ED%D2%22%23%8C%2C%A4%3B%A5R2%93%E6%F3%14%17%CC%C6
# %2C%ED%06%11%88%1A%0F%A8m~%C97%C8%8E%0C%FF%82Nt%B7%3F%3A%07%B8%FD%1D%7B#c

# getting data from link
udb = UrlDB(setdb="https://example.com?x%9C%ABV2R%B22%AE%05%00%07C%01%DC#c")
udb.data
# {'2': 3}

udb = UrlDB(setdb="https://urldb.pfel.cc/data?2=%22two%22#n")
udb.data
# {2: 'two'}
```