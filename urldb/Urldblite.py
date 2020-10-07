import re
import zlib
from urllib import parse
import ujson
import pyperclip
import base64


class UrlDBlite:
	"""
	A "database" class that is really just an alternative representation of the data.

	*Аргументы*

	:param base: link to add query string
	:type base: ``str``, optional
	:param setdb: convert URL to urlDB class
	:type setdb: ``str``, URL, optional
	:param compress: compressing data in URL
	:type compress: ``bool``
	"""
	def __init__(self, base: str = None, setdb: str = None, compress: bool = None):
		self.data = list()
		if setdb:
			if "#c" in setdb:
				if compress is None or compress is True:
					self.compress = True
					self._parse_link_to_db(setdb)
				else:
					self.compress = False
					self.data = self._decode_with_decompress(setdb)
			else:
				self.compress = False
				self._parse_link_to_db(setdb)
		else:
			self.compress = True if compress else False
			if base and self._is_base_url(base):
				self.base = base
				self._url = self.base
			else:
				self.base = "https://urldb.pfel.cc/datalite"
				self._url = self.base

	def _is_base_url(self, url):
		if re.match(r"(https?://)([a-zA-Z0-9\-_.?]+)(/?[a-zA-Z0-9/]+)", url):
			return True
		else:
			return False

	def _parse_link_to_db(self, to_parse):
		if len(to_parse.split("?")) > 1:
			self.base = to_parse.split("?")[0]
			self.data = self._decode(to_parse.split("?")[-1].split("#")[0])
			self._update_link()

	def _encode(self, data):
		if self.compress:
			return self._encode_with_compress(data)
		else:
			return self._encode_without_compress(data)

	def _decode(self, to):
		if self.compress:
			return self._decode_with_decompress(to)
		else:
			return self._decode_without_decompress(to)

	def _encode_without_compress(self, to_encode: list):
		pd = []
		for v in to_encode:
			pd.append(f"{parse.quote(ujson.dumps(v))}")
		enc = "&".join(pd)
		return enc

	def _encode_with_compress(self, to_encode: list):
		return base64.urlsafe_b64encode(zlib.compress(ujson.dumps(to_encode)[1:-1].encode("utf-8"))).decode()

	def _decode_with_decompress(self, to_decode: str):
		return ujson.loads(zlib.decompress(base64.urlsafe_b64decode(f"[{to_decode}]".encode())).decode())

	def _to_value(self, arg):
		if arg.isdigit():
			return int(arg)
		else:
			try:
				return ujson.loads(arg)
			except ValueError as e:
				return ujson.loads(f'"{arg}"')

	def _decode_without_decompress(self, to_decode: str):
		data = list()
		pd = to_decode.split("&")
		for i in pd:
			v = parse.unquote(i)
			v = self._to_value(v)
			data.append(v)
		return data

	@property
	def link_data(self):
		return self._encode(self.data)

	def _update_link(self):
		if len(self.__dict__):
			self._url = f"{self.base}?{self.link_data}#{'c' if self.compress else 'n'}"
		else:
			self._url = f"{self.base}"

	def to_clipboard(self):
		"""
		Copy to clipboard
		"""
		pyperclip.copy(self._url)

	def __setitem__(self, key, item):
		self.data[key] = item
		self._update_link()

	def __getitem__(self, key):
		return self.data[key]

	def __repr__(self):
		return f"<urlDB {self.url}>"

	def __len__(self):
		return len(self.data)

	def __delitem__(self, key):
		del self.data[key]
		self._update_link()

	def __iadd__(self, value):
		self.data.append(value)
		return self

	def add(self, value):
		self.data.append(value)

	def clear(self):
		"""
		Clear the data dict

		:return: clear URL (``str``)
		"""
		self.data.clear()
		return self.url

	def copy(self):
		"""
		Make a copy of the data dict

		:return: ``dict``
		"""
		return self.data.copy()

	def pop(self, *args):
		"""
		:param: key of pop item
		:return: value of pop item
		"""
		x = self.data.pop(*args)
		self._update_link()
		return x

	def __cmp__(self, dict_):
		return self.__cmp__(self.data, dict_)

	def __contains__(self, item):
		return item in self.data

	def __iter__(self):
		return iter(self.data)

	@property
	def url(self):
		self._update_link()
		return self._url
