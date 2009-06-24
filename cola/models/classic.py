import os

from cola import utils
from cola.models.main import MainModel


class ClassicModel(MainModel):
    """Defines data used by the classic view."""
    message_paths_staged   = 'paths_staged'

    def __init__(self):
        MainModel.__init__(self)
        self.use_worktree(os.getcwd())
        self.update_status()

    def stage_paths(self, paths):
        """Adds paths to git and notifies observers."""
        self.update_status()
        self.git.add('--', *paths)

        paths = set(paths)

        # Grab the old list of modified files
        old_modified = set(self.modified)

        # Rescan for new changes
        self.update_status()

        # Handle 'git add' on a directory
        new_modified = set(self.modified)
        newly_staged = utils.add_parents(old_modified - new_modified)

        for path in newly_staged:
            paths.add(path)

        self.notify_message_observers(self.message_paths_staged, paths=paths)

    def everything(self):
        """Returns a sorted list of all files, including untracked files."""
        files = self.all_files() + self.untracked
        files.sort()
        return files
