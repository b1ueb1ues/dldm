from .NamedObject import NamedObject


class Texture(NamedObject):
	def __init__(self, reader):
		super().__init__(reader=reader)
		if self.version[0] > 2017 or (self.version[0] == 2017 and self.version[1] >= 3):  # 2017.3 and up
			self.forced_fallback_format = reader.read_int()
			self.downscale_fallback = reader.read_boolean()
			reader.align_stream()
