"""This class performs surface normal estimation for point clouds."""
import open3d as o3d

from pipeline.point_cloud_processor import PointCloudProcessor


class NormalEstimator(PointCloudProcessor):
	"""Estimates surface normals for a point cloud."""

	def __init__(self, radius: float, max_nn: int) -> None:
		self.radius = radius
		self.max_nn = max_nn

	def process(self, cld: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
		"""
		Estimate and return cld with surface normals computed.

		Args:
			cld: The input point cloud.
		"""
		if len(cld.points) == 0:
			raise ValueError("Input point cloud is empty. Cannot estimate normals for an empty point cloud.")
		cld.estimate_normals(
			search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=self.radius, max_nn=self.max_nn)
		)
		return cld
