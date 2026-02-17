Commit & Push page: select account, repo, branch, multiple files; preview uploads/<filename>; run pipeline (one commit + push per file).
"""
import os
import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QProgressBar,
)
from PySide6.QtCore import Qt, QThread, Signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.store_json import (
    read_json,
    write_json,
    get_workspace_path,
    get_logs_dir,
)
from core.secrets import get_token
from core.github_api import get_repos
from core.path_policy import clean_filename, resolve_upload_path, ensure_upload_dir
from core.git_ops import clone_repo, checkout_branch, add_commit_push


def _runs_data() -> list:
    return read_json("runs.json")


def _append_run(entry: dict) -> None:
    data = _runs_data()
    data.append(entry)
    write_json("runs.json", data)


class _LoadReposWorker(QThread):
    result = Signal(object)

    def __init__(self, token: str, parent=None):
        super().__init__(parent)
        self.token = token

    def run(self):
        self.result.emit(get_repos(self.token))
