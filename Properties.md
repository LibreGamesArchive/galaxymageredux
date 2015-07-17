In some programming languages, being able to access and modify class variables directly can be a problem.  The reason for this is that if you later need to do some form of computation on the variable before accessing or modifying it, you must change the API and that breaks developer code.

The solution to this is to create getter and setters for all public class variables (ie. get\_variable\_a, set\_variable\_a).  You must do this from the beginning even if you do nothing more than get or set the variable, just so that possible future changes will not break the API.  In Python, calling a function has significant overhead so the developers have creative a more elegant solution, properties.  Be aware that this only works with new-style classes.

```
property(fget=None, fset=None, fdel=None, doc=None)
```

A contrived example:

```
class A(object):
    def __init__(self):
        self.x = 1
```

The pythonic way of accessing and modifying the x variable would be:

```
>>> a = A()
>>> a.x
-  1
>>> a.x = 5
>>> a.x
-  5
```

Now, if you wanted to check to make sure someone can not set x to a negative number you could change the definition of A:

```
class A(object):
    def __init__(self):
        self.x = 1
    def _getx(self):
        return self._x
    def _setx(self, n):
        if n < 0:
            raise Exception("A.x can not be negative!")
        else:
            self._x = n
    x = property(_getx, _setx)
```

And using it:

```
>>> a = A()
>>> a.x
-  1
>>> a.x = 3
>>> a.x
-  3
>>> a.x = -3
-  Exception: A.x can not be negative!
```

What we have done here is to create methods for getting and setting x.  We preface them with an underscore so as not to pollute the namespace of the class.  We also use the variable name with an underscore inside the getx and setx methods.  Finally, we set the x variable to a property with fget=`_`getx and fset=`_`setx.

The result is that when you access x, the class will internally call self.`_`getx.  Also, when you modify x, the class will internally call self.`_`setx.  We have accomplished our goal without having to change the api, without muddying up the code with getters and setters for every class variable, and without the function overhead for variables that do not need it.
