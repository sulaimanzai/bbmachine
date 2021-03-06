FROM alpine:3.10

RUN apk --no-cache add  python3 \
                        git \
                        go \
                        musl-dev \
                        postgresql-dev \
                        python3-dev

RUN pip3 install gunicorn

RUN mkdir /home/go

ENV GOPATH="/home/go"
ENV PATH="${PATH}:${GOPATH}/bin"

RUN go get -u github.com/tomnomnom/assetfinder

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "bbmachine.wsgi"]

