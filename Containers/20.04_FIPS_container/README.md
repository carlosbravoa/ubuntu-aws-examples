# FIPS Container.

A FIPS basic container that checks kernel on worker nodes and FIPS libraries.
If the worker nodes are running on FIPS mode, it will detect it and display a message.

Based on [Create FIPS-enabled Ubuntu container images with 10-year security updates](https://ubuntu.com/blog/fips-ubuntu-container-security-updates) tutorial


## How to build it

To build the container, you need to add your token in the `ua-attach-config.yaml` file
and build it with:

```
sudo DOCKER_BUILDKIT=1 docker build . --secret id=ua-attach-config,src=ua-attach-config.yaml -t ubuntu20.04-fips
```


## How to deploy it

We have included a sample deployment.yaml file for Kubernetes
