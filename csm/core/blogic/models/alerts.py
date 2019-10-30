"""
 ****************************************************************************
 Filename:          alerts.py
 Description:       Contains the alert model and the interface for alerts
                    repository.

 Creation Date:     12/08/2019
 Author:            Pawan Kumar Srivastava

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import sys
from csm.common.errors import CsmError, CsmNotFoundError
from csm.common.log import Log
from datetime import datetime
from abc import ABC, abstractmethod
from csm.common.queries import SortBy, QueryLimits, DateTimeRange
from typing import Optional, Iterable
import json
import threading
import errno


# TODO: probably, it makes more sense to put alert data directly into the fields of
# the class, rather than storing Alert as a dictionary in the _data field
class Alert(object):
    """
    Represents an alert to be sent to front end
    """

    def __init__(self, data):
        self._key = data.get("alert_uuid", None)
        self._data = data
        self._published = False
        self._timestamp = datetime.utcnow()
        self._resolved = False

    def key(self):
        return self._key

    def data(self):
        return self._data

    def timestamp(self):
        return self._timestamp

    def store(self, key):
        self._key = key
        self._data["alert_uuid"] = key

    def is_stored(self):
        return self._key is not None

    def publish(self):
        self._published = True

    def is_published(self):
        return self._published

    def resolved(self, value):
        self._resolved = value

    def is_resolved(self):
        return self._resolved

# TODO: Consider a more generic approach to storage interfaces
class IAlertStorage(ABC):
    """
    Interface for Alerts repository
    """
    @abstractmethod
    async def store(self, alert: Alert):
        """
        Store an alert.
        It is supposed that the passed object already has the unique key 

        :param alert: Alert object
        :return: nothing
        """
        pass

    @abstractmethod
    async def retrieve(self, alert_id, def_val=None) -> Optional[Alert]:
        """
        Retrieves an alert by its unique key.

        :return: an Alert object or None if there is no such entity
        """
        pass

    @abstractmethod
    async def update(self, alert: Alert):
        """
        Saves the alert object

        :param alert: Alert object
        :return: nothing
        """
        pass

    @abstractmethod
    async def retrieve_by_range(
            self, time_range: DateTimeRange, sort: Optional[SortBy],
            limits: Optional[QueryLimits]) -> Iterable[Alert]:
        """
        Retrieves alerts that occured within the specified time range

        :param time_range: Alerts will be filered according to this parameter.
        :param sort: Alserts will be ordered according to this parameter
        :param limits: Allows to specify offset and limit for the query
        :return: a list of Alert objects
        """
        pass

    @abstractmethod
    async def count_by_range(self, time_range: DateTimeRange) -> int:
        """
        Retrieves the number of alerts that occured within the specified time range

        :param time_range: Alerts will be filered according to this parameter.
        :return: the number of suitable alerts
        """
        pass

    @abstractmethod
    async def retrieve_all(self) -> list:
        """
        Retrieves all the
        """
        pass