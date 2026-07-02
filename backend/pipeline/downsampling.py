"""Point cloud downsampling."""
import open3d as o3d

from pipeline.point_cloud_processor import PointCloudProcessor


class Downsampler(PointCloudProcessor):
	"""Downsamples a given point cloud using a voxel grid filter."""

	def __init__(self, voxel_size: float) -> None:
		self.voxel_size = voxel_size

	def process(self, cld: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
		"""
		Return a down-sampled copy of cld.

		Args:
			cld: The input point cloud.
		"""
		if len(cld.points) == 0:
			raise ValueError("Input point cloud is empty. Cannot down-sample an empty point cloud.")
		return cld.voxel_down_sample(voxel_size=self.voxel_size)
