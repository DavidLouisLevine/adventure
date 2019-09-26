# A lists of Item_s indexed by item number, item name, or item abbreviation
class Items():
    def __init__(self, items):
        self.items = dict()
        self.index = ()
        for item in items:
            self.items[item.name] = item
#            self.items[Items.Abbreviate(item.abbreviation)] = item
        self.UpdateIndex()

    # self.index is needed because item abbreviations may not be unique (e.g. objects in the C.I.A. Adventure Game)
    # iteration uses self.index
    def UpdateIndex(self):
        i = 0
        self.index = ()
        for item in self.items.values():
            self.index += (item, )
            item.i = i
            i += 1

    def __len__(self):
        return len(self.index)

    def __getitem__(self, item):
        return self.Find(item)

    def __iter__(self):
        for item in self.index:
            yield item

    def __contains__(self, item):
        if len(self.items) == 0:
            return False

        if type(item) is int:
            return item < len(self.index)
        for i in self:
            if type(item) is str:
                if i.name == item or i.abbreviation == item:
                    return True
            if item == i:
                return True

        return False

    @staticmethod
    def Abbreviate(name):
        return name[:3]

    def Find(self, item, location=None):
        foundItem = None
        if type(item) == str:
            if item in self.items:
                foundItem = self.items[item]
            else:
                abbreviation = Items.Abbreviate(item)
                for ii in self.index:
                    if ii.abbreviation == item:
                        foundItem = ii
                        break
        elif type(item) == int:
            foundItem = self.index[item]

        return foundItem

    def GetAbbreviations(self):
        return list(map(lambda x: x.abbreviation, self.index))

    def GetNames(self):
        return list(map(lambda x: x.name, self.index))
        # for item in self.index:
        #     yield item.name

    def Remove(self, name):
        self.items.pop(name)
        self.UpdateIndex()
        # for item in self.items.values():
        #     if name == item.name:
        #         self.items.pop(name)
        #         self.UpdateIndex()
        #         return
        #assert False, "Missing key " + name

# One Item in a list of Items
class Item:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    def Is(self, strItem):
        return self.name == strItem or self.abbreviation == Items.Abbreviate(strItem)
