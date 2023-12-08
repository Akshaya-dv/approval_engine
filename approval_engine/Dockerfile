FROM python:3.9
RUN mkdir /ApprovalEngine

WORKDIR /ApprovalEngine/


COPY requirement.txt /ApprovalEngine/
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
COPY . /ApprovalEngine/


CMD python sp_creation.py && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8004

