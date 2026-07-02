"""Tests for downsampling.py"""
import open3d as o3d
import pytest

from downsampling import Downsampler

@pytest.fixture
def sample_point_cloud() -> o3d.geometry.PointCloud:
	point_cloud = o3d.data.EaglePointCloud()
	return o3d.io.read_point_cloud(point_cloud.path)

def test_point_count_reduction(sample_point_cloud):
	downsampled = Downsampler(voxel_size=0.05).process(sample_point_cloud)

	# Asserting that downsampled point cloud contains fewer points.
	assert len(downsampled.points) < len(sample_point_cloud.points)
