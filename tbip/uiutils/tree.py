"""tree.py- class for keeping directory trees."""


import os
import json
import shutil


class Tree:
    """class for maintaining directories.
    when iterated, will yield either a file object, or another
    tree object if it is a directory.
    uses a zipfile internally.
    """

    def __init__(self, dirname, defmode='r'):
        """set dirname to the directory name that you want."""
        self.name = dirname
        self.defmode = defmode

        self.items = []

        for i in os.listdir(dirname):
            if os.path.isdir(os.path.join(dirname, i)):
                self.items.append(Tree(os.path.join(dirname, i), defmode))

            else:
                self.items.append(open(os.path.join(dirname, i), defmode))

        self._dict = self.to_dict()

    def __iter__(self):
        """yield each filename"""
        for i in self.items:
            yield i

    def __getitem__(self, fname):
        """returns self.items[index]"""
        return self._dict[fname]

    def __setitem__(self, fname, obj):
        """adds an item to the directory. if it is there already,
        replace it. if it is another Tree object, recursively add
        it as well.
        """
        if isinstance(obj, Tree):
            for i in obj:
                obj[i.name] = obj[i]

        else:
            with open(os.path.join(self.name, fname), 'wb') as openfile:
                raw = obj.read()
                openfile.write(raw.encode() if isinstance(raw, str) else raw)

        self._refresh()

    def _refresh(self):
        """refresh directory structure"""
        for i in os.listdir(self.name):
            if os.path.isdir(os.path.join(self.name, i)):
                self.items.append(
                    Tree(os.path.join(self.name, i), self.defmode))

            else:
                self.items.append(
                    open(os.path.join(self.name, i), self.defmode))

    def to_dict(self, content=0):
        """convert the directory structure to a dict.
        if content is 0, put the actual object.
        if it is 1, display only the name if it is a file.
        if it is 2, display the contents of the file.
        """

        func = {
            0: lambda x: x,
            1: lambda x: x.read(),
            2: lambda x: x.name,
        }[content]

        dictionary = {}
        for i in self:
            if isinstance(i, Tree):
                dictionary[os.path.split(i.name)[-1]] = i.to_dict(content)
            else:
                item = func(i)
                dictionary[os.path.split(i.name)[-1]] = item

        return dictionary

    def to_json(self, pretty=False, content=0, skipkeys=True):
        """convert the dict to json object.
        if pretty is false, then it will be minified.
        if content must be either 0 or 1, if 0, than display the
        file contents, if 1, then the name
        if skipkeys is False, then it will raise an exception on invalid
        items.
        """

        opts = {'separators': (',', ':')} if not pretty else {'indent': 4}
        string = json.dumps(self.to_dict(content + 1),
                            skipkeys=skipkeys, **opts)
        return string

    def make_zip(self):
        """creates a zip file of the directory."""
        shutil.make_archive(self.name, 'zip', self.name)

    def read(self, fname):
        """reads fname"""
        return self._dict[fname]


def _test():
    """test Tree class"""
    import pprint
    import io
    test = Tree('../test-dir')
    pprint.pprint(test.to_dict())
    print(test['howdy.txt'])
    test['howdy.txt'] = io.StringIO('bah humbug.')
    print(test['howdy.txt'].read())
    test['dir.json'] = io.StringIO(test.to_json(pretty=1, content=1))
    test.make_zip()


if __name__ == '__main__':
    _test()
