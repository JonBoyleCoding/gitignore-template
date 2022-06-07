from gitignore_template import typer_main
from github import Github
import pytest


@pytest.mark.parametrize("project_type", [
    "python",
    "c++",
    "godot",
    "visualstudio",
])
def test_get_potential_filenames_palindrome(project_type: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	gitignore_files, levenshtein_distances, min_distance_files = typer_main.get_potential_filenames(project_type, repo)

	assert len(min_distance_files) == 1
