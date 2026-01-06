# MyMind

MyMind is a modern web application designed to help users manage threads and ingest logs efficiently. Built with a robust Laravel backend and a dynamic React frontend, it offers a seamless experience for tracking and organizing personal data streams.

## Features

-   **Secure Authentication**: Powered by Laravel Sanctum for secure, cookie-based session management.
-   **Thread Management**: Create, view, and update threads and status.
-   **Message System**: Real-time message exchange within threads.
-   **Log Ingestion**: API endpoints to ingest and store system or user logs.
-   **Responsive Design**: A sleek, modern user interface built with TailwindCSS v4.

## Tech Stack

### Backend

-   **Framework**: Laravel 12
-   **Language**: PHP 8.2+
-   **Authentication**: Laravel Sanctum
-   **Database**: MySQL / SQLite (configurable)

### Frontend

-   **Library**: React 19
-   **Build Tool**: Vite
-   **Styling**: TailwindCSS v4
-   **State Management**: Zustand
-   **Data Fetching**: React Query (@tanstack/react-query)
-   **Routing**: React Router v7

## Prerequisites

Ensure you have the following installed on your local machine:

-   [PHP](https://www.php.net/downloads) (8.2 or higher)
-   [Composer](https://getcomposer.org/)
-   [Node.js](https://nodejs.org/) & [npm](https://www.npmjs.com/)

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/mymind.git
    cd mymind
    ```

2.  **Install Backend Dependencies**

    ```bash
    composer install
    ```

3.  **Install Frontend Dependencies**

    ```bash
    npm install
    ```

4.  **Environment Setup**
    Copy the example environment file and configure your database settings:

    ```bash
    cp .env.example .env
    ```

    Generate the application key:

    ```bash
    php artisan key:generate
    ```

5.  **Database Migration**
    Run the migrations to set up your database schema:
    ```bash
    php artisan migrate
    ```

## Running the Application

For development, you can run both the backend and frontend servers concurrently using the provided script (if `concurrently` is configured, otherwise run in separate terminals):

```bash
npm run dev
```

_Note: The `dev` script in `composer.json` is configured to run Laravel Sail, Artisan Serve, Queue Listen, and Vite concurrently._

Alternatively, run them separately:

-   **Backend**: `php artisan serve`
-   **Frontend**: `npm run dev` (Vite)

## API Documentation

-   `POST /api/login`: Authenticate user.
-   `POST /api/logout`: End session.
-   `GET /api/user`: Get authenticated user details.
-   `GET /api/threads`: List threads.
-   `GET /api/threads/{id}/messages`: Get messages for a thread.
-   `POST /api/ingest-log`: Ingest external logs.

## License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
