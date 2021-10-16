FROM python:3.9 as base

RUN mkdir /bot && \
  useradd --create-home --shell /bin/bash bot && \
  chown -R bot:bot /bot

USER bot

WORKDIR /bot

COPY --chown=bot:bot ./requirements.txt ./

RUN pip install -r requirements.txt

COPY --chown=bot:bot . ./

CMD ["python", "main.py"]

FROM base as dev

ENV PATH="/home/bot/.local/bin:${PATH}"

RUN pip install py-mon colorama watchdog

CMD ["pymon", "main.py"]
