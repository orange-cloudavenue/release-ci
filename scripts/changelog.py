import argparse
import os
import subprocess

CHANGELOG_GITHUB_TEMPLATE_PATH = ".github/workflows/generate_changelog.yml"
RELEASE_GITHUB_TEMPLATE_PATH = ".github/workflows/release.yml"
CHANGELOG_GITHUB_TEMPLATE_NAME = "template_generate_changelog.yml"
RELEASE_GITHUB_TEMPLATE_NAME = "template_release.yml"


def write_template(file_to_write, template_file):
    """
    Write a template file with the content of a given template file.

    file_to_write {str}: name of the file to create with data.
    template_file {str}: name of the template file to get the data.

    return: None
    """
    try:
        new_file = open(file_to_write, "a")
        new_file.close()
        new_file = open(file_to_write, "w")
        new_file.write(template_file.read())
        new_file.close()
    except Exception as error:
        print("Exeption during configuration file creation")
        raise error


def create_template_file(template_file_path, template_path, template_file_name):
    """
    Create a template file.

    template_file_path {str}:           path of the template
    template_path {str}:                path where we want to create the template
    template_file_name {str}:           name of the template file that we want to create
    """
    if not os.path.exists(template_file_path):
        try:
            template_generate_changelog_path = template_path + template_file_name
            template_generate_changelog = open(template_generate_changelog_path, "r")
            write_template(template_file_path, template_generate_changelog)
            template_generate_changelog.close()
        except Exception as error:
            raise error


def main():
    """Main function"""
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Setup Changelog")
    parser.add_argument(
        "-p", "--path", type=str, help="Project path", default=None, required=True
    )

    # Initialize arguments
    arguments = parser.parse_args()
    parent_dir = arguments.path
    if not parent_dir:
        return

    if not parent_dir.endswith("/"):
        parent_dir += "/"

    curent_dir = os.getcwd()
    template_path = "/".join(curent_dir.split("/")[:-1]) + "/templates/"

    # Step 1 - Changelog folder
    changelog_folder = os.path.join(parent_dir, ".changelog")
    if not os.path.exists(changelog_folder):
        os.mkdir(changelog_folder)

    gitkeep_file = parent_dir + ".changelog/.gitkeep"
    if not os.path.exists(gitkeep_file):
        try:
            file = open(gitkeep_file, "a")
            file.close()
        except Exception as error:
            raise error

    github_folder = os.path.join(parent_dir, ".github")
    if not os.path.exists(github_folder):
        os.mkdir(github_folder)

    parent_workflow = parent_dir + ".github/"
    workflow_folder = os.path.join(parent_workflow, "workflows")
    if not os.path.exists(workflow_folder):
        os.mkdir(workflow_folder)

    # Step 2 - .ci submodule
    ci_process = subprocess.Popen(['git', 'submodule', 'add', '--name', '.ci', 'https://github.com/FrangipaneTeam/release-ci', '.ci'], cwd=parent_dir)
    ci_process.wait()

    # Step 3 - changelog configuration
    template_file_path = parent_dir + CHANGELOG_GITHUB_TEMPLATE_PATH
    template_file_name = CHANGELOG_GITHUB_TEMPLATE_NAME
    create_template_file(template_file_path, template_path, template_file_name)

    # Step 4 - Release configuration
    template_file_path = parent_dir + RELEASE_GITHUB_TEMPLATE_PATH
    template_file_name = RELEASE_GITHUB_TEMPLATE_NAME
    create_template_file(template_file_path, template_path, template_file_name)

    # Step 5: CHANGELOG.md
    tag_version = None
    git_repository = parent_dir + ".git"
    if os.path.exists(git_repository):
        try:
            changelog_process = subprocess.run(
                ["git", "describe", "--tags"], capture_output=True, cwd=parent_dir
            )
            tag_str = changelog_process.stdout.decode("utf-8")
            if tag_str.startswith("v"):
                tag_str = tag_str[1:]
            if tag_str:
                tag_version = tag_str
        except subprocess.CalledProcessError as e:
            print(e.returncode, e.output)
        except Exception as e:
            print("Exception during git describe tag execution: %e", e)

    changelog = parent_dir + "CHANGELOG.md"
    if not os.path.exists(changelog):
        f = open(changelog, "a")
        f.close()
        f = open(changelog, "w")
        if not tag_version:
            f.write("## 0.0.1 (Unreleased)")
        else:
            tag_version = "## " + tag_version[:-1] + "(Unreleased)"
            f.write(tag_version)
        f.close()
    print("Changelog sucessfully added")


if __name__ == "__main__":
    main()
