from git import Repo
import os

os.chdir('https://github.com/Huonghtdn/airflow_covid/blob/main')

PATH_OF_GIT_REPO = "https://github.com/Huonghtdn/airflow_covid/blob/main"+'/.git'
COMMIT_MESSAGE = 'Daily update'

def git_push():

    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add('--all')
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()


git_push()
