## Solution details:

1. Run docker-compose.yml to add API_KEY to environment variable. We can also take off key value from docker-compose.yml file and give the value while running 'docker-compose run -e API_KEY=*****'
2. I tried to provide a good UI experience but I didn't add any advanced UI experience since I am not a Front end expert.
3. For ideal production ready code, json files should live on a cloud location like S3/google drive or in Database. I don't have resources to support that on my home machine.
 I will use Boto3 to connect to S3 bucket and access files



Run docker built and docker-compose up command to run docker container.
 >> docker build -t openapp .
 >> docker-compose up -d
