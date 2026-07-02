"""Main orchestrator file for handling end-to-end point cloud processing."""
import open3d as o3d
from data_loader import DataLoader

class MainApp:
	"""Main application entry point for point cloud processing."""

	def __init__(self) -> None:
		self.name = "MainApp"
		self.data_loader = DataLoader()

	def run(self) -> None:
		"""Loads a point cloud and visualizes it."""
		pcd = self.data_loader.load()
		o3d.visualization.draw_geometries([pcd], window_name=f"{self.name} - Before")

if __name__ == "__main__":
	app = MainApp()
	app.run()
