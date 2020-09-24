import re
import zlib
from urllib import parse
import ujson


class UrlDB:
	"""
	Класс урл'ьной базы данных. Он классный.
	"""
	def __init__(self, base: str = None, setdb: str = None, compress: bool = None):
		self.link_data = ""
		self.data = dict()
		if setdb:
			if "#c" in setdb or (compress is None or compress is True):
				self.compress = True
			else:
				self.compress = False
			self._parse_link_to_db(setdb)
		else:
			self.compress = True if compress else False
			if base and self._is_base_url(base):
				self.base = base
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
			self.data = self._decode(to_parse.split("?")[-1])
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

	def _encode_without_compress(self, data):
		pd = []
		for k, v in data.items():
			pd.append(f"{parse.quote(ujson.dumps(k))}={parse.quote(ujson.dumps(v))}")
		enc = "&".join(pd)
		return enc

	def _encode_with_compress(self, data):
		return parse.quote(zlib.compress(ujson.dumps(data).encode("utf-8")))

	def _decode_with_decompress(self, to):
		return ujson.loads(zlib.decompress(parse.unquote_to_bytes(to)).decode())

	def _decode_without_decompress(self, to):
		data = dict()
		pd = to.split("&")
		for i in pd:
			tmp = i.split("=")
			data[ujson.loads(parse.unquote(tmp[0]))] = ujson.loads(parse.unquote(tmp[1]))
		return data

	def _update_link(self):
		if len(self.__dict__):
			self.link_data = self._encode(self.data)
			self.url = f"{self.base}?{self.link_data}#{'c' if self.compress else 'n'}"
		else:
			self.url = f"{self.base}"

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
