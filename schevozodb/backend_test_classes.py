"""ZODB backend test classes."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

import os
from StringIO import StringIO

from schevo import database
from schevo.lib import module

_db_cache = {
    # (format, version, evolve_skipped, schema_source, suffix):
    #   (db, filename),
    }
_cached_dbs = set(
    # db,
    )


def random_filename():
    return os.tempnam(None, 'schevo')


class TestMethods_CreatesDatabase(object):

    __test__ = False

    @staticmethod
    def backend_base_open(test_object, suffix, schema_source, schema_version):
        """Perform the actual opening of a database, then return it.

        - `test_object`: The instance of the test class we're opening
          a database for.
        - `suffix`: The suffix to use on variable names when storing
          open databases and auxiliary information.
        - `schema_source`: Schema source code to use.
        - `schema_version`: Version of the schema to use.
        """
        db_name = 'db' + suffix
        filename = getattr(test_object, 'filename' + suffix, None)
        if filename is None:
            filename = random_filename()
            db = database.create(
                filename = filename,
                backend_name = 'zodb',
                backend_args = test_object.backend_args,
                schema_source = schema_source,
                schema_version = schema_version,
                format = test_object.format,
                )
        else:
            db = database.open(
                filename = filename,
                backend_name = 'zodb',
                backend_args = test_object.backend_args,
                )
        setattr(test_object, db_name, db)
        setattr(test_object, 'filename' + suffix, filename)
        return db

    @staticmethod
    def backend_close(test_object, suffix=''):
        """Perform the actual closing of a database.

        - `test_object`: The instance of the test class we're closing
          a database for.
        - `suffix`: The suffix to use on variable names when finding
          the database and auxiliary information for it.
        """
        db_name = 'db' + suffix
        db = getattr(test_object, db_name)
        if db not in _cached_dbs:
            db.close()

    @staticmethod
    def backend_convert_format(test_object, suffix, format):
        """Convert the internal structure format of an already-open database.

        - `test_object`: The instance of the test class we're
          converting a database for.
        - `suffix`: The suffix to use on variable names when finding
          the database and auxiliary information for it.
        """
        filename = getattr(test_object, 'filename' + suffix)
        # Convert it to the requested format.
        database.convert_format(
            filename = filename,
            backend = test_object.backend_name,
            backend_args = test_object.backend_args,
            format = format,
            )

    @staticmethod
    def backend_reopen_finish(test_object, suffix):
        """Perform cleanup required at the end of a call to
        `test_object.reopen()` within a test.

        - `test_object`: The instance of the test class performing the
          reopen.
        - `suffix`: The suffix to use on variable names when finding
          the database and auxiliary information for it.
        """
        pass

    @staticmethod
    def backend_reopen_save_state(test_object, suffix):
        """Save the state of a database file before it gets closed
        during a call to `test_object.reopen()` within a test.

        - `test_object`: The instance of the test class performing the
          reopen.
        - `suffix`: The suffix to use on variable names when finding
          the database and auxiliary information for it.
        """
        db = getattr(test_object, 'db' + suffix)
        db.backend.close()


class TestMethods_CreatesSchema(TestMethods_CreatesDatabase):

    __test__ = False

    @staticmethod
    def backend_open(test_object, suffix, schema, reopening=False):
        """Perform the actual opening of a database for a test
        instance.

        - `test_object`: The instance of the test class we're opening
          a database for.
        - `suffix`: The suffix to use on variable names when storing
          open databases and auxiliary information.
        - `schema`: Schema source code to use.
        """
        format = test_object.format
        db_name = 'db' + suffix
        filename_name = 'filename' + suffix
        cache_key = (format, 1, None, schema, suffix)
        if (test_object._use_db_cache
            and cache_key in _db_cache
            and not hasattr(test_object, filename_name)
            ):
            db, filename = _db_cache[cache_key]
            setattr(test_object, filename_name, filename)
            if not hasattr(test_object, db_name):
                db._reset_all()
            setattr(test_object, db_name, db)
        else:
            # Forget existing modules.
            for m in module.MODULES:
                module.forget(m)
            db = test_object._base_open(suffix, schema)
        if test_object._use_db_cache:
            filename = getattr(test_object, filename_name)
            db_info = (db, filename)
            _db_cache[cache_key] = db_info
            _cached_dbs.add(db)
        return db


class TestMethods_EvolvesSchemata(TestMethods_CreatesDatabase):

    __test__ = False

    @staticmethod
    def backend_open(test_object):
        """Perform the actual opening of a database for a test
        instance.

        - `test_object`: The instance of the test class we're opening
          a database for.
        """
        format = test_object.format
        use_db_cache = test_object._use_db_cache
        filename_name = 'filename'
        schema = test_object.schemata[-1]
        version = test_object.schema_version
        skip_evolution = test_object.skip_evolution
        suffix = ''
        cache_key = (format, version, skip_evolution, schema, suffix)
        if (use_db_cache
            and cache_key in _db_cache
            and not hasattr(test_object, filename_name)
            ):
            db, filename = _db_cache[cache_key]
            test_object.filename = filename
            if not hasattr(test_object, 'db'):
                db._reset_all()
            test_object.db = db
        else:
            # Forget existing modules.
            for m in module.MODULES:
                module.forget(m)
        if not skip_evolution:
            # Open database with version 1.
            db = test_object._base_open(suffix, test_object.schemata[0])
            # Evolve to latest.
            for i in xrange(1, len(test_object.schemata)):
                schema_source = test_object.schemata[i]
                database.evolve(db, schema_source, version=i+1)
        else:
            # Open database with target version.
            db = test_object._base_open(suffix, schema, schema_version=version)
        if use_db_cache:
            filename = test_object.filename
            _db_cache[cache_key] = (db, filename)
            _cached_dbs.add(db)
        return db
