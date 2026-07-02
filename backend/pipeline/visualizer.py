"""This module saves renders of point clouds as image files."""
from pathlib import Path

import numpy as np
import open3d as o3d

# Camera orientation for the render.
CAMERA_FRONT = (-0.3, -0.65, -0.7)
CAMERA_UP = (-0.3, -0.65, 0.7)

# Directory the renders are saved to.
RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "figures" / "results"


class Visualizer:
	"""Saves renders of a point cloud to image files."""

	def save_render(self, cld: o3d.geometry.PointCloud, filename: str, show_normals: bool = False) -> None:
		"""
		Render the given point cloud and save the image to RESULTS_DIR/filename (PNG).

		Args:
			cld: The point cloud to render.
			filename: Name of the image file to write inside RESULTS_DIR, which is created if missing.
			show_normals: Whether to draw the point normals in the render.
		"""
		if len(cld.points) == 0:
			raise ValueError("Input point cloud is empty. Cannot render an empty point cloud.")
		filename = RESULTS_DIR / filename
		filename.parent.mkdir(parents=True, exist_ok=True)

		vis = o3d.visualization.Visualizer()
		vis.create_window(width=1280, height=960, visible=False)
		vis.add_geometry(cld)

		render_option = vis.get_render_option()
		render_option.background_color = np.ones(3)
		render_option.point_size = 3.0
		render_option.point_show_normal = show_normals

		view_control = vis.get_view_control()
		view_control.set_front(CAMERA_FRONT)
		view_control.set_up(CAMERA_UP)
		view_control.set_lookat(cld.get_center())
		view_control.set_zoom(0.7)

		vis.capture_screen_image(str(filename), do_render=True)
		vis.destroy_window()
