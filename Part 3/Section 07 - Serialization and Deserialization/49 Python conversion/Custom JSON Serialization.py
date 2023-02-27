# Custom JSON Serialization
from fractions import Fraction
from decimal import Decimal
from functools import singledispatch
from time import sleep
from datetime import datetime
import json
current = datetime.utcnow()
print(current.isoformat())

log_record = {'time': datetime.utcnow().isoformat(), 'message': 'testing'}
lr = json.dumps(log_record)
print(lr)


def format_iso(dt):
    return dt.isoformat()


sleep(0)
log_record = {'time': datetime.utcnow(), 'message': 'utcnow'}
print(json.dumps(log_record, default=format_iso))

log_record = {
    'time1': datetime.utcnow(),
    'time2': datetime.utcnow(),
    'message': 'Testing...'
}

print(json.dumps(log_record, default=format_iso))

log_record = {
    'time': datetime.utcnow(),
    'message': 'Testing...',
    'other': {'a', 'b', 'c'}
}


def custom_json_formatter(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)


print(json.dumps(log_record, default=custom_json_formatter))


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()

    def __str__(self):
        return(f'{self.name}, is {self.age} years old')

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'

    def toJSON(self):
        return {
            'name': self.name,
            'age': self.age,
            # 'create_dt': self.create_dt.isoformat() # since it was converted to a string here it prevented the custom_json_formatter from being called.
            'create_dt': self.create_dt  # uses the custom_json_formatter
        }


p = Person('John', 82)
print(p.__repr__())
print(p.toJSON())

# ln23


def custom_json_formatter(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)
    elif isinstance(arg, Person):
        return arg.toJSON()


# ln 24
log_record = dict(time=datetime.utcnow(),
                  message='Created new person record',
                  person=p)
# sleep(1)
print(json.dumps(log_record, default=custom_json_formatter))
print(json.dumps(log_record, default=custom_json_formatter, indent = 2))

# ln 27


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'

    def toJSON(self):
        return {
            'name': self.name,
            'age': self.age,
            'create_dt': self.create_dt  # the format_iso is removed allowing the custom_json_formatter to handle
        }


p = Person('Monty', 100)
log_record = dict(time=datetime.utcnow(),
                  message='Created new person record',
                  person=p)
print(json.dumps(log_record, default=custom_json_formatter, indent=2))

# ln 31


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'

    def toJSON(self):
        return vars(self)  # returning a dictionary of the attributes


p = Person('Python', 27)
print(p.toJSON())  # using vars

log_record['person'] = p
print(log_record)
print(json.dumps(log_record, default=custom_json_formatter, indent=2))

print('toJSON' in vars(Person))


def custom_json_formatter_3(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)
    else:
        try:
            return arg.toJSON()  # does the class have a 'toJSON' attribute?
        except AttributeError:
            try:
                return vars(arg)  # if not
            except TypeError:
                return str(arg)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'


pt1 = Point(10, 10)

print(vars(pt1))

log_record = dict(time=datetime.utcnow(),
                  message='Created new point',
                  point=pt1,
                  created_by=p)

print(log_record)

# ln 43
print(json.dumps(log_record, default=custom_json_formatter_3, indent=2))


@singledispatch
def json_format(arg):
    print(f'in json_format single dispatch - {arg}')
    try:
        print('\ttrying to use toJSON...')
        return arg.toJSON()
    except AttributeError:
        print('\tfailed - trying to use vars...')
        try:
            return vars(arg)
        except TypeError:
            print('\tfailed - using string representation...')
            return str(arg)


@json_format.register(datetime)
def _(arg):
    print("json_format register(datetime)")
    return arg.isoformat()


@json_format.register(set)
def _(arg):
    rint("json_format register(set)")
    return list(arg)


print(json.dumps(log_record, default=json_format, indent=2))


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'

    def toJSON(self):
        return dict(name=self.name)


p = Person('Python', 27)

log_record['created_by'] = p

print(json.dumps(log_record, default=json_format, indent=2))

# ln52
print(json.dumps(dict(a=1 + 1j,
                      b=Decimal('0.5'),
                      c=Fraction(1, 3),
                      p=Person('Python', 27),
                      pt=Point(0, 0),
                      time=datetime.utcnow()
                      ),
                 default=json_format, indent = 2))


@json_format.register(Decimal)
def _(arg):
    return f'Decimal({str(arg)})'


print(json.dumps(dict(a=1 + 1j, b=Decimal(0.5), c=Fraction(1, 3), p=Person('Python', 27), pt = Point(0, 0), time =
                      datetime.utcnow()), default=json_format))

print(json.dumps(dict(pt = Point(Person('Python', 27), 2 + 2j)),
                 default=json_format, indent=2))
