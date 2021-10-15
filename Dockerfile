FROM python:3.9

RUN mkdir /bot && \
  useradd --create-home --shell /bin/bash bot && \
  chown -R bot:bot /bot

USER bot

WORKDIR /bot

COPY --chown=bot:bot ./requirements.txt ./

RUN pip install -r requirements.txt

COPY --chown=bot:bot . ./

CMD ["python", "main.py"]
