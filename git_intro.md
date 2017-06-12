# Introduction to using Git and GitHub

## Overview

The goal of this introduction is to provide enough background to use github for code development and collaboration.

Git is very flexible; this introduction makes a lot of idiosyncratic decisions. You can assume that 
any of those decisions can be changed to suit your needs.s

### Advantages

* Source code control
* Personal backup
* Collaboration
* Sharing

### git concepts

Git is a distributed version control system.

Repository

Local working copy

Commit

Remote - typically called origin

Clone

Branch 

Tag

### GitHub concepts

Github is a cloud-based git repository.

* Teams
* public vs. private repository
* pull requests


## Set up for using Github


### install a git client

You can find lots of references on the internets.

Edit your local git configuration

* choose an editor
In the examples below, replace 'edit' with command of your choice.

Experiment with some dummy repos

### create a github account

Use your cdw email

https://github.com/

* Contact Brad to to join the cdwlabs team

* Set up SSH keys 
Generate RSA public/private keys
@github:  <avatar> > Settings > SSH and GPG keys
  New SSH Key

* verifiy your keys
  ssh -T git@github.com 

* verify you can access a repo

git clone git@github.com:cdwlabs/<REPO>.git

ls -l <REPO>



## Create a personal repo 

Anybody with a github account can create multiple 'personal' repos for free. Note that these repos will be visible to the world.

In this example we assume that 
* your github user name is 'johndoe'
* GIT ==  the root directory for all your git repos
* DEV == the root the directory for your development work on your local machine
* you have some existing code for a project named 'alpha', in the directory DEV/alpha, and you want o move this to a github repo.
* 'edit' is your favorite editor (which is of course vim, obviously).

pro: keep artifacts from polluting repo
con: requires an extra 'build' step, e.g. in makefile
  (but you'll probably need to do that anyway in a production seting)

### Considerations

Before creating the repo, think about the naming conventions for files, directory structure, functions,
commit messages, issue tracking, tags,...

This is especially important if you're collaborating with other users. 

Its possible to change these after the repo is created, but you can save youreslf some grief by planning ahead.

NOTE: before commiting any files, make sure there NO PASSWORDS or other sensitive information in your files.

If neccesary, refactor your code so that any credentials, user names, etc. are kept in config files or environment variables separate from your code.

### directory structure

For a project 'alpha', you might have the following sub-directories

* docs 
* examples 
* tests 
* build -scripts for installing, compiling, etc.  e.g. makefile, Ansible, Puppet...
* alpha - the actual project code


It might be helpful to peruse other repos on GitHub.


### Create

Create a personal repository, 'alpha', on GitHub, with a simple README.md file

Log in to github 
create new repo, with name 'alpha'
(x) initialize with README

GitHub provides a handy cheat sheet for initializing your repo.

Create a working copy on your local machine.
> cd GIT
> git clone git@github.com:johndoe/alpha.git
> cd alpha
> git status

Make your first commit

> edit README.md  ( add some more text here)
> git commit README.md -m "my first commit"
> git push

Verify that your update is reflected on Github

### Branching

Branching is your friend. Create a branch, 'develop', for beta development

> git checkout -b develop
> copy DEV/alpha/{some files} .
> git commit . -m "I added some files"
> git push

Verify that the github site has those files.

lather, rinse, repeat


## Collaborate

The general approach to colloborating with multiple developers is that each developer 
works on a separate branch ( or branches). When that branch is ready, the developer creates
a pull request. The Committers (who may be identical with the developers) then approve and
merge that pull request.

### Forking

### As contributurs

For a person repo, other users can be added as "contributors" to that repo.  Those users can then create a 
pull requests from a new feature branch

dev2> git clone git@github.org:johndoe/alpha.git
dev2> cd alpha
dev2> git checkout -b  dev2stuff
dev2> edit newfiles
dev2> git add newfiles
dev2> git commit newfiles -m "files from dev2"
dev2> git push --set-upstream origin dev2stuff


@github

Create pull request
develop > deldevstuff



## Creating a CDW labs repo

As a member of the cdwlabs organization, you can also have private repos. 

Contact Brad to create CDW Labs repo. You will need to provide
* the name of the repo
* the members of the 'committers' team
* whether it should public or private


## Workflow

### branching

Branching is very powerful, and potentially confusing.

* git flow model
I like to use the git-flow model:
http://nvie.com/posts/a-successful-git-branching-model/

You can install code to simplify the commands: 
   https://danielkummer.github.io/git-flow-cheatsheet/

But that isn't neccesary. In this example we'll use the model w/o the git-flow commands.

* create branch locally, and on remote
git checkout -b develop
git push --set-upstream origin develop

git branch -a -vv

* do some work

edit /test / edit /test
git diff
git commit . -m MESSAGE
git push

git status

* merge

Make sure develop is clean:

git status
On branch develop
Your branch is up-to-date with 'origin/develop'.
nothing to commit, working directory clean

Back to the master branch:

git checkout master

Show changes 

git log ..develop

Merge

git merge develop

git status

If all is well:

git push

No go right back to develop to continue working

git checkout develop

### Pull request

A 'pull request' is request ( to another developer, or the 'official committer') to pull your changes into another branch.

Example: 
* create a feature branch
* publish your feature branch
* create pull request to merge your feature branch into develop

@GitHub - developer 1)
 Create Pull request
 base: master
 
 compare: feature_x
 
 Once again: write good messages!
 
 Add Reviewers

@GitHub - Reviewer
  write message
  merge pull request
  (optionally - delete branch )

* developer, locally
git checkout develop

Get the updates from remote:

git fetch

Show the list of new commits

git log ..origin/develop
 
Pull in those changes locally

git pull

### tagging

A handy way to keep track of versions, etc.

git tag  v0.1
git push --tags

Verify @GitHub

## References
https://guides.github.com/activities/hello-world/

http://rogerdudler.github.io/git-guide/

https://discdungeon.cdw.com/vvtwiki/index.php/DDVT/Git






