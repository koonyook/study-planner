python manage.py dumpdata core.Subject --format yaml --indent 2 > fixtures/Subject_.yaml
python manage.py datamigration core update_prerequisite