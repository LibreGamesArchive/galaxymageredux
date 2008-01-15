# Observer design pattern implementation copied from http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html#observer

class Delegate:
    '''Handles a list of methods and functions
    Usage:
        d = Delegate()
        d += function    # Add function to end of delegate list
        d(*args, **kw)   # Call all functions, returns a list of results
        d -= function    # Removes last matching function from list
        d -= object      # Removes all methods of object from list
    '''
    def __init__(self):
        self.__delegates = []

    def add_callback(self, callback):
        self.__delegates.append(callback)
        return self

    def remove_callback(self, callback):
        # If callback is a class instance,
        # remove all callbacks for that instance
        self.__delegates = [ cb
            for cb in self.__delegates
                if getattr(cb, 'im_self', None) != callback]

        # If callback is callable, remove the last
        # matching callback
        if callable(callback):
            for i in range(len(self.__delegates)-1, -1, -1):
                if self.__delegates[i] == callback:
                    del self.__delegates[i]
                    return self
        return self

    def __call__(self, *args, **kw):
        return [ callback(*args, **kw)
            for callback in self.__delegates]



class Event(property):
    '''Class event notifier
    Usage:
        class C:
            TheEvent = Event()
            def OnTheEvent(self):
                self.TheEvent(self, context)

        instance = C()
        instance.TheEvent += callback
        instance.OnTheEvent()
        instance.TheEvent -= callback
    '''
    def __init__(self):
        self.attrName = attrName = "__Event_" + str(id(self))
        def getEvent(subject):
            if not hasattr(subject, attrName): 
                setattr(subject, attrName, Delegate())
            return getattr(subject, attrName)
        super(Event, self).__init__(getEvent)

    def call(self, subject, *args, **kw):
        if hasattr(subject, self.attrName):
            getattr(subject, self.attrName)(subject, *args, **kw)

