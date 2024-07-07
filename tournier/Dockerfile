
FROM python:3.11 AS chess-engines-load
WORKDIR /chess_engines
RUN wget -q 'https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar'
RUN tar -xvf stockfish-ubuntu-x86-64-avx2.tar
RUN mv ./stockfish/stockfish-ubuntu-x86-64-avx2 ./
RUN wget https://rofchade.nl/wp-content/uploads/2023/10/wnn_rofChadeLin3.1.zip
RUN unzip ./wnn_rofChadeLin3.1.zip
RUN find ./ -type d -exec chmod 755 {}
RUN chmod 777 rofChadeSSE2

FROM python:3.11 AS poetry-init
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11 AS final
WORKDIR /project
COPY --from=poetry-init /tmp/requirements.txt /project/requirements.txt
COPY --from=chess-engines-load /chess_engines /chess_engines
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt
COPY . .
CMD python3 main.py
