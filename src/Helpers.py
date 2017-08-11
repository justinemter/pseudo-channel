import os

import logging

class Helpers():
	"""Class for consolidating helper methods"""

	def __init__(self):

		pass

	def save_file(self, data, filename, path, overwrite=True):

        fileName = filename

        writepath = path

        if not os.path.exists(writepath):

            os.makedirs(writepath)

        if os.path.exists(writepath+fileName) and overwrite:
            
            os.remove(writepath+fileName)

        mode = 'a' if os.path.exists(writepath) else 'w'

        with open(writepath+fileName, mode) as f:

            f.write(data)

	def get_file(self, filename, path):

		if not os.path.exists(writepath):

            raise IOError("{}, doesn't exist").format(writepath)

        if not os.path.exists(writepath+fileName):
            
            raise IOError("{}, doesn't exist").format(fileName)

		return None

