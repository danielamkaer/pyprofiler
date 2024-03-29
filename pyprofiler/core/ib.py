import pyprofiler.core
import pickle


def convert(obj, parent):
    if type(obj) == list:
        i = IBList(obj, parent=parent, base=parent.base)
        return i
    elif type(obj) == dict:
        i = IBDict(obj, parent=parent, base=parent.base)
        return i
    else:
        return obj

UPDATE_SET = 'UPDATE_SET'
UPDATE_APPEND = 'UPDATE_APPEND'
UPDATE_INSERT = 'UPDATE_INSERT'
UPDATE_REMOVE = 'UPDATE_REMOVE'
UPDATE_CLEAR = 'UPDATE_CLEAR'

class IBList(list):
    def __init__(self, items, parent=None, base=None):
        self.parent = parent
        self.base = base
        super().__init__([convert(item, self) for item in items])

    def append(self, item):
        super().append(convert(item, self))
        self.base.updated(self, self.index(item), item, UPDATE_APPEND)

    def clear(self):
        super().clear()
        self.base.updated(self, None, None, UPDATE_CLEAR)

    def copy(self):
        return super().copy()

    def extend(self, itr):
        for item in itr:
            self.append(item)

    def insert(self, index, item):
        super().insert(index, convert(item, self))
        self.base.updated(self, self.index(item), item, UPDATE_INSERT)

    def pop(self, index=None):
        it = super().pop(index)
        self.base.updated(self, index, None, UPDATE_REMOVE)
        return it

    def remove(self, item):
        super().item(index)
        self.base.updated(self, index, None, UPDATE_REMOVE)
    
    def first(self, **search):
        for item in self:
            for key in search:
                if key not in item or item[key] != search[key]:
                    break
            # nb. for/else
            else:
                return item

        return None

    def firstOrCreate(self, **search):
        item = self.first(**search)
        if item:
            return item
        else:
            item = convert(search, self)
            self.append(item)
            return item

    def serialize(self):
        return [x.serialize() if isinstance(x, (IBDict, IBList)) else x for x in self]

class IBDict(dict):
    def __init__(self, items, parent=None, base=None):
        self.parent = parent
        self.base = base
        super().__init__({k: convert(items[k], self) for k in items})

    def __setitem__(self, key, val):
        val = convert(val, self)
        if val in self.values() and self[key] != val:
            print(f"{val} already in {self}")
        self.base.updated(self, key, val, UPDATE_SET)
        super().__setitem__(key, val)

    def __repr__(self):
        return f'IBDict{super().__repr__()}'

    def _lookup(self, val):
        idx = list(self.values()).index(val)
        return list(self.keys())[idx]

    def incr(self, key, val=1):
        if key in self:
            self[key] = self[key] + val
        else:
            self[key] = val
    
    def serialize(self):
        return {k:(self[k].serialize() if isinstance(self[k], (IBDict, IBList)) else self[k]) for k in self}

class InformationBase:

    def __init__(self):
        self.base = self
        self.root = convert({}, self)
        self.onInformationChanged = pyprofiler.core.Event()

    def resolve(self, item):
        chain = []
        while not isinstance(item, InformationBase):
            p = item.parent
            if isinstance(p, InformationBase):
                break
            elif isinstance(p, IBDict):
                k = p._lookup(item)
                chain.append(k)
            elif isinstance(p, IBList):
                k = p.index(item)
                chain.append(k)
            else:
                return []
            item = item.parent

        return list(reversed(chain))


    def updated(self, obj, key, item, update):
        res = self.resolve(obj)
        if update == UPDATE_SET:
            pathlist = res + [key]
            path = '.'.join(list(map(str, pathlist)))
        elif update == UPDATE_APPEND:
            pathlist = res
            path = '.'.join(list(map(str, pathlist)))
        
        self.container.run_coroutine(self.onInformationChanged({'update':update, 'path':path, 'item': item}))

    @staticmethod
    def register(app):
        app.singleton(InformationBase, InformationBase)

    def boot(self):
        print("IB booted")
        try:
            with open('ib.bin', 'rb') as file:
                print("loading")
                loaded = pickle.load(file)
                self.root = convert(loaded, self)
                print("done loading")
        except IOError:
            pass
        except EOFError:
            pass

    def shutdown(self):
        try:
            with open('ib.bin', 'wb') as file:
                pickle.dump(self.root.serialize(), file)
        except AttributeError as e:
            print(e)
