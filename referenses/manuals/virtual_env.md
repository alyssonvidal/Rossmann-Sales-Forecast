### Softwares and Tools Required###

1. [Github Account](https://github.com)
2. [Heroku Account](https://heroku.com)
3. [VS Code](https://code.visualstudio.com)
4. [GitCLI](https://git-scm.com/)

Create a virtual environment on Anaconda

    conda create -p venv python==3.7 -y

Create a virtual environment on Power Shell:

    py -3 -m venv .venv
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    .venv\scripts\activate


Installing python libraries on virtual .env

    pip install -r requirements.txt

Send files to github

    git config --global user.name
    git config --global user.email
    git add . 
    git status
    git commit -m "First Commit"
    git push origin main




