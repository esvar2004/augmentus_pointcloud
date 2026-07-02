"""Main orchestrator file for handling end-to-end point cloud processing."""
import argparse
import open3d as o3d

from data_loader import DataLoader
from downsampling import Downsampler
from normal_estimation import NormalEstimator

class MainApp:
	"""Main application entry point for point cloud processing."""

	def __init__(self, voxel_size: float, normal_radius: float, normal_max_nn: int) -> None:
		self.name = "MainApp"
		self.data_loader = DataLoader()
		self.downsampler = Downsampler(voxel_size=voxel_size)
		self.normal_estimator = NormalEstimator(radius=normal_radius, max_nn=normal_max_nn)

	def run(self) -> None:
		"""Loads a point cloud, then visualizes it before down-sampling, after down-sampling, and after normal estimation."""
		cld = self.data_loader.load()
		o3d.visualization.draw_geometries([cld], window_name = f"{self.name} - Before")

		downsampled_cld = self.downsampler.process(cld)
		o3d.visualization.draw_geometries([downsampled_cld], window_name = f"{self.name} - After Downsampling")

		normal_estimated_cld = self.normal_estimator.process(downsampled_cld)
		o3d.visualization.draw_geometries(
			[normal_estimated_cld], window_name = f"{self.name} - After Normal Estimation", point_show_normal=True
		)


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
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	app = MainApp(
		voxel_size=args.downsampling,
		normal_radius=args.normal_radius,
		normal_max_nn=args.normal_max_nn,
	)
	app.run()
