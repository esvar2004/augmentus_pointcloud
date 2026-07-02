"""Tests for normal_estimation.py"""
import open3d as o3d
import pytest

from pipeline.normal_estimation import NormalEstimator

@pytest.fixture
def sample_point_cloud() -> o3d.geometry.PointCloud:
	point_cloud = o3d.data.EaglePointCloud()
	cld = o3d.io.read_point_cloud(point_cloud.path)
	cld.normals = o3d.utility.Vector3dVector()
	return cld

def test_estimates_normals(sample_point_cloud):
	assert not sample_point_cloud.has_normals()

	processed = NormalEstimator(radius=0.1, max_nn=30).process(sample_point_cloud)

	assert processed.has_normals()
	assert len(processed.normals) == len(processed.points) # Asserting a 1:1 correspondence between points and normals.
