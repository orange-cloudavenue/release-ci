import argparse
import os
import subprocess

def write_template(file_to_write, template_file):
    try:
        new_file = open(file_to_write, "a")
        new_file.close()
        new_file = open(file_to_write, "w")
        new_file.write(template_file.read())
        new_file.close()
    except Exception as error:
        print("Exeption during configuration file creation")
        raise error

def main():
    """Main function"""
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Setup Changelog")
    parser.add_argument("-p", "--path", type=str, help="Project path", default=None, required=True)

    # Initialize arguments
    arguments = parser.parse_args()
    parent_dir = arguments.path
    if not parent_dir:
        return

    # Step 1 - Changelog folders
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
    p = subprocess.Popen(['git', 'submodule', 'add', '--name', '.ci', 'https://github.com/FrangipaneTeam/release-ci', '.ci'], cwd=parent_dir)
    p.wait()

    # Step 3 - changelog configuration
    generate_changelog = parent_dir + ".github/workflows/generate_changelog.yml"
    if not os.path.exists(generate_changelog):
        try:
            template_generate_changelog = open('template_generate_changelog.yml', 'r')
            write_template(generate_changelog, template_generate_changelog)
            template_generate_changelog.close()
        except Exception as error:
            raise error

    # Step 4 - Release configuration
    release = parent_dir + ".github/workflows/release.yml"
    if not os.path.exists(release):
        try:
            template_release = open('template_release.yml', 'r')
            write_template(release, template_release)
            template_release.close()
        except Exception as error:
            raise error

    # Step 5: CHANGELOG.md
    tag_version = None
    git_repository = parent_dir + ".git"
    if os.path.exists(git_repository):
        try:
            changelog_process = subprocess.run(["git", "describe", "--abbrev=0", "--match='v*.*.*'", "--tags"], stdout=subprocess.PIPE ,cwd=parent_dir)
            process_message = changelog_process.stdout
            if process_message:
                tag_version = process_message
        except subprocess.CalledProcessError as e:
             print(e.returncode, e.output)
        except Exception as e:
            print("Exception during git describe tag execution")

    changelog = parent_dir + "CHANGELOG.md"
    if not os.path.exists(changelog):
        f = open(changelog, "w", encoding="utf-8")
        if not tag_version:
            f.write('## 0.0.1 (Unreleased)')
        else:
            tag_version = '## ' + tag_version + ' (Unreleased)'
            f.write(tag_version)
        f.close()
    print("Changelog sucessfully added")


if __name__ == "__main__":
    main()
