# Kubernetes Sandbox
Simple system to experiment with Kubernetes, Skaffold and friends  



## Components  

### Lotr-Quotes
Is a simple Node.js Express service giving a random quote out of 50 "Lord Of The Rings" quotes.   
Runs on port `8080`.


| route | purpose |
| --- | --- |
| GET: /quote | returns `JSON: {quote, author}` |
| GET: /ready | returns `JSON: {ready}` to indicate if ready to serve |


### Python-Starter
Is a simple Python Flask service checking if the other service is ready (and pretends to be starting it).  
Runs on port `5000`.


| route | purpose |
| --- | --- |
| GET: / | returns `TEXT: <whether ready or not message>` |

### Message-Writer
Is a simple Python Flask service that publishes the received messages to the `rabbitmq` service.


| route | purpose |
| --- | --- |
| POST: /publish | for JSON input: `'{"food": "<your food>"}'` publishes the content to the queue of topic `food` |

### Message-Worker
A listening process that waits for the incoming messages from the `rabbitmq`.  
Is not a service, but a running pod. Replicated to `5 (maybe different number)` instances.  

### Job-Worker
Is a `Job` container performing some action on the supplied job.  
Expects the job suppied as an environment variable `MY_JOB_ITEM`.  
 

| env_key | value | operation |
| --- | --- |
| `MY_JOB_ITEM` | `string: <any string value>` | simply reverses the supplied item and writes the result to the console. |



## Infrastructure

### Skaffold
> _Disclaimer: use `Skaffold v0.23.0` while `sync` issues are not solved_.  

The definition for the Skaffold project is described in `skaffold.yaml`.  
It uses the `file-sync` option to update container code without rebuilding.  
Important to notice, that for the `sync` option the mapping should correspond to the `WORKDIR` of the associated `DockerFile`

```
# in skaffold.yaml
...
build:
  artifacts:
  - image: gcr.io/k8s-skaffold/lotr-quotes
    context: ./lotr-quotes/
    sync:
      '**/*.js': /usr/src/app
...

# ~~

# in ./lotr-quotes/Dockerfile
...
WORKDIR /usr/src/app
...
```

### Rabbitmq
The deployment of a [`rabbitmq`](https://www.rabbitmq.com/) service is described in `./insfrastructure/rabbitmq/k8s/deployment.yaml`.  

