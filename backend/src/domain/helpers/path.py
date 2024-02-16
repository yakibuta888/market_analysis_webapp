from pathlib import Path


def get_project_root() -> Path:
    current_file = Path(__file__).resolve()
    project_root_marker = 'requirements.txt'
    project_root = current_file.parent
    while str(project_root) != str(project_root.root):
        if (project_root / project_root_marker).exists():
            break
        project_root = project_root.parent
    return project_root
