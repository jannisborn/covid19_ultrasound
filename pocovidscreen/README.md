# Laravel-React SPA

Starter Boilerplate SPA made with Laravel and React.

## Features

- Laravel 7, React, React Router
- React Hook, React Context for state management
- Authentication with JWT
- Login, register, reset password
- Flexible Page Layout
- Flexible, Protected Routing
- Tailwind CSS
- ESlint

## Installation

- Clone the repo
- Installing all Composer & NPM dependencies.

```bash
composer install && npm install
```

- Copy .env.example to .env
- Generate app key

```bash
php artisan key:generate
```

- Run database migration

```bash
php artisan migrate:fresh
```

- Generate JWT secret

```bash
php artisan jwt:secret
```

- Compiling Assets

```bash
npm run dev
```

- Boot up a server

```bash
php artisan serve
```
