"""Tests for data_loader.py"""
from data_loader import DataLoader
import open3d as o3d

def test_load_returns_point_cloud():
	cld = DataLoader().load()

	assert isinstance(cld, o3d.geometry.PointCloud) and len(cld.points) > 0
