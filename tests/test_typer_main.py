import unittest.mock
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

@pytest.mark.parametrize("project_type,gitignore_filename,directory", [("python", "Python", ""), ("python", "Python", "Global"), ("python", "Python", "Community")])
def test_get_potential_filenames_with_directory(project_type: str, gitignore_filename: str, directory: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	gitignore_files, levenshtein_distances, min_distance_files = typer_main.get_potential_filenames(project_type, repo, directory)

	assert len(min_distance_files) == 1
	assert min_distance_files[0][0] == gitignore_filename + ".gitignore"

@pytest.mark.parametrize("directory", ["", "Global", "Community"])
def test_typer_main_with_directory(project_type: str, gitignore_filename: str, directory: str):
	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

 # Call the typer_main function with a project_type, replace argument of GitIgnoreReplaceType.CHOOSE, and a directory argument
 with unittest.mock.patch('typer.confirm', return_value=True):
 	result = typer_main.typer_main("python", typer_main.GitIgnoreReplaceType.CHOOSE, directory=directory)

 # Assert that the function returns 0, which indicates success
 assert result == 0
