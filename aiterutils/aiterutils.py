import asyncio
import json
import inspect
from functools import reduce

async def apply(fn, x):
    if asyncio.iscoroutinefunction(fn):
        return await fn(x)
    elif hasattr(fn, '__call__'):
        if asyncio.iscoroutinefunction(fn.__call__):
            return await fn(x)
        else:
            return fn(x)
    else:
        return fn(x)


async def sapply(fn, x):
    if asyncio.iscoroutinefunction(fn):
        return await fn(*x)
    elif hasattr(fn, '__call__'):
        if asyncio.iscoroutinefunction(fn.__call__):
            return await fn(*x)
        else:
            return fn(*x)
    else:
        return fn(*x)


async def println(stream, **kwargs):
    async for string in stream:
        print(string, **kwargs)


async def map(fn, aiter):
    async for x in aiter:
        yield await apply(fn, x)


async def starmap(fn, aiter):
    async for x in aiter:
        yield await sapply(fn, x)


async def each(fn, aiter):
    async for x in aiter:
        await apply(fn, x)


async def filter(fn, aiter):
    async for x in aiter:
        y = await apply(fn, x)

        if y == True:
            yield x


async def merge(aiters):

    q = asyncio.Queue()

    co = [ each(q.put, aiter) for aiter in aiters ]

    tasks = [ asyncio.ensure_future(c) for c in co ]

    while True:
        done = True
        for t in tasks:
            if not t.done():
                done = False
                break
        if done:
            return

        try:
            # this esures that if work is done after a stream yields
            # that we don't block forever rather than completing the coro.
            item = await asyncio.wait_for(q.get(), 1)
            yield item
        except asyncio.TimeoutError as e:
            pass


def branch(filters, aiter):

    queues = [ asyncio.Queue() for _ in range(len(filters)) ]

    POISON_PILL = object() #unique poison pill

    async def publish_thunk():
        async for x in aiter:
            for queue, fn in zip(queues, filters):
                if fn(x):
                    await queue.put(x)
        for queue in queues:
            await queue.put(POISON_PILL)

    task = asyncio.ensure_future(publish_thunk())

    async def aiter_queue(queue):
        while True:
            x = await queue.get()
            if x is POISON_PILL:
                break
            else:
                yield x

    return [ aiter_queue(queue) for queue in queues ]


def bifurcate(fn, aiter):
    return branch([ fn, lambda x: not fn(x) ], aiter)
