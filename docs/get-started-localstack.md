# How to use Localstack with docker (Windows)
This readme explains how to install and localstack with docker. <br>From installing the necessary software to creating a SQS queue.

<h1> Step 1: Install Docker </h1>
If you haven't already, you will need to install Docker on your machine. <br>
You can download the installation package from the Docker website.<br>
[Docker website](https://www.docker.com/products/docker-desktop/)

<h1>Step 2: Start Localstack in Docker</h1>
To start Localstack in Docker, run the following command in your terminal:<br>


```env
docker run --name localstack -p 4566:4566 -e SERVICES=sqs -e DEFAULT_REGION=us-east-1 -e <br> AWS_ACCESS_KEY_ID=localstackdevelopment -e AWS_SECRET_ACCESS_KEY=localstackdevelopment localstack/localstack
```
<br>
This command will download the Localstack image, create a container named "localstack", <br>and start the container with the SQS service enabled.

<h1>Step 3: Install the AWS CLI </h1>
1.	Download the AWS CLI MSI installer for Windows from the AWS website.<br>
2.	Run the MSI installer and follow the instructions to install the AWS CLI.<br>
3.	Open a command prompt or PowerShell window and verify that the AWS CLI is installed correctly by running the following command: aws –version

<h1>Step 4: Configure the AWS CLI</h1>
Before you can interact with Localstack using the AWS CLI, you will need to configure the AWS CLI with your AWS access key and secret access key. Run the following command to start the configuration process:<br>
aws configure<br>
•	AWS access key ID: localstack (Can be anything)<br>
•	Secret access key: secret (Can be anything)<br>
•	Default region name: us-east-1<br>
•	Default output format: json

<h1>Step 4: Create a Queue</h1>
To create a queue, you can use the AWS CLI. In your terminal, run the following command to create a queue named "my-queue". This queue is meant for the events:<br>

```env
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name my-queue
```

run the following command to create a queue named "users-queue". This queue is meant for the sending the users that are created in the powersuite:<br>

```env
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name users-queue
```
This will create a queue named "my-queue" and “users-queue” in Localstack. You will now be able to connect to this queue from cmd or application<br>


<h1>Step 5: Extra (windows cmd commands)</h1>
Listing the queue:<br>

```env
aws --endpoint-url=http://localhost:4566 sqs list-queues --output json
```
Sending a hello world string:<br>

```env
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/my-queue --message-body "Hello, world!" --output json
```
Sending a json file (message.json in this case):<br>

```env
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/my-queue --message-body file://message.json
```
Receiving the message:<br>

```env
aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/my-queue --output json
```








