# `aiterutils`

A functional programming toolkit for manipulation of asynchronous iterators in python >3.5

It has two types of operations:

1. Iterator functions
   * `au.map(fn, aiter): aiter`
   * `au.each(fn, aiter): coroutine`
   * `au.filter(fn, aiter): aiter`
   * `au.merge([aiter...]): aiter`
   * `au.bifurcate(fn, aiter): (aiter, aiter)`
   * `au.branch([fn...], aiter): (aiter...)`

2. Dynamic streams
   * `au.Stream(aiter)`

Dynamics streams can have their underlying object methods invocated implicitly

```
capitals = au.Stream(['a','b','c']).upper()
```

## API

### `au.map(fn, aiter): aiter`

```python
stream = au.map(lambda s: s + '!', team())
app    = au.println(stream, end='')

loop.run_until_complete(app)
```
🙂!☀️!🤡!🤡!🤡!☀️!🤡!🤡!🙂!☀️!☀️!🙂!☀️!🙂!🙂!

### `au.each(fn, aiter): coroutine`

```python
app = au.each(single_line_print, team())
loop.run_until_complete(app)
```
🙂☀️🤡🤡🤡☀️🤡🤡🙂☀️☀️🙂☀️🙂🙂

### `au.filter(fn, aiter): aiter`

```python
stream = au.filter(lambda s: s == '☀️', team())
app    = au.println(stream, end="")
loop.run_until_complete(app)
```
☀️☀️☀️☀️☀️

### `au.merge([aiter...]): aiter`

```python
stream = au.merge([smiley(), sunny()])
app    = au.println(stream, end="")
loop.run_until_complete(app)
```
🙂☀️☀️🙂☀️☀️🙂☀️🙂🙂

### `au.bifurcate(fn, aiter): (aiter, aiter)`

```python
smile_stream, other_stream = au.bifurcate(lambda s: s == '🙂', team())

loop.run_until_complete(au.println(smile_stream, end=""))
loop.run_until_complete(au.println(other_stream, end=""))
```
🙂🙂🙂🙂🙂☀️🤡🤡🤡☀️🤡🤡☀️☀️☀️

### `au.branch([fn...], aiter): (aiter...)`

```python
filters = [
    lambda s: s == '🙂',
    lambda s: s == '☀️',
    lambda s: s == '🤡'
]

smile_stream, sun_stream, clown_stream = au.branch(filters, team())

loop.run_until_complete(au.println(smile_stream, end=''))
loop.run_until_complete(au.println(sun_stream, end=''))
loop.run_until_complete(au.println(clown_stream, end=''))
```
🙂🙂🙂🙂🙂☀️☀️☀️☀️☀️🤡🤡🤡🤡🤡

### `au.Stream(aiter)`

> NB: The jury is still out as to whether these promote hygienic consistent code

**map and each member methods**
```python
app = (au.Stream(team())
         .map(lambda s: s+'!')
         .each(single_line_print))

loop.run_until_complete(app)
```
🙂!☀️!🤡!🤡!🤡!☀️!🤡!🤡!🙂!☀️!☀️!🙂!☀️!🙂!🙂!

**operator overloading**
> dynamics streams can have underlying object methods called implicitly

```python
stream = au.Stream(symbol_stream([{"key-2" : 1, "key-2" : 2}]*10, 0.5))
value2 = stream['key-2'] + 3 / 5

app = au.println(value2, end='')
loop.run_until_complete(app)
```
2.62.62.62.62.62.62.62.62.62.6

**dynamic method invocation**
```python
stream = au.Stream(symbol_stream([{"key-1" : 1, "key-2" : 2}]*5, 0.5))

keys = stream.keys()
key = keys.map(lambda key: list(key))
key = key[-1]
key = key.upper().encode('utf-8')

app = au.println(key, end='')

loop.run_until_complete(app)
```
b'KEY-2'b'KEY-2'b'KEY-2'b'KEY-2'b'KEY-2'
