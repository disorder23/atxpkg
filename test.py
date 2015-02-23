#!/usr/bin/python3

import unittest
import os
import shutil
import subprocess
import tempfile

from utils import *

class MyOtherTestCase(unittest.TestCase):
	def setUp(self):
		#self.d = tempfile.mkdtemp()
		self.d = '/tmp/atxpkg'
		if os.path.isdir(self.d): shutil.rmtree(self.d)
		os.mkdir('/tmp/atxpkg')

		if os.path.isdir('/tmp/atxpkg_dest'): shutil.rmtree('/tmp/atxpkg_dest')

		with open('%s/repos.txt' % self.d, 'w') as f:
			f.write('http://atxpkg.asterix.cz\n')
			f.write('http://atxpkg-dev.asterix.cz\n')
		#endwith
	#endef

	def test_install(self):
		subprocess.check_call('./atxpkg install atxpkg --yes --prefix=/tmp/atxpkg_dest', shell=True)
		subprocess.check_call('./atxpkg update atxpkg..router --yes --prefix=/tmp/atxpkg_dest', shell=True)
		subprocess.check_call('./atxpkg remove router --yes --prefix=/tmp/atxpkg_dest', shell=True)
	#enddef

	def tearDowon(self):
		if os.path.isdir(self.d): shutil.rmtree(self.d)
		if os.path.isdir('/tmp/atxpkg_dest'): shutil.rmtree('/tmp/atxpkg_dest')
	#enddef
#endclass


class MyTestCase(unittest.TestCase):
	def test_package_name(self):
		self.assertEqual(get_package_name('package-3.5.6-1.atxpkg.zip'), 'package')
		self.assertEqual(get_package_name('package-3.5.6-1'), 'package')
		self.assertEqual(get_package_name('package'), 'package')

		self.assertEqual(get_package_name('package-name-3.5.6-1.atxpkg.zip'), 'package-name')
		self.assertEqual(get_package_name('package-name-3.5.6-1'), 'package-name')
		self.assertEqual(get_package_name('package-name'), 'package-name')
	#enddef

	def test_package_version(self):
		self.assertEqual(get_package_version('package-3.5.6-1.atxpkg.zip'), '3.5.6-1')
		self.assertEqual(get_package_version('package-with-hyphen-3.5.6-1.atxpkg.zip'), '3.5.6-1')

		self.assertEqual(get_package_version('package'), None)
		self.assertEqual(get_package_version('package-with-hyphen'), None)
	#enddef

	def test_valid_package_fn(self):
		self.assertTrue(is_valid_package_fn('package-3.5.6-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package-name-3.5.6-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package_name-3.5.6-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package-name.dev-3.5.6-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package-name-3-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package.dev-20150101145536-6.atxpkg.zip'))
		self.assertTrue(is_valid_package_fn('package-name.dev-20150101145536-6.atxpkg.zip'))

		self.assertFalse(is_valid_package_fn('package-xxx-6.atxpkg.zip'))
		self.assertFalse(is_valid_package_fn('package-name-xxx-xxx.atxpkg.zip'))
		self.assertFalse(is_valid_package_fn('package-name-3-6.xxx.zip'))
	#enddef

	def test_max_version(self):
		urls = [
			'http://example.com/repo/package-2.2-3.atxpkg.zip',
			'http://example.com/repo/package-1.2-3.atxpkg.zip',
			'http://example.com/repo/package-1.2-4.atxpkg.zip',
			'http://example.com/repo/package-1.2222-4.atxpkg.zip',
			'http://example.com/repo/package-1.2222-44444.atxpkg.zip',
		]

		self.assertEqual(get_max_version_url(urls), 'http://example.com/repo/package-2.2-3.atxpkg.zip')
	#enddef
#endclass


if __name__ == '__main__':
	unittest.main()
#endif
