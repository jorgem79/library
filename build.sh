## Build Backend 
cd backend
docker build -t backend:latest .

## Build Frontend 
cd ../frontend
docker build -t frontend:latest .


## Testing 
#http://127.0.0.1:5001/books


## Remove all containers 
docker rm -f $(docker ps -q)

## Runing backend
docker run -d -p 5001:5001 --name backend-container backend:latest

## Running Frontend
docker run -d -p 8080:80 --name frontend-container frontend:latest


## running docker registry local 
#docker run -d -p 5003:5000 --restart=always --name registry registry:2
##Verify registry 
#curl http://127.0.0.2:5003/v2     

##Tagging 
# docker tag backend:latest 127.0.0.2:5003/backend:latest 

# Pushing 
#docker push 127.0.0.2:5003/backend:latest   

# port forward 
# kubectl port-forward backend-676457d459-kl8z8 5001:5001 -n library
