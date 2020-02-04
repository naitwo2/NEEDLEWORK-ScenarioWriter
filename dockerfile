FROM python:3.7

RUN python -m pip install --upgrade pip 
RUN python -m pip install pandas==0.25.0
ADD ./ /NEEDLEWORK-ScenarioWriter/
ADD ./entrypoint.sh /entrypoint.sh

CMD [ "sh", "./entrypoint.sh"]