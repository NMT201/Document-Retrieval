# Document-Retrival

## Run systems
```
bash ./script/run.sh
```

## Build docker image
```
docker build -t docrev .
```
## Run container
```
docker run -it -p 8051:8051 --runtime=nvidia --gpus alls docrev
```
