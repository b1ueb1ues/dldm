from .Component import Component
from .PPtr import PPtr


class StaticBatchInfo:
	def __init__(self, reader):
		self.firstSubMesh = reader.read_u_short()
		self.subMeshCount = reader.read_u_short()


class Renderer(Component):
	def __init__(self, reader):
		super().__init__(reader=reader)
		version = self.version
		if version[0] < 5:  # 5.0 down
			self.m_Enabled = reader.read_boolean()
			self.m_CastShadows = reader.read_boolean()
			self.m_ReceiveShadows = reader.read_boolean()
			self.m_LightmapIndex = reader.read_byte()
		else:  # 5.0 and up
			if version[0] > 5 or (version[0] == 5 and version[1] >= 4):  # 5.4 and up
				self.m_Enabled = reader.read_boolean()
				self.m_CastShadows = reader.read_byte()
				self.m_ReceiveShadows = reader.read_byte()
				if version[0] > 2017 or (version[0] == 2017 and version[0] >= 2):  # 2017.2 and up
					self.m_DynamicOccludee = reader.read_byte()
				self.m_MotionVectors = reader.read_byte()
				self.m_LightProbeUsage = reader.read_byte()
				self.m_ReflectionProbeUsage = reader.read_byte()
				reader.align_stream()
			else:
				self.m_Enabled = reader.read_boolean()
				reader.align_stream()
				self.m_CastShadows = reader.read_byte()
				self.m_ReceiveShadows = reader.read_boolean()
				reader.align_stream()

			if version[0] >= 2018:  # 2018 and up
				self.m_RenderingLayerMask = reader.read_u_int()

			if version[0] > 2018 or (version[0] == 2018 and version[1] >= 3):  # 2018.3 and up
				self.m_RendererPriority = reader.read_int()

			self.m_LightmapIndex = reader.read_u_short()
			self.m_LightmapIndexDynamic = reader.read_u_short()

		if version[0] >= 3:  # 3.0 and up
			self.m_LightmapTilingOffset = reader.read_vector4()

		if version[0] >= 5:  # 5.0 and up
			self.m_LightmapTilingOffsetDynamic = reader.read_vector4()

		m_MaterialsSize = reader.read_int()
		self.m_Materials = [
			PPtr(reader)  # Material
			for _ in range(m_MaterialsSize)
		]

		if version[0] < 3:  # 3.0 down
			self.m_LightmapTilingOffset = reader.read_vector4()
		else:  # 3.0 and up
			if version[0] > 5 or (version[0] == 5 and version[1] >= 5):  # 5.5 and up
				self.m_StaticBatchInfo = StaticBatchInfo(reader)
			else:
				self.m_SubsetIndices = reader.read_u_int_array()

			self.m_StaticBatchRoot = PPtr(reader)  # Transform

		if version[0] > 5 or (version[0] == 5 and version[1] >= 4):  # 5.4 and up
			self.m_ProbeAnchor = PPtr(reader)  # Transform
			self.m_LightProbeVolumeOverride = PPtr(reader)  # GameObject
		elif version[0] > 3 or (version[0] == 3 and version[1] >= 5):  # 3.5 - 5.3
			self.m_UseLightProbes = reader.read_boolean()
			reader.align_stream()

			if version[0] >= 5:  # 5.0 and up
				self.m_ReflectionProbeUsage = reader.read_int()

			self.m_LightProbeAnchor = PPtr(reader)  # Transform #5.0 and up m_ProbeAnchor

		if version[0] > 4 or (version[0] == 4 and version[1] >= 3):  # 4.3 and up
			if version[0] == 4 and version[1] == 3:  # 4.3
				self.m_SortingLayer = reader.read_short()
			else:
				self.m_SortingLayerID = reader.read_u_int()

			# SInt16 m_SortingLayer 5.6 and up
			self.m_SortingOrder = reader.read_short()
			reader.align_stream()
