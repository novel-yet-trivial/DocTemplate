#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import template

data = dict(
	firstname = "Vincent",
	address = "123 Main St."
	)

template.template("Example.odt", data, "output.odt")


data = dict(
	first = "Vincent"
	)

template.template("Example.docx", data, "output.docx")
