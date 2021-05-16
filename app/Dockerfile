FROM centos:8

WORKDIR /app/

COPY dist/helloworld-*.tar.gz .

RUN yum install python3 -y;\
    pip3 install gunicorn;\
    tarball_name=`ls helloworld-*.tar.gz`;\
    pip3 install $tarball_name;

EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "helloworld:create_app()"]
    