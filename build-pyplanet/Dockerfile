FROM python:3.8-bookworm

# docs: https://pypla.net/en/latest/intro/configuration.html

# update & install packages
RUN apt-get update -yq && apt-get install -yq mariadb-client

# create server user
ENV HOME=/home/server
ENV PYPLANET_HOME=/home/server/pyplanet
RUN mkdir -p $HOME && groupadd server && useradd -g server server \
    && mkdir -p $PYPLANET_HOME

# copy server scripts
WORKDIR $PYPLANET_HOME
COPY run.sh .

# copy pyplanet files
ADD pyplanet $PYPLANET_HOME

# change permissions before switching user
RUN chown -R server:server $HOME
RUN chmod +x $PYPLANET_HOME/manage.py
RUN chmod +x $PYPLANET_HOME/run.sh

# switch to server user
USER server
ENV PATH="${PATH}:/home/server/.local/bin"

# install python dependencies
RUN pip3 install --user -r $PYPLANET_HOME/requirements.txt \
    && mkdir -p $PYPLANET_HOME/tmp $PYPLANET_HOME/logs

# start server
CMD ["./run.sh"]
