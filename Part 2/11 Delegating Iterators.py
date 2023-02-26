# Delegating Iterators

from collections import namedtuple

Person = namedtuple('Person', 'first last')


class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize() +
                             ' ' + person.last.capitalize()
                             for person in persons]
        except (TypeError, AttributeError):
            self._persons = []


persons_list = [Person('michaeL', 'paLin'), Person('eric', 'idLe'), Person('john', 'cLeese')]

person_names = PersonNames(persons_list)

print(person_names._persons)

#  Adding iter


class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize()
                             + ' ' + person.last.capitalize()
                             for person in persons]
        except TypeError:
            self._persons = []

    def __iter__(self):
        print("__iter__ called")
        return iter(self._persons)


person_names = PersonNames(persons_list)

for p in person_names:
    print(p)

sl = sorted(person_names)
print(f"Sorted Names:\n{sl}")

