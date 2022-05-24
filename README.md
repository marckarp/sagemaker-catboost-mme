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
