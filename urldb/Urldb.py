import re
import zlib
from urllib import parse
import ujson
import pyperclip


class UrlDB:
	"""
	Класс "базы данных", которая на самом деле является просто альтернативным представлением данных.

	*Аргументы*
	:param base: начальная часть URL, на которую будут накладываться данные
	:type base: ``str``, optional
	:param setdb: можно уже имеющуюся строку прочитать и сделать из неё понятное и редактируемое хранилище
	:type setdb: ``str``, optional
	:param compress: добавить ли сжатие данных в URL с помощью zlib
	:type compress: ``bool``
	"""
	def __init__(self, base: str = None, setdb: str = None, compress: bool = None):
		self.link_data = ""
		self.data = dict()
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
				self.url = self.base
			else:
				self.base = "https://urldb.pfel.cc/data"
				self.url = self.base

	def _is_base_url(self, url):
		if re.match(r"(https?:\/\/)([a-zA-Z0-9\-\_.?]+)(\/?[a-zA-Z0-9\/]+)", url):
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

	def _encode_without_compress(self, to_encode: dict):
		pd = []
		for k, v in to_encode.items():
			pd.append(f"{parse.quote(ujson.dumps(k))}={parse.quote(ujson.dumps(v))}")
		enc = "&".join(pd)
		return enc

	def _encode_with_compress(self, to_encode: dict):
		return parse.quote(zlib.compress(ujson.dumps(to_encode).encode("utf-8")))

	def _decode_with_decompress(self, to_decode: str):
		return ujson.loads(zlib.decompress(parse.unquote_to_bytes(to_decode)).decode())

	def _to_value(self, arg):
		if arg.isdigit():
			return int(arg)
		else:
			try:
				return ujson.loads(arg)
			except ValueError as e:
				return ujson.loads(f'"{arg}"')

	def _decode_without_decompress(self, to_decode: str):
		data = dict()
		pd = to_decode.split("&")
		for i in pd:
			tmp = i.split("=")
			k, v = parse.unquote(tmp[0]), parse.unquote(tmp[1])
			k, v = self._to_value(k), self._to_value(v)
			data[k] = v
		return data

	def _update_link(self):
		if len(self.__dict__):
			self.link_data = self._encode(self.data)
			self.url = f"{self.base}?{self.link_data}#{'c' if self.compress else 'n'}"
		else:
			self.url = f"{self.base}"

	def to_clipboard(self):
		"""
		Втавсляет в буфер обмена строку
		"""
		pyperclip.copy(self.url)

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

	def clear(self):
		"""
		Очищает данные и возвращает чистый URL
		:return: URL (``str``)
		"""
		self.data.clear()
		self._update_link()
		return self.url

	def copy(self):
		return self.data.copy()

	def has_key(self, k):
		return k in self.data

	def update(self, *args, **kwargs):
		self.data.update(*args, **kwargs)
		self._update_link()
		return self.data.update({})

	def keys(self):
		return self.data.keys()

	def values(self):
		return self.data.values()

	def items(self):
		return self.data.items()

	def pop(self, *args):
		x = self.data.pop(*args)
		self._update_link()
		return x

	def __cmp__(self, dict_):
		return self.__cmp__(self.data, dict_)

	def __contains__(self, item):
		return item in self.data

	def __iter__(self):
		return iter(self.data)
