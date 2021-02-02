FROM jupyter/scipy-notebook

ENV JUPYTER_ENABLE_LAB=1

WORKDIR /project

COPY requirements.txt /project/requirements.txt
COPY --chown=jovyan:users config/start.py /home/jovyan/.ipython/profile_default/startup/start.py

RUN pip install -r requirements.txt

EXPOSE 8888
