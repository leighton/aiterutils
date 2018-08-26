from .aiterutils import apply

class Stream:

    def __init__(self, aiter, transforms=None):
        self._aiter = aiter
        self._transforms = [] if transforms is None else transforms

    def __getattr__(self, name):
        def fn(*args, **kwargs):
            return self.map(lambda x: getattr(x, name)(*args, **kwargs))
        return fn

    def __aiter__(self):
        return self

    async def __anext__(self):
        obj = await self._aiter.__anext__()
        for fn in self._transforms:
            obj = await apply(fn, obj)
        return obj

    def map(self, fn):
        return Stream(self._aiter,
                      transforms=self._transforms + [fn])

    async def each(self, fn):
        async for obj in self:
            await apply(fn, obj)

    def astype(self, typ):
        return self.map(typ)

    def __add__(self, other):
        return self.map(lambda x: x + other)

    def __sub__(self, other):
        return self.map(lambda x: x + other)

    def __mul__(self, other):
        return self.map(lambda x: x + other)

    def __getitem__(self, key):
        return self.map(lambda x: x[key])

    def __mod__(self, other):
        return self.map(lambda x: x % other)

    def __rmod__(self, other):
        return self.map(lambda x: other % x)

    # def __str__(self):
    #     return self.map(lambda x: str(x))
