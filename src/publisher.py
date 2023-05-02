class Publisher:
    """allows objects to keep track of changes to other objects
    """
    def __init__(self):
        self._subscribers = []

    def notify(self, exclude = None):
        for subscribed in self._subscribers:
            if exclude != subscribed:
                subscribed.update(self)

    def attach(self, subscribed):
        if subscribed not in self._subscribers:
            self._subscribers.append(subscribed)

    def detach(self, subscribed):
        if subscribed in self._subscribers:
            self._subscribers.remove(subscribed)
