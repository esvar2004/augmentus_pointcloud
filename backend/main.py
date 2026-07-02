"""Main orchestrator file for handling end-to-end point cloud processing."""
import argparse

from data_loader import DataLoader
from downsampling import Downsampler
from normal_estimation import NormalEstimator
from cluster_extraction import ClusterExtractor
from visualizer import Visualizer

class MainApp:
	"""Main application entry point for point cloud processing."""

	def __init__(
		self,
		voxel_size: float,
		normal_radius: float,
		normal_max_nn: int,
		cluster_eps: float,
		cluster_min_points: int,
	) -> None:
		self.data_loader = DataLoader()
		self.downsampler = Downsampler(voxel_size=voxel_size)
		self.normal_estimator = NormalEstimator(radius=normal_radius, max_nn=normal_max_nn)
		self.cluster_extractor = ClusterExtractor(eps=cluster_eps, min_points=cluster_min_points)
		self.visualizer = Visualizer()

	def run(self) -> None:
		"""Loads a point cloud and saves a render of it after each stage of the processing pipeline."""
		cld = self.data_loader.load()
		self.visualizer.save_render(cld, "01_initial_point_cloud.png")

		downsampled_cld = self.downsampler.process(cld)
		self.visualizer.save_render(downsampled_cld, "02_downsampled_point_cloud.png")

		normal_estimated_cld = self.normal_estimator.process(downsampled_cld)
		self.visualizer.save_render(normal_estimated_cld, "03_estimated_normals.png", show_normals=True)

		clustered_cld = self.cluster_extractor.process(normal_estimated_cld)
		self.visualizer.save_render(clustered_cld, "04_clusters_extracted.png")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Load a point cloud and visualize it through the processing pipeline.")
	parser.add_argument(
		"--downsampling",
		type=float,
		default=0.05,
		help="Voxel size used for down-sampling (larger values remove a higher concentration of points). Default: 0.05",
	)
	parser.add_argument(
		"--normal-radius",
		type=float,
		default=0.1,
		help="Search radius used for surface normal estimation. Default: 0.1",
	)
	parser.add_argument(
		"--normal-max-nn",
		type=int,
		default=30,
		help="Maximum number of neighbors considered for surface normal estimation. Default: 30",
	)
	parser.add_argument(
		"--cluster-eps",
		type=float,
		default=0.08,
		help="Maximum neighbor distance within a DBSCAN cluster. Default: 0.08",
	)
	parser.add_argument(
		"--cluster-min-points",
		type=int,
		default=10,
		help="Minimum number of points required to form a DBSCAN cluster. Default: 10",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	app = MainApp(
		voxel_size=args.downsampling,
		normal_radius=args.normal_radius,
		normal_max_nn=args.normal_max_nn,
		cluster_eps=args.cluster_eps,
		cluster_min_points=args.cluster_min_points,
	)
	app.run()
