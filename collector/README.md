# Collector Microservice

A Clojure microservice for collecting and managing customer decisions with an in-memory database.

## Features

- **In-memory database** for fast data access during development/testing
- **RESTful API** for decision management
- **Schema validation** using Prismatic Schema
- **Component-based architecture** using Stuart Sierra's Component library
- **Comprehensive test coverage** with unit and integration tests

## Data Model

The service manages decision records with the following structure:

```clojure
{:customer-id #uuid "..."                    ; UUID (required)
 :decision-type :application                 ; Enum: :application, :lobby, :registration-base, :registration-complement
 :data-decision {:score 85 :approved true}  ; Map with keyword keys and primitive values
 :created-at #inst "2024-01-01T10:00:00Z"}  ; Timestamp (auto-generated)
```

## API Endpoints

### POST /decisions
Create a new decision record.

**Request Body:**
```json
{
  "customer-id": "550e8400-e29b-41d4-a716-446655440000",
  "decision-type": "application",
  "data-decision": {
    "score": 85,
    "approved": true,
    "reason": "Good credit score"
  }
}
```

**Response (201 Created):**
```json
{
  "customer-id": "550e8400-e29b-41d4-a716-446655440000",
  "decision-type": "application",
  "data-decision": {
    "score": 85,
    "approved": true,
    "reason": "Good credit score"
  },
  "created-at": "2024-01-01T10:00:00.000Z"
}
```

### GET /decisions/:customer-id
Retrieve a specific decision by customer ID.

**Response (200 OK):**
```json
{
  "customer-id": "550e8400-e29b-41d4-a716-446655440000",
  "decision-type": "application",
  "data-decision": {
    "score": 85,
    "approved": true
  },
  "created-at": "2024-01-01T10:00:00.000Z"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Decision not found"
}
```

### GET /decisions
Retrieve all decisions.

**Response (200 OK):**
```json
[
  {
    "customer-id": "550e8400-e29b-41d4-a716-446655440000",
    "decision-type": "application",
    "data-decision": {"score": 85},
    "created-at": "2024-01-01T10:00:00.000Z"
  }
]
```

### GET /health
Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

## Decision Types

The service supports the following decision types:

- `:application` - Application-related decisions
- `:lobby` - Lobby/queue management decisions  
- `:registration-base` - Basic registration decisions
- `:registration-complement` - Complementary registration decisions

## Running the Service

### Prerequisites
- Java 8 or higher
- Leiningen

### Development
```bash
# Install dependencies
lein deps

# Run tests
lein test

# Start the service (default port 3000)
lein run

# Start on custom port
lein run 8080
```

### Production
```bash
# Create uberjar
lein uberjar

# Run the jar
java -jar target/uberjar/collector-0.1.0-SNAPSHOT-standalone.jar [port]
```

## Testing

The project includes comprehensive test coverage:

### Unit Tests
- Model validation tests
- Database component tests  
- Controller logic tests

### Integration Tests
- Full API workflow tests
- End-to-end request/response validation
- Error handling verification

```bash
# Run all tests
lein test

# Run specific test namespace
lein test collector.models.decision-test
lein test collector.integration.api-test
```

## Project Structure

```
src/
├── collector/
│   ├── components/          # Component system
│   │   ├── database.clj     # In-memory database component
│   │   └── webapp.clj       # Web application component
│   ├── controllers/         # Request handlers
│   │   └── decisions.clj    # Decision API handlers
│   ├── models/              # Data models and validation
│   │   └── decision.clj     # Decision record schema
│   ├── components.clj       # System configuration
│   └── core.clj            # Application entry point
test/
├── collector/
│   ├── components/          # Component tests
│   ├── controllers/         # Controller tests  
│   ├── models/              # Model tests
│   └── integration/         # Integration tests
```

## Error Handling

The API provides structured error responses:

- **400 Bad Request** - Invalid UUID format or decision data
- **404 Not Found** - Decision not found
- **500 Internal Server Error** - Unexpected server errors

All error responses follow the format:
```json
{
  "error": "Error description",
  "message": "Detailed error message"
}
```

## Architecture

The service follows functional programming principles and uses:

- **Component System** for dependency injection and lifecycle management
- **Schema Validation** for data integrity
- **Protocol-based Design** for database abstraction
- **Pure Functions** for business logic
- **Immutable Data Structures** throughout

## Development Notes

- The in-memory database resets on service restart
- UUIDs are automatically validated and converted
- Decision types are strictly validated against the enum
- All timestamps use UTC timezone
- Data-decision maps support nested structures with keyword keys

