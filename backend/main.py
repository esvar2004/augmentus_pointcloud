"""Main orchestrator file for handling end-to-end point cloud processing."""
import open3d as o3d

class MainApp:
	"""Main application entry point for point cloud processing."""

	def __init__(self) -> None:
		self.name = "MainApp"

	def run(self) -> None:
		"""Load a point cloud, and visualize it."""
		point_cloud = o3d.data.EaglePointCloud()
		pcd = o3d.io.read_point_cloud(point_cloud.path)
		o3d.visualization.draw_geometries([pcd], window_name=f"{self.name}")

if __name__ == "__main__":
	app = MainApp()
	app.run()
