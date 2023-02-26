class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __getitem__(self, index):
        print(f'Calling __getitem__ with index {index}')
        if index > len(self):
            raise StopIteration()
        else:
            return self._cities[index]

    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)

    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        #def __iter__(self):
            #print('Calling CitiyIterator instance __iter__')
            #return self

        def __getitem__(self, index):
            print(f'Calling __getitem__ with index: {index}')
            return index

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                print(f'StopIteration Exception raised')
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item


cities = Cities()
#print(list(enumerate(cities)))
for j in cities:
    print(f'cities index {j}')

