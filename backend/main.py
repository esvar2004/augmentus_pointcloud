"""Main orchestrator file for handling end-to-end point cloud processing."""
import argparse
import open3d as o3d

from data_loader import DataLoader
from downsampling import Downsampler

class MainApp:
	"""Main application entry point for point cloud processing."""

	def __init__(self, voxel_size: float) -> None:
		self.name = "MainApp"
		self.voxel_size = voxel_size
		self.data_loader = DataLoader()
		self.downsampler = Downsampler(voxel_size=self.voxel_size)

	def run(self) -> None:
		"""Loads a point cloud, visualizes it, then visualizes it down-sampled."""
		cld = self.data_loader.load()
		o3d.visualization.draw_geometries([cld], window_name = f"{self.name} - Before")

		downsampled_cld = self.downsampler.process(cld)
		o3d.visualization.draw_geometries([downsampled_cld], window_name = f"{self.name} - After")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Load a point cloud and visualize it before/after down-sampling.")
	parser.add_argument(
		"--downsampling",
		type=float,
		default=0.05,
		help="Voxel size used for down-sampling (larger values remove more points). Default: 0.05",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	app = MainApp(voxel_size=args.downsampling)
	app.run()
