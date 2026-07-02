"""This module provides a DataLoader class for loading point cloud data using Open3D."""
import open3d as o3d

class DataLoader:
	"""Loads point cloud data for downstream processing."""

	def load(self) -> o3d.geometry.PointCloud:
		"""Load and return a point cloud."""
		point_cloud = o3d.data.EaglePointCloud()
		return o3d.io.read_point_cloud(point_cloud.path)
