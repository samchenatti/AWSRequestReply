# Async request-reply prototype

A simple prototype for a multi-tenancy, async request/reply system, as shown in the figure:

<img src="resources/architecture.png" />

To avoid AWS expenses we run both the Requester and Replier applications locally.
ElasticCache also have been replaced by [Redis running in Docker](https://hub.docker.com/_/redis).