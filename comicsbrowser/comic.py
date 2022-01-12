from zipfile import ZipFile
from functools import cached_property


class Comic(ZipFile):
    def __init__(self, *args, **kwargs):
        super(Comic, self).__init__(*args, **kwargs)
        self.pagelist = [name for name in self.namelist() if name.endswith('.jpg')]
        self.pagememory = {}

    def page(self, n):
        """Returns page according to its number

        Parameters
        ----------
        n: int

        Returns
        -------

        """
        # clip values
        if n < 0:
            n = 0
        elif n > len(self.pagelist) - 1:
            n = -1

        if n not in self.pagememory.keys():
            self.pagememory[n] = self.read(self.pagelist[n])

        return self.pagememory[n]

    def pages(self, first, end):
        return [self.page(n) for n in range(first, end + 1)]
