from gitignore_template import typer_main
from github import Github
import pytest


@pytest.mark.parametrize("project_type,gitignore_filename", [
    ("python", "Python"),
    ("c++", "C++"),
    ("godot", "Godot"),
    ("visualstudio", "VisualStudio"),
])
def test_get_potential_filenames_palindrome(project_type: str, gitignore_filename: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	gitignore_files, levenshtein_distances, min_distance_files = typer_main.get_potential_filenames(project_type, repo, "")

	assert len(min_distance_files) == 1
	assert min_distance_files[0][0] == gitignore_filename + ".gitignore"

def test_get_potential_filenames_global(project_type: str, gitignore_filename: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	gitignore_files, levenshtein_distances, min_distance_files = typer_main.get_potential_filenames(project_type, repo, "Global")

	assert len(min_distance_files) == 1
	assert min_distance_files[0][0] == gitignore_filename + ".gitignore"

def test_get_potential_filenames_community(project_type: str, gitignore_filename: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	gitignore_files, levenshtein_distances, min_distance_files = typer_main.get_potential_filenames(project_type, repo, "Community")

	assert len(min_distance_files) == 1
	assert min_distance_files[0][0] == gitignore_filename + ".gitignore"
