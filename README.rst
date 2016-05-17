===================
 Django Lab
===================

 .. image:: https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat
   :target: https://gitter.im/DhiaTN/djangolab
   :alt: Chat Room

 .. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://raw.githubusercontent.com/DhiaTN/djangolab/master/LICENSE
   :alt: Project Licence

 .. image:: https://requires.io/github/DhiaTN/djangolab/requirements.svg?branch=master
   :target: https://requires.io/github/DhiaTN/djangolab/requirements/?branch=master
   :alt: Requirements Status


I’ve been spending some time doing researches on how best work with django and improve my code performance. Then I did a bit of testing myself and decided to put it all together in a project for future’s sake and as a sample that showcases some django features and good practices.
Any suggestions, comments and/or contributions are more than welcome.


Technology Stack
----------------

- Python 2.7
- Django 1.9+
- PostgreSQL 9.4+
- Fabric
- Docker


Setup
------

- Install Docker

    https://docs.docker.com/installation/

- Install Docker Compose

    http://docs.docker.com/compose/install/

    To run any command inside the Django Docker container, simply prepend ``docker-compose run web``.

- Run the Django database migrations

    ``:~$ docker-compose run web python manage.py migrate``

- Start the Docker containers

    ``:~$ docker-compose up -d``

    This will start the containers in the background.


