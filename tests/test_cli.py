"""
Tests for Ludwig CLI
"""

import pytest
import subprocess
import tempfile
import os
import shutil


class TestCLI:
    """Test CLI commands."""
    
    def test_version(self):
        """Test ludwig version command."""
        result = subprocess.run(
            ["python", "-m", "ludwig.cli", "version"],
            capture_output=True,
            text=True,
        )
        assert "Ludwig" in result.stdout or result.returncode == 0
    
    def test_new_project_basic(self):
        """Test creating basic project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = os.path.join(tmpdir, "test-project")
            
            result = subprocess.run(
                ["python", "-m", "ludwig.cli", "new", project_path, "--template", "basic"],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
            
            # Check app.py created
            assert os.path.exists(os.path.join(project_path, "app.py"))
            assert os.path.exists(os.path.join(project_path, "requirements.txt"))
            assert os.path.exists(os.path.join(project_path, "README.md"))
    
    def test_new_project_api(self):
        """Test creating API project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = os.path.join(tmpdir, "api-project")
            
            result = subprocess.run(
                ["python", "-m", "ludwig.cli", "new", project_path, "--template", "api"],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
            
            assert os.path.exists(os.path.join(project_path, "app.py"))
            
            # Check API template content
            with open(os.path.join(project_path, "app.py")) as f:
                content = f.read()
                assert "Model" in content
                assert "@app.get" in content
    
    def test_new_project_robot(self):
        """Test creating robot project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = os.path.join(tmpdir, "robot-project")
            
            result = subprocess.run(
                ["python", "-m", "ludwig.cli", "new", project_path, "--template", "robot"],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
            
            assert os.path.exists(os.path.join(project_path, "app.py"))
            
            with open(os.path.join(project_path, "app.py")) as f:
                content = f.read()
                assert "Robot" in content
