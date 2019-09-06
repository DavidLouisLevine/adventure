class Items(dict):
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.Find(item)

    def __iter__(self):
        return self.items.__iter__()

    def Find(self, item, location=None):
        for i in self.items:
            if i.name == item or i.abbreviation[:3] == item[:3]:
                if location is None or i.placement.location == location:
                    return i
        return None

    def Add(self, items):
        self.items += items

class Item:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation