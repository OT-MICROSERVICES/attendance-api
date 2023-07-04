<p align="center">
  <img src="./static/attendance-api-logo.svg" height="330" width="330">
</p>

Attendance REST API is a python based microservice which is responsible for all the attendance related transactions in the [OT-Microservices](https://github.com/OT-MICROSERVICES). This application supports cross-platform, the only thing will be required to run this application is python runtime modules.

Supported features of the application are:-

- Flask based web framework for all REST related transactions
- PostgresSQL as a primary database for storing all the attendance records
- Redis as cache management middleware for storing all API response
- Prometheus and open-telemetry metrics supports for monitoring and observability
- Swagger integration for API documentation of all endpoints
