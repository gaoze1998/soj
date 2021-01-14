# soj
simple online judge
## quick start
1. sudo apt install python3 python3-pip mysql-server
2. pip3 install django djangorestframework mysqlclient
3. python3 manage.py makemigrations
4. python3 manage.py migrate
5. python3 manage.py createsuperuser --user admin
6. You can check soj/urls.py for routes, soj/oj/views.py for HTTP handlers.(This is not a command!)
7. python3 manage.py runserver 0.0.0.0:8080
8. You can use postman to test api.(This is not a command!)
## project structure
1. code: user upload directory.
2. sample: problem sample directory.
3. soj/urls.py: routes.
4. soj/oj/views.py: controller.
5. soj/oj/models.py: app models.
6. soj/oj/permissions.py: controller accessing permissions.
7. soj/oj/utils/judge.py: main judge function.
8. libfakelib.so: fake system call dynamic library which contains fake fork(), clone(), execv(), etc. check libfakelib.c for details.
9. libsojsandbox.so: deprecated. check libsojsandbox.c for details.
## sandbox dev log
1. Use libseccomp to disable some system calls. Python had to load dynamic library to use sandbox. Also it's too expensive to use this tech here.
2. Use LD_PRELOAD to enable fake system calls which do nothing. See *Computer Systems: A Programmer's Perspective (3rd Edition) Randal E.Bryant / David O'Hallaron*  for details.
