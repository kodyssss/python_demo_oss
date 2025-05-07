FROM m.daocloud.io/docker.io/python:3.8-slim-buster                

WORKDIR /app

COPY . /app



RUN mkdir -p /root/.pip && echo "[global]\ntrusted-host =  pypi.tuna.tsinghua.edu.cn\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > /root/.pip/pip.conf
RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "run.py"]