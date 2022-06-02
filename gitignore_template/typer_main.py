import typer
import sys
import requests
import click

from github import Github
from gitignore_template.utility_functions import levenshtein_distance

def typer_main(project_type: str = typer.Argument(..., help="The programming language/project type"),
			   verbose_check: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")):
	"""
	Download the gitignore template from github.com/github/gitignore into the current directory.
	"""

	# NOTE (JB) Initialize the github client
	g = Github()

	# NOTE (JB) Get the github/gitignore repo
	repo = g.get_repo("github/gitignore")

	# NOTE (JB) Extract all gitignore files from the repo
	gitignore_files = [x.name for x in repo.get_contents("") if x.name.endswith(".gitignore")]
	stripped_gitignore_files = [x.replace(".gitignore", "") for x in gitignore_files]

	# NOTE (JB) Get the levenshtein distance between the user's input and the list of gitignore files
	levenshtein_distances = [levenshtein_distance(project_type, x) for x in stripped_gitignore_files]

	# NOTE (JB) Print the distances and the files
	if verbose_check:
		for file, distance in zip(stripped_gitignore_files, levenshtein_distances):
			print("{} : {}".format(file, distance))

	minimum_distance = min(levenshtein_distances)

	# NOTE (JB) If multiple files have the same minimum distance, ask the user which one they want
	min_distance_files = [(x, idx) for idx, (x, y) in enumerate(zip(gitignore_files, levenshtein_distances)) if y == minimum_distance]

	if len(min_distance_files) > 1:
		typer.echo("Multiple files have the same minimum distance. Please choose one:")
		for idx, (x, _) in enumerate(min_distance_files):
			typer.echo(f"\t{idx}: {x}")

		typer.echo(f"\t{len(min_distance_files)}: Cancel")

		while True:
			option = click.prompt("Please choose one of the above options:", type=int)

			if option == len(min_distance_files):
				return 0
			else:
				break

		closest_match_index = min_distance_files[option][1]
	else:
		closest_match_index = min_distance_files[0][1]

	# NOTE (JB) Get the index of the closest match
	best_match = gitignore_files[closest_match_index]

	# NOTE (JB) If distance is more than 2 characters, ask the user if detected match is correct
	#           (if they haven't already chosen)
	if levenshtein_distances[closest_match_index] >= 2 and len(min_distance_files) == 1:
		if not typer.confirm(f"Best match is {best_match} - do you wish to continue?"):
			typer.echo("Aborting...")
			return 1

	# NOTE (JB) Print the best match
	typer.echo(f"Downloading {best_match}...")

	# NOTE (JB) Download the best match
	contents = repo.get_contents(best_match)

	# NOTE (JB) Save as .gitignore
	with open(".gitignore", "w") as f:
		f.write(contents.decoded_content.decode("utf-8"))

	# NOTE (JB) Print success
	typer.echo("Success!")

	return 0











def main():
	return typer.run(typer_main)


if __name__ == '__main__':
	sys.exit(main())
