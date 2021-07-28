from git import Repo
import os

os.chdir(YourGithubPageDirectoryPath)

PATH_OF_GIT_REPO = YourGithubPageDirectoryPath/.git'
COMMIT_MESSAGE = 'Daily update'

def git_push():

    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add('--all')
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()


git_push()