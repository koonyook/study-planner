python manage.py dumpdata core.Course --format yaml --indent 2 > yaml/Course.yaml
python manage.py dumpdata core.Field --format yaml --indent 2 > yaml/Field.yaml
python manage.py dumpdata core.Group --format yaml --indent 2 > yaml/Group.yaml
python manage.py dumpdata core.Institution --format yaml --indent 2 > yaml/Institution.yaml
python manage.py dumpdata core.Subject --format yaml --indent 2 > yaml/Subject.yaml