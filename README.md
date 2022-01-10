# Trojan Scheduler

## About

Trojan Scheduler lets users input in the classes they're interested in registering and return a list of possible combination of classes they can take with minimum amount of conflicts

## Commands

1. Run Server

- Windows:
  - run `./run-server.bat`
- Mac:
  - run `./run-server.sh`

## Getting Started

1. Install Python3 from [here](https://www.python.org/downloads/)
2. Install `virtualenv` from [here](https://pypi.org/project/virtualenv/) -- this allows us to create a virtual environment which will ensure us to be all using the same packages. Think of it as a simple version of virtual box or docker. So any packages you install (as long as your virtual environment) is activated will only live inside it (if you delete the virtual environment, it'll get deleted as well). This also makes it easy so your computer isn't filled with a bunch of random libraries and junk you won't need :)
3. Install PostgreSQL from [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
   - You can just install all the components
   - When it asks for password make sure you remember it! We'll be using this for our root access for the db
   - After installing Postgres, you can just close when it asks if you wanna launch StackBuilder
4. Create virtual environment
   - Windows:
     - `python -m venv env`
   - Mac:
     - `python3 -m venv env`
5. Activating your virtual environment
   - Windows:
     - `env\Scripts\activate.bat`
   - Mac:
     - `source env/bin/activate`
6. Installing dependencies -- this will install all the dependencies to your virtual environment
   - `pip install -r requirements.txt`
7. Setting up pre-commit
   - run `pre-commit install` to set up git hook scripts
     - what this does is it runs the the scripts specified in `.pre-commit-config.yaml` whenever you commit so it formats the code nice and beautiful so it's consistent across everyone
   - then run `pre-commit run --all-files` to make sure it works properly

## Tech Stack

Backend: Django

Frontend: Django HTML

## Recommended Stuff

- Code Editor: VSCode or PyCharm (I'm used to using VSCode)
  - If you're using VSCode these are the extensions I recommend:
    - Django by Baptiste Darthenay - cuz we using Django
    - Git History by Don Jayamanne - lets you see git commit history in vscode
    - GitLens by GitKraken - so you know who wrote which big brain code
    - MagicPython by MagicStack - see below
    - Pylance, Python, VS IntelliCode by Microsoft - tbh idk which is better i just have them all lol
    - Cucumber by Alexander Krechik - for writing tests so we become Test Driven Development
    - Code Spell Checker by Street Side Software - helps prevent whoopsies of spelling wrong variable names
    - vscode-icons by VSCode Icons Team or Material Icon Theme by Philipp Kief (prettier icons for your code editor)
- [SourceTree](https://www.atlassian.com/software/sourcetree) - git GUI if you don't wanna deal with terminal stuff
- [iTerm2](https://iterm2.com/) - A better terminal (Note: Mac OS Only)
- [Postman](https://www.postman.com/) - Test out APIs
- [Powerlevel10k](https://github.com/romkatv/powerlevel10k) - Makes terminal better (Note: Unix terminals only)

## Resources

Below are some good resources to refer to

### Backend

- [Learn Basic Django](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)
  - Get started with learning Django
- [Learn Basic Django REST framework](https://www.django-rest-framework.org/tutorial/quickstart/)
  - Get started with learning Django REST framework
- [Two Scoops of Django](resources/Two%20Scoops%20of%20Django.pdf)
  - Outlines some best practices of Django
- [Django Documentation](https://docs.djangoproject.com/en/4.0/)
  - Understand how Django works
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
  - We're gonna be developing our web app using REST practices this allows us to do that. Read more about REST [here](https://en.wikipedia.org/wiki/Representational_state_transfer)
- [Django Filter](https://django-filter.readthedocs.io/en/latest/)
  - Lets user to filter the querysets dynamically form
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
  - Gonna scrape USC class schedules website with this

### Frontend

- [Django Templates](https://www.geeksforgeeks.org/django-templates/)
  - We'll be using Django Templates to build out our frontend
- [Bootstrap](https://getbootstrap.com/)
  - We're gonna be using bootstrap to help create our frontend
- [How to Center in CSS](http://howtocenterincss.com/)
  - nuff said
- [Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
  - In the event you don't wanna use bootstrap
- Icons
  - [System UI Icons](https://systemuicons.com/)
  - [Feather Icons](https://feathericons.com/)
  - [Bootstrap Icons](https://icons.getbootstrap.com)
  - [Flat Icons](https://www.flaticon.com/)

### Git

- [Oh Shit, Git!?!](https://ohshitgit.com/)
  - Common git stuff to undo mistakes
- [Git Rebase](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
  - Makes our git flow more linear
