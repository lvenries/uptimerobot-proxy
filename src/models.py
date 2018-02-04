"""
    Wraps data sent from uptimerobot into python objects. Following vars can be passed:
      - monitorID: the ID of the monitor
      - monitorURL: the URL of the monitor
      - monitorFriendlyName: the friendly name of the monitor
      - alertType: 1: down, 2: up, 3: SSL expiry notification
      - alertTypeFriendlyName: Down or Up
      - alertDetails: any info regarding the alert -if exists-
      - alertDuration: in seconds and only for up events
      - monitorAlertContacts: the alert contacts associated with the alert in the format of
            457;2;john@doe.com - alertContactID;alertContactType, alertContactValue
      - sslExpiryDate: only for SSL expiry notifications
      - sslExpiryDaysLeft: only for SSL expiry notifications
"""
from datetime import datetime
from collections import deque
from itertools import islice


class Event:

    def __init__(self, monitor_name, alert_type, alert_name, alert_details, alert_duration, timestamp=None):
        self.monitor_name = monitor_name
        self.alert_type = alert_type
        self.alert_name = alert_name
        self.alert_details = alert_details
        self.alert_duration = alert_duration
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return "<{0.__class__.__name__} ({0.alert_type}) for " \
            "{0.monitor_name}: {0.alert_name} since {0.alert_duration}>".format(self)

    @classmethod
    def create_event(cls, data):
        return cls(
            data.get('monitorFriendlyName'),
            data.get('alertType'),
            data.get('alertTypeFriendlyName'),
            data.get('alertDetails'),
            data.get('alertDuration'),
        )


class Store:

    def __init__(self):
        self.store = deque()

    @classmethod
    def init_app(cls, app):
        return cls()

    def select(self):
        return self.store

    def flush(self, size):
        self.store = deque(islice(self.store, 0, size))

    def insert(self, item):
        self.store.appendleft(item)

    def create(self, data):
        event = Event.create_event(data)
        self.insert(event)
        return event

    def __repr__(self):
        return '<Store with {} events>'.format(len(self.store))

    def __len__(self):
        return len(self.store)


storage = Store()
