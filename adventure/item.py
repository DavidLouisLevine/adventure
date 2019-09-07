import copy

class Items():
    def __init__(self, items):
        self.items = dict()
        self.index = ()
        i = 0
        for item in items:
            self.items[Items.Abbreviate(item.abbreviation)] = item
            self.index += (item, )
            item.i = i
            i += 1

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.Find(item)

    def __iter__(self):
        #return self.items.__iter__()
        for item in self.index:
            yield item

    @staticmethod
    def Abbreviate(name):
        return name[:3]

    def Find(self, item, location=None):
        i = None
        if type(item) == str:
            abbreviation = Items.Abbreviate(item)
            if abbreviation in self.items:
                i = self.items[abbreviation]
            else:
                for ii in self.index:
                    if ii.name == item:
                        i = ii
                        break
        elif type(item) == int:
            i = self.index[item]

        if i is not None and (location is None or i.placement.location == location):
            return i

        return None

    def GetAbbreviations(self):
        return list(self.items.keys())

    def GetNames(self):
        for item in self.index:
            yield item.name

class Item:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation