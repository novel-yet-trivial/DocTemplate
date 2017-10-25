#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from zipfile import ZipFile
import tempfile
import shutil

def extract(zip_fn, fn):
	'''extracts the contents of the given file from the given zip file'''
	with ZipFile(zip_fn) as z:
		with z.open(fn) as f:
			return f.read()

def intract(old_name, new_data, data_file, new_name):
	"""add the data to the zipfile with the given filename, overwriting any file
	that already has that name
	:zfn: zip file name
	:data: text data
	:fn: the file name inside the zip file
	"""
	#since zipfile cannot delete files from a zip archive, we have to
	#remake the archive with the 'deleted' file omitted
	tempname = tempfile.mktemp()
	with ZipFile(old_name, 'r') as zipread, ZipFile(tempname, 'w') as zipwrite:
		for item in zipread.infolist():
			if item.filename != data_file:
				data = zipread.read(item.filename)
				zipwrite.writestr(item, data)
		zipwrite.writestr(data_file, new_data)
	shutil.move(tempname, new_name)

def _template(old_fn, data, new_fn, data_file):
	'''generic version'''
	template_data = extract(old_fn, data_file)
	if not isinstance(template_data, str): # python3 check and fix
		template_data = template_data.decode()
	new_data = template_data.format(**data)
	intract(old_fn, new_data, data_file, new_fn)

def template(template_filename, data, new_filename):
	'''auto choose the data file name based on the extension'''
	if template_filename.endswith('.odt'):
		_template(template_filename, data, new_filename, 'content.xml')
	elif template_filename.endswith('.docx'):
		_template(template_filename, data, new_filename, 'word/document.xml')
	else:
		raise ValueError("only .docx and.odt files are supported at the moment")
