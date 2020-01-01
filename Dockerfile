# ---------------------------------------------------------------
# Dockerfile for exsimo
# ---------------------------------------------------------------
# Build image from `Dockerfile`
#   docker build -t matthiaskoenig/exsimo:${EXSIMO_VERSION} .
#
# Images are build automatically on dockerhub after merging in
# master.
#
# The image is pushed to dockerhub
#   docker login
#   docker push matthiaskoenig/exsimo:${EXSIMO_VERSION}
# ---------------------------------------------------------------
FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
RUN pip install pip setuptools --upgrade
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds application code to the image
COPY . /code
WORKDIR /code

# install pkexsimo
RUN pip install -e .

# run all tests
RUN pytest

# execute workflow
RUN execute

CMD ["/bin/bash"]