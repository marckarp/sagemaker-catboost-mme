## SageMaker CatBoost Multi-Model Endpoint
This repo depicts how to make use of a custom container to host multiple CatBoost models on a SageMaker Multi-Model-Endpoint.

The `catboost-mme.ipynb` contains the steps to build and push the custom image to ECR, deploy the SageMaker Endpoint and make inference against the Multi-Model-Endpoint.

The `container` folder contains the files needed for the custom image. 

```
├── container
│   ├── dockerd-entrypoint.py
│   ├── Dockerfile
│   └── model_handler.py
```

- `dockerd-entrypoint.py` is the entry point script that will start the multi model server.
- `Dockerfile` contains the container definition that will be used to assemble the image. This include the packages that need to be installed.
- `model_handler.py` is the script that will contain the logic to load up the model and make inference.

Benchmarking and load testing:

All tests conducted on a single `ml.m5.xlarge`.	

**1) Uncompressed 569KB model in memory test**
*~470TPS*

End to end:
```
Response time percentiles (approximated)
 Type     Name                                                                              50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|----------------------------------------------------------------------------|---------|------|------|------|------|------|------|------|------|------|------|------|
 custom_protocol_boto3 sagemaker_client_invoke_endpoint                                      30     32     34     35     39     43     50     56     85    280   2100 137879
```

Model Latency (p99) and Invocations (Sum) - 1min:
![metric1](https://github.com/marckarp/sagemaker-catboost-mme/blob/fce2d7eaf36ac10f2cffa147895921d162fd50bc/small-model-hot-metrics.png)
