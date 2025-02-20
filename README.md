# Weather App

A full-stack weather application that fetches and displays historical weather data based on user input.

## Features
- Fetches average temperature data for a specified city and number of days.
- FastAPI backend to retrieve weather data from a third-party API.
- Next.js frontend to display weather information.
- Dockerized setup for easy deployment.

---

## 🚀 Setup Instructions

### Prerequisites
Make sure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clone the Repository
```sh
git clone https://github.com/peijiunchong/weather-app.git
cd weather-app
```

### Running the Application with Docker
```sh
docker-compose up --build
```
This will:
- Build and start the **backend** (FastAPI) on `http://localhost:8000`
- Build and start the **frontend** (Next.js) on `http://localhost:3000`

### Stopping the Application
```sh
docker-compose down
```

---

## 🖥️ API Documentation

### Base URL
```
http://localhost:8000
```

### **1️⃣ Get Average Temperature**
Fetches the average temperature for a given city over a specified number of days.

**Endpoint:**
```
GET /weather/average?city={city}&days={days}
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `city`    | `string` | Name of the city |
| `days`    | `integer` | Number of days |

**Example Request:**
```
GET /weather/average?city=London&days=7
```

**Example Response:**
```json
{
  "average_temperature": 15.2
}
```

**Error Responses:**
```json
{
  "detail": "Invalid city name"
}
```


