"""ZODB3 backend.

For copyright, license, and warranty, see bottom of file.
"""

from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from persistent.list import PersistentList
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction


from schevozodb.backend_test_classes import (
    TestMethods_CreatesDatabase,
    TestMethods_CreatesSchema,
    TestMethods_EvolvesSchemata,
    )


class ZodbBackend(object):

    description = 'Backend that directly uses ZODB 3.7.0'
    backend_args_help = """
    (no backend options)
    """

    __test__ = False

    BTree = OOBTree
    PDict = PersistentMapping
    PList = PersistentList

    TestMethods_CreatesDatabase = TestMethods_CreatesDatabase
    TestMethods_CreatesSchema = TestMethods_CreatesSchema
    TestMethods_EvolvesSchemata = TestMethods_EvolvesSchemata

    def __init__(self, filename):
        self._filename = filename
        self._is_open = False
        self.open()

    @classmethod
    def args_from_string(cls, s):
        """Return a dictionary of keyword arguments based on a string given
        to a command-line tool."""
        kw = {}
        if s is not None:
            for arg in (p.strip() for p in s.split(',')):
                name, value = (p2.strip() for p2 in arg.split('='))
                raise KeyError(
                    '%s is not a valid name for backend args' % name)
        return kw

    @classmethod
    def usable_by_backend(cls, filename):
        """Return (True, additional_backend_args) if the named file is
        usable by this backend, or False if not."""
        # Get first 128 bytes of file.
        f = open(filename, 'rb')
        header = f.read(128)
        f.close()
        # Look for ZODB signatures.
        if header[:4] == 'FS21' and 'persistent.mapping' in header:
            return (True, {})
        return False

    def open(self):
        if not self._is_open:
            self.storage = FileStorage(self._filename)
            self.zodb = DB(self.storage)
            self.conn = self.zodb.open()
            self._is_open = True

    def get_root(self):
        """Return the connection 'root' object."""
        return self.conn.root()

    @property
    def has_db(self):
        """Return True if the backend has a schevo db."""
        return self.get_root().has_key('SCHEVO')

    def commit(self):
        """Commit the current transaction."""
        transaction.commit()

    def rollback(self):
        """Abort the current transaction."""
        transaction.abort()

    def pack(self):
        """Pack the underlying storage."""
        self.zodb.pack()

    def close(self):
        """Close the underlying storage (and the connection if needed)."""
        self.rollback()
        self.conn.close()
        self.zodb.close()
        self.storage.close()
        self._is_open = False


# Copyright (C) 2001-2006 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# 709 East Jackson Road
# Saint Louis, MO  63119-4241
# http://orbtech.com/
#
# This toolkit is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
