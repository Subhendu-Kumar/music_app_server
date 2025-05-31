# Music App API

A FastAPI application with Prisma & NeonDB for managing music collections, user authentication, and favorite songs.

## 🎵 Features

- **User Authentication**: Secure signup and login with JWT bearer tokens
- **Song Management**: Upload, list, and manage songs with metadata
- **Favorites System**: Add/remove songs from personal favorites
- **File Upload**: Support for audio files and thumbnail images
- **Health Monitoring**: Built-in health check endpoints

## 🚀 API Overview

The API is built with FastAPI and provides the following main functionalities:

### Authentication Endpoints

- **POST** `/auth/signup` - Create a new user account
- **POST** `/auth/login` - Authenticate and receive access token
- **GET** `/auth/user` - Get current user information (requires authentication)

### Song Management Endpoints

- **POST** `/song/upload` - Upload a new song with metadata and files
- **GET** `/song/list` - List all available songs
- **GET** `/song/fav` - Get user's favorite songs
- **POST** `/song/fav` - Add a song to favorites
- **DELETE** `/song/fav/{song_id}` - Remove a song from favorites

### Utility Endpoints

- **GET** `/` - Root endpoint
- **GET** `/health` - Health check endpoint

## 📋 API Documentation

### Authentication

#### Sign Up

```http
POST /auth/signup
Content-Type: application/json

{
  "name": "string",
  "email": "user@example.com",
  "password": "string"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "string"
}
```

#### Get User Info

```http
GET /auth/user
Authorization: Bearer <your-token>
```

### Song Management

#### Upload Song

```http
POST /song/upload
Authorization: Bearer <your-token>
Content-Type: multipart/form-data

Form Data:
- artist: string (required)
- song_name: string (required)
- hex_color: string (required)
- song: binary file (required)
- thumbnail: binary file (required)
```

#### List All Songs

```http
GET /song/list
Authorization: Bearer <your-token>
```

#### Get Favorite Songs

```http
GET /song/fav
Authorization: Bearer <your-token>
```

#### Add to Favorites

```http
POST /song/fav?song_id=<song-id>
Authorization: Bearer <your-token>
```

#### Remove from Favorites

```http
DELETE /song/fav/<song-id>
Authorization: Bearer <your-token>
```

## 🔒 Authentication

This API uses **HTTP Bearer Token** authentication. After logging in, include the received token in all authenticated requests:

```
Authorization: Bearer <your-access-token>
```

## 📊 Response Codes

- **200**: OK - Request successful
- **201**: Created - Resource created successfully
- **422**: Validation Error - Invalid request data
- **401**: Unauthorized - Authentication required or invalid token
- **404**: Not Found - Resource not found

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Prisma**: Next-generation ORM for database management
- **NeonDB**: Serverless PostgreSQL database
- **JWT**: JSON Web Tokens for authentication
- **Multipart Forms**: File upload support

## 🚦 Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Prisma Client
- NeonDB account

### Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install fastapi prisma uvicorn python-multipart
   ```

3. Set up your database connection with NeonDB & add `.env`

   ```bash
   # Neon DB
   DATABASE_URL="<your neon db postgresql url>"

   # jwt
   JWT_SECRET=<your secret>
   JWT_ALGORITHM=<algo>
   JWT_EXP_DELTA_SECONDS=<in seconds>

   # Cloudinary
   CLOUDINARY_CLIENT_NAME=<client name>
   CLOUDINARY_CLIENT_API=<client api>
   CLOUDINARY_CLIENT_SECRET=<api secret>
   ```

4. Run Prisma migrations:

   ```bash
   prisma migrate dev
   ```

5. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 File Upload Requirements

When uploading songs, ensure:

- **Audio files**: Supported formats (MP3, WAV, FLAC, etc.)
- **Thumbnails**: Image files (JPG, PNG, etc.)
- **Hex color**: Valid hex color code for UI theming
- **Metadata**: Artist name and song name are required

## 🎨 Color Theming

Each song includes a `hex_color` field that can be used for dynamic UI theming, allowing the app to adapt its color scheme based on the currently playing song.

## 📝 Error Handling

The API returns structured error responses for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🔍 Health Check

Monitor your API status using the health endpoint:

```http
GET /health
```

This endpoint can be used for monitoring, load balancer health checks, and deployment verification.

## 📄 License

[See the LICENSE File in the repo]

## 🤝 Contributing

[Will br Added Soon...]

## 📞 Support

[Email: subhendukumardutta330@gmail.com]
