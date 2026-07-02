"""Tests for cluster_extraction.py"""
import numpy as np
import open3d as o3d
import pytest

from cluster_extraction import ClusterExtractor, MAIN_COLOR, NOISE_COLOR, SMALL_COLOR

@pytest.fixture
def sample_point_cloud() -> o3d.geometry.PointCloud:
	point_cloud = o3d.data.EaglePointCloud()
	cld = o3d.io.read_point_cloud(point_cloud.path)
	downsampled = cld.voxel_down_sample(voxel_size=0.05)
	downsampled.colors = o3d.utility.Vector3dVector()  # sample data ships with colors; clear them to test cluster coloring
	return downsampled

def test_extracts_clusters_and_assigns_colors(sample_point_cloud):
	assert not sample_point_cloud.has_colors()

	extractor = ClusterExtractor(eps=0.1, min_points=10)
	processed = extractor.process(sample_point_cloud) # returns the same point cloud object, but with colors assigned

	assert processed.has_colors()
	assert len(processed.colors) == len(processed.points)

def test_produces_more_than_one_segment(sample_point_cloud):
	# "Segments" here refer to the main structure vs. isolated noise, not multiple real clusters.
	# This dataset is one continuous surface with no internal gaps, so tuned parameters should 
	# keep it intact while still marking sparse outlier points as noise (label -1).
	extractor = ClusterExtractor(eps=0.1, min_points=10)
	extractor.process(sample_point_cloud)

	assert len(set(extractor.labels)) > 1

def test_preserves_main_structure_as_single_cluster(sample_point_cloud):
	extractor = ClusterExtractor(eps=0.1, min_points=10)
	extractor.process(sample_point_cloud)

	real_clusters = set(extractor.labels) - {-1}
	assert len(real_clusters) == 1
