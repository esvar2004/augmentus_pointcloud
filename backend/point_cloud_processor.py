"""Abstract interface for establishing a baseline process function."""
from abc import ABC, abstractmethod

import open3d as o3d

class PointCloudProcessor(ABC):
	"""Base interface for a single point cloud processing responsibility."""

	@abstractmethod
	def process(self, cld: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
		"""Process cld and return the resulting point cloud."""
