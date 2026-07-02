"""Tests for data_loader.py"""
from data_loader import DataLoader
import open3d as o3d

def test_load_returns_point_cloud():
	pcd = DataLoader().load()

	assert isinstance(pcd, o3d.geometry.PointCloud) and len(pcd.points) > 0
