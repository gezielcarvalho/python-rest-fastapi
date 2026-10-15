# Architecture

## Current shape

```text
HTTP client
    |
    v
FastAPI routes (main.py)
    |
    v
UserController -> User model -> Motor async client -> MongoDB
    |
    +--> Pydantic UserDTO request model
```

## Application flow

`main.py` defines health and user CRUD routes. Requests are typed with `UserDTO`, passed into `UserController`, and persisted through the user model using a Motor MongoDB collection. User identifiers are represented as UUID values and converted to BSON binary values for storage.

## Container topology

The Compose file represents a local FastAPI and MongoDB pair. It is a development convenience, not an approved production topology.

## Configuration boundary

The data model reads one environment variable name for the MongoDB connection string, while the Compose configuration sets a differently named MongoDB URL variable. This documentation records the mismatch only; resolving it requires a separately reviewed configuration change.
