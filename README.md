# Docker development

## Step 0 - Prerequisites

1. You have [docker](https://docs.docker.com/get-docker/) installed on your local machine
2. Make sure docker is running
3. Make sure that PowerSuite is running
4. You have setup the LocalStack container using the - [Docs](/READMELOCALSTACK.md)

## Step 1 - Setup `.env` files

There are 2 env file that you have to set up before building and running the docker containers. 

- Root: `.env`
  - Used by `docker-compose.yml` to build and run docker containers
- db: `db/db.env`
  - Used by the backend for credentials
  - [Docs](./envs/server-app.md)

In each of these directories there is an `.env.example`, duplicate it and rename it to `.env` and fill in each of the variables described in the env file.

## Step 2 - Build the docker image

Now that all of the environment variables have been set, you can build the image. If you set the environment variables correctly it should build without any issues.

1. Open a terminal in the root of the project
2. Execute command `docker-compose build`

*Note: If it the variables are correct, but it is giving errors, add the `--no-cache` argument to the build command*

## Step 3 - Running the docker container

If the container images are built correctly and the environment variables are set, you can execute:

- `docker-compose up -d`

*Note: the `-d` flag is used to detatch the running containers from the current terminal*
