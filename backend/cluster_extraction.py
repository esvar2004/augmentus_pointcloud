"""This module performs cluster extraction from a point cloud."""
import numpy as np
import open3d as o3d

from point_cloud_processor import PointCloudProcessor

MAIN_COLOR = (0.12, 0.47, 0.71)  # blue
NOISE_COLOR = (0.84, 0.15, 0.16)  # red
SMALL_COLOR = (1.0, 0.5, 0.05)  # orange

class ClusterExtractor(PointCloudProcessor):
	"""Extracts clusters using DBSCAN and colors them by cluster."""

	def __init__(self, eps: float, min_points: int) -> None:
		self.eps = eps
		self.min_points = min_points
		self.labels: np.ndarray | None = None

	def process(self, cld: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
		"""
		Cluster cld with DBSCAN and color its points by cluster.

		Sets self.labels to the per-point cluster label produced by DBSCAN (-1 indicates noise).

		Args:
			cld: The input point cloud.
		"""
		if len(cld.points) == 0:
			raise ValueError("Input point cloud is empty. Cannot extract clusters from an empty point cloud.")
		self.labels = np.array(cld.cluster_dbscan(eps=self.eps, min_points=self.min_points))
		self.assign_colors(cld, self.labels)
		return cld

	def assign_colors(self, cld: o3d.geometry.PointCloud, labels: np.ndarray) -> None:
		"""
		Color the largest cluster in labels MAIN_COLOR, noise points NOISE_COLOR, and the
		remaining small clusters SMALL_COLOR.

		Args:
			cld: The point cloud whose colors will be set.
			labels: Cluster label for each point in cld, as returned by cluster_dbscan (-1 indicates noise).
		"""
		colors = np.zeros((len(labels), 3))
		colors[labels == -1] = NOISE_COLOR
		real_labels, counts = np.unique(labels[labels >= 0], return_counts=True)
		if len(real_labels) > 0:
			colors[labels >= 0] = SMALL_COLOR
			colors[labels == real_labels[np.argmax(counts)]] = MAIN_COLOR # Assigns the main cluster color to the largest cluster.
		cld.colors = o3d.utility.Vector3dVector(colors)
