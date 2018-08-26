# `aiterutils` tutorial

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
   * `au.Stream(aiter)'

Dynamics streams can have their undelying object methods invocated implicitly

```
capitals = au.Stream(['a','b','c']).upper()
