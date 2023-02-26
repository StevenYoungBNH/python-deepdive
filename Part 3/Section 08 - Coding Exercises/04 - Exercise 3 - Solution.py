#!/usr/bin/env python
# coding: utf-8

# ### Exercise 3 - Solution

# Here we want to use Marshmallow to do the serialization and deserialization that we did in Exercises 1 and 2.

# In[1]:


class Stock:
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        
class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume


# In[2]:


from datetime import date, datetime
from decimal import Decimal

activity = {
    "quotes": [
        Stock('TSLA', date(2018, 11, 22), 
              Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
        Stock('AAPL', date(2018, 11, 22), 
              Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
        Stock('MSFT', date(2018, 11, 22), 
              Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
    ],
    
    "trades": [
        Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
        Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
    ]
}


# I'm first going to define some schemas for trades and stocks:

# In[3]:


from marshmallow import Schema, fields


# In[4]:


class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal()
    high = fields.Decimal()
    low = fields.Decimal()
    close = fields.Decimal()
    volume = fields.Integer()


# Let's test this one out quickly:

# In[5]:


StockSchema().dump(Stock('TSLA', date(2018, 11, 22), 
                          Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), 
                          Decimal('338.19'), 365_607))


# That's great, but there's a slight issue - you'll notice that the marshalled data has `Decimal` objects for our prices. This is still going to be an issue if we try to serialize to JSON:

# In[6]:


StockSchema().dumps(Stock('TSLA', date(2018, 11, 22), 
                          Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), 
                          Decimal('338.19'), 365_607))


# So let's fix that:

# In[7]:


class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Integer()


# In[8]:


StockSchema().dump(Stock('TSLA', date(2018, 11, 22), 
                          Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), 
                          Decimal('338.19'), 365_607)).data


# And now we can serialize to JSON:

# In[9]:


StockSchema().dumps(Stock('TSLA', date(2018, 11, 22), 
                          Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), 
                          Decimal('338.19'), 365_607)).data


# Let's now handle the `Trade` schema:

# In[10]:


class TradeSchema(Schema):
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal(as_string=True)
    commission = fields.Decimal(as_string=True)
    volume = fields.Integer()


# In[11]:


TradeSchema().dumps(Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99'))).data


# Now let's write a schema for our overall dictionary that contains a list of Trades and a list of Quotes:

# In[12]:


class ActivitySchema(Schema):
    trades = fields.Nested(TradeSchema, many=True)
    quotes = fields.Nested(StockSchema, many=True)


# And we can now serialize and deserialize:

# In[13]:


result = ActivitySchema().dumps(activity, indent=2).data


# In[14]:


type(result)


# In[15]:


print(result)


# So a JSON string...
# Let's deserialize that JSON string:

# In[16]:


activity_deser = ActivitySchema().loads(result).data


# In[17]:


type(activity_deser)


# In[18]:


from pprint import pprint

pprint(activity_deser)


# That's looking pretty good, but you'll notice something - the objects in the `trades` and `quotes` list have been loaded into plain dictionary objects, not `Trade` and `Stock` objects:

# In[19]:


type(activity_deser['trades'][0])


# For this we have to remember to provide functions decorated with `@post_load`:

# In[20]:


from marshmallow import post_load

class TradeSchema(Schema):
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal(as_string=True)
    commission = fields.Decimal(as_string=True)
    volume = fields.Integer()
    
    @post_load
    def make_trade(self, data):
        return Trade(**data)


# In[21]:


class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Integer()
    
    @post_load()
    def make_stock(self, data):
        return Stock(**data)


# And of course we have to redefine our `ActivitySchema` to make sure it is referencing the newly defined sub schema classes:

# In[22]:


class ActivitySchema(Schema):
    trades = fields.Nested(TradeSchema, many=True)
    quotes = fields.Nested(StockSchema, many=True)


# And now we can try this again:

# In[23]:


activity_deser = ActivitySchema().loads(result).data


# So here we have an issue - basically our method to construct a new `Stock` object expects the argument for the open price to be `open_`, and not `open` which is what our schema is producing.
# 
# We could do it in one of two ways:
# 
# First we can change our method that builds the `Stock` object:

# In[24]:


class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Integer()
    
    @post_load()
    def make_stock(self, data):
        data['open_'] = data.pop('open')
        return Stock(**data)


# In[25]:


class ActivitySchema(Schema):
    trades = fields.Nested(TradeSchema, many=True)
    quotes = fields.Nested(StockSchema, many=True)


# In[26]:


activity_deser = ActivitySchema().loads(result).data


# In[27]:


pprint(activity_deser)


# So, let's just recap the various schemas we have to create:

# In[28]:


class StockSchema(Schema):
    symbol = fields.Str()
    date = fields.Date()
    open = fields.Decimal(as_string=True)
    high = fields.Decimal(as_string=True)
    low = fields.Decimal(as_string=True)
    close = fields.Decimal(as_string=True)
    volume = fields.Integer()
    
    @post_load()
    def make_stock(self, data):
        data['open_'] = data.pop('open')
        return Stock(**data)
    
class TradeSchema(Schema):
    symbol = fields.Str()
    timestamp = fields.DateTime()
    order = fields.Str()
    price = fields.Decimal(as_string=True)
    commission = fields.Decimal(as_string=True)
    volume = fields.Integer()
    
    @post_load
    def make_trade(self, data):
        return Trade(**data)
    
class ActivitySchema(Schema):
    trades = fields.Nested(TradeSchema, many=True)
    quotes = fields.Nested(StockSchema, many=True)


# As you can see this is a whole lot easier than doing it by hand using the standard library.
