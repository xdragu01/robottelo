"""Unit tests for the ``ptables`` paths.

A full API reference for patition tables can be found here:
http://theforeman.org/api/apidoc/v2/ptables.html

"""
from ddt import ddt
from fauxfactory import gen_string
from nailgun import entities
from random import randint
from requests.exceptions import HTTPError
from robottelo.common.constants import OPERATING_SYSTEMS
from robottelo.common.decorators import data, skip_if_bug_open
from robottelo.test import APITestCase


@ddt
class PartitionTableTestCase(APITestCase):
    """Tests for the ``ptables`` path."""

    @skip_if_bug_open('bugzilla', 1229384)
    @data(
        gen_string('alphanumeric', 1),
        gen_string('alpha', 1),
        gen_string('cjk', 1),
        gen_string('latin1', 1),
        gen_string('numeric', 1),
        gen_string('utf8', 1),
    )
    def test_bugzilla_1229384(self, name):
        """@Test: Create Partition table with 1 symbol in name

        @Assert: Partition table was created

        @Feature: Partition Table - Create

        @BZ: 1229384

        """
        ptable = entities.PartitionTable(name=name).create()
        self.assertEqual(ptable.name, name)

    @data(
        gen_string('alphanumeric', randint(1, 255)),
        gen_string('alpha', randint(1, 255)),
        gen_string('cjk', randint(1, 85)),
        gen_string('latin1', randint(1, 255)),
        gen_string('numeric', randint(1, 255)),
        gen_string('utf8', randint(1, 85)),
    )
    def test_create_ptable_with_different_names(self, name):
        """@Test: Create new partition tables using different inputs as a name

        @Assert: Partition table created successfully and has correct name

        @Feature: Partition Table - Create

        """
        ptable = entities.PartitionTable(name=name).create()
        self.assertEqual(ptable.name, name)

    @data(
        gen_string('alphanumeric', randint(1, 255)),
        gen_string('alpha', randint(1, 255)),
        gen_string('cjk', randint(1, 85)),
        gen_string('latin1', randint(1, 255)),
        gen_string('numeric', randint(1, 255)),
        gen_string('utf8', randint(1, 85)),
    )
    def test_create_ptable_with_different_layouts(self, layout):
        """@Test: Create new partition tables using different inputs as a
        layout

        @Assert: Partition table created successfully and has correct layout

        @Feature: Partition Table - Create

        """
        ptable = entities.PartitionTable(layout=layout).create()
        self.assertEqual(ptable.layout, layout)

    def test_create_ptable_with_operating_system(self):
        """@Test: Create new partition table with random operating system

        @Assert: Partition table created successfully and has correct operating
        system

        @Feature: Partition Table - Create

        """
        os_family = OPERATING_SYSTEMS[randint(0, 8)]
        ptable = entities.PartitionTable(os_family=os_family).create()
        self.assertEqual(ptable.os_family, os_family)

    @data(
        '',
        ' ',
        gen_string('alphanumeric', 300),
        gen_string('alpha', 300),
        gen_string('cjk', 300),
        gen_string('latin1', 300),
        gen_string('numeric', 300),
        gen_string('utf8', 300),
        gen_string('html', 300),
    )
    def test_create_ptable_with_different_names_negative(self, name):
        """@Test: Try to create partition table using invalid names only

        @Assert: Partition table was not created

        @Feature: Partition Table - Create

        """
        with self.assertRaises(HTTPError):
            entities.PartitionTable(name=name).create()

    @data(
        '',
        ' ',
        None
    )
    def test_create_ptable_with_no_layout_negative(self, layout):
        """@Test: Try to create partition table with empty layout

        @Assert: Partition table was not created

        @Feature: Partition Table - Create

        """
        with self.assertRaises(HTTPError):
            entities.PartitionTable(layout=layout).create()

    def test_delete_ptable(self):
        """@Test: Delete partition table

        @Assert: Partition table was deleted

        @Feature: Partition Table - Delete

        """
        ptable = entities.PartitionTable().create()
        ptable.delete()
        with self.assertRaises(HTTPError):
            ptable.read()

    @data(
        gen_string('alphanumeric', randint(1, 255)),
        gen_string('alpha', randint(1, 255)),
        gen_string('cjk', randint(1, 85)),
        gen_string('latin1', randint(1, 255)),
        gen_string('numeric', randint(1, 255)),
        gen_string('utf8', randint(1, 85)),
    )
    def test_update_ptable_with_new_name(self, new_name):
        """@Test: Update partition tables with new name

        @Assert: Partition table updated successfully and name was changed

        @Feature: Partition Table - Update

        """
        ptable = entities.PartitionTable().create()
        ptable.name = new_name
        self.assertEqual(ptable.update(['name']).name, new_name)

    @data(
        gen_string('alphanumeric', randint(1, 255)),
        gen_string('alpha', randint(1, 255)),
        gen_string('cjk', randint(1, 85)),
        gen_string('latin1', randint(1, 255)),
        gen_string('numeric', randint(1, 255)),
        gen_string('utf8', randint(1, 85)),
    )
    def test_update_ptable_with_new_layout(self, new_layout):
        """@Test: Update partition table with new layout

        @Assert: Partition table updated successfully and layout was changed

        @Feature: Partition Table - Update

        """
        ptable = entities.PartitionTable().create()
        ptable.layout = new_layout
        self.assertEqual(ptable.update(['layout']).layout, new_layout)

    def test_update_ptable_with_new_operating_system(self):
        """@Test: Update partition table with new random operating system

        @Assert: Partition table updated successfully and operating system was
        changed

        @Feature: Partition Table - Update

        """
        ptable = entities.PartitionTable(
            os_family=OPERATING_SYSTEMS[0],
        ).create()
        new_os_family = OPERATING_SYSTEMS[randint(1, 8)]
        ptable.os_family = new_os_family
        self.assertEqual(ptable.update(['os_family']).os_family, new_os_family)

    @data(
        '',
        ' ',
        gen_string('alphanumeric', 300),
        gen_string('alpha', 300),
        gen_string('cjk', 300),
        gen_string('latin1', 300),
        gen_string('numeric', 300),
        gen_string('utf8', 300),
        gen_string('html', 300),
    )
    def test_update_ptable_with_new_name_negative(self, new_name):
        """@Test: Try to update partition table using invalid names only

        @Assert: Partition table was not updated

        @Feature: Partition Table - Update

        """
        ptable = entities.PartitionTable().create()
        ptable.name = new_name
        with self.assertRaises(HTTPError):
            self.assertNotEqual(ptable.update(['name']).name, new_name)

    @data(
        '',
        ' ',
        None
    )
    def test_update_ptable_with_empty_layout_negative(self, new_layout):
        """@Test: Try to update partition table with empty layout

        @Assert: Partition table was not updated

        @Feature: Partition Table - Update

        """
        ptable = entities.PartitionTable().create()
        ptable.layout = new_layout
        with self.assertRaises(HTTPError):
            self.assertNotEqual(ptable.update(['layout']).layout, new_layout)
