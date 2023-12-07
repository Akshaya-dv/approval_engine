FROM python:3.9
RUN mkdir /ApprovalEngine
WORKDIR /ApprovalEngine
COPY requirement.txt /ApprovalEngine/
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
COPY . /ApprovalEngine/
