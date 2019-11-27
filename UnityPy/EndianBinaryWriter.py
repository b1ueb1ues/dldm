import io
import struct

from .math import Color, Matrix4x4, Quaternion, Vector2, Vector3, Vector4, Rectangle


class EndianBinaryWriter:
	endian: str
	Length: int
	Position: int
	stream: io.BufferedReader

	def __init__(self, input_, endian='>'):
		if isinstance(input_, (bytes, bytearray)):
			self.stream = io.BytesIO(input_)
		elif isinstance(input_, (io.BytesIO, io.BufferedReader)):
			self.stream = input_
		else:
			raise ValueError("Invalid input type - %s."%type(input_))
		self.endian = endian

	@property
	def bytes(self):
		self.stream.seek(0)
		return self.stream.read()

	def dispose(self):
		self.stream.close()
		pass

	def write(self, *args):
		self.stream.write(*args)

	def write_byte(self, value: int):
		self.write(struct.pack(self.endian + "b", value))

	def write_u_byte(self, value: int):
		self.write(struct.pack(self.endian + "B", value))

	def write_bytes(self, value: bytes):
		return self.write(value)

	def write_short(self, value: int):
		self.write(struct.pack(self.endian + "h", value))

	def write_int(self, value: int):
		self.write(struct.pack(self.endian + "i", value))

	def write_long(self, value: int):
		self.write(struct.pack(self.endian + "q", value))

	def write_u_short(self, value: int):
		self.write(struct.pack(self.endian + "H", value))

	def write_u_int(self, value: int):
		self.write(struct.pack(self.endian + "I", value))

	def write_u_long(self, value: int):
		self.write(struct.pack(self.endian + "Q", value))

	def write_float(self, value: float):
		self.write(struct.pack(self.endian + "f", value))

	def write_double(self, value: float):
		self.write(struct.pack(self.endian + "d", value))

	def write_boolean(self, value: bool):
		self.write(struct.pack(self.endian + "?", value))

	"""
	def write_string(self, size=None, encoding="utf-8") -> str:
		if size is None:
			ret = self.write_string_to_null()
		else:
			ret = struct.unpack(f"{self.endian}{size}is", self.read(size))[0]
		try:
			return ret.decode(encoding)
		except UnicodeDecodeError:
			return ret
	"""

	def write_string_to_null(self, value: str):
		self.write(value.encode('utf8'))
		self.write(b"\0")

	def write_aligned_string(self, value: str):
		self.write_int(len(value))
		self.write(value.encode("utf8", 'backslashreplace'))
		self.align_stream(4)

	def align_stream(self, alignment=4):
		pos = self.stream.tell()
		mod = pos % alignment
		if mod != 0:
			self.write(b"\0" * (alignment - mod))

	def write_quaternion(self, value: Quaternion):
		self.write_float(value.X)
		self.write_float(value.Y)
		self.write_float(value.Z)
		self.write_float(value.W)

	def write_vector2(self, value: Vector2):
		self.write_float(value.X)
		self.write_float(value.Y)

	def write_vector3(self, value: Vector3):
		self.write_float(value.X)
		self.write_float(value.Y)
		self.write_float(value.Z)

	def write_vector4(self, value: Vector4):
		self.write_float(value.X)
		self.write_float(value.Y)
		self.write_float(value.Z)
		self.write_float(value.W)

	def write_rectangle_f(self, value: Rectangle):
		self.write_float(value.x)
		self.write_float(value.y)
		self.write_float(value.width)
		self.write_float(value.height)

	def write_color4(self, value: Color):
		self.write_float(value.R)
		self.write_float(value.G)
		self.write_float(value.B)
		self.write_float(value.A)

	def write_matrix(self, value: Matrix4x4):
		for val in value.M:
			self.write_float(val)

	def write_array(self, command, value: list, write_length: bool = True):
		if write_length:
			self.write_int(len(value))
		for val in value:
			command(val)

	def write_boolean_array(self, value: list):
		self.write_array(self.write_boolean, value)

	def write_u_short_array(self, value: list):
		self.write_array(self.write_u_short, value)

	def write_int_array(self, value: list, write_length: bool = False):
		return self.write_array(self.write_int, value, write_length)

	def write_u_int_array(self, value: list, write_length: bool = False):
		return self.write_array(self.write_u_int, value, write_length)

	def write_float_array(self, value: list, write_length: bool = False):
		return self.write_array(self.write_float, value, write_length)

	def write_string_array(self, value: list):
		self.write_array(self.write_aligned_string, value)

	def write_vector2_array(self, value: list):
		self.write_array(self.write_vector2, value)

	def write_vector4_array(self, value: list):
		self.write_array(self.write_vector4, value)

	def write_matrix_array(self, value: list):
		self.write_array(self.write_matrix, value)
