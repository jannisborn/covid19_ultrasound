## Infrastructure
<img src="../.ddev/doc/pocovidscreen_arch.png" width="600"/>

### Screening process
<img src="../.ddev/doc/screen_process.png" width="600"/>

## Installation (web application)

To use the trained model with our web application *locally* follow those steps :

- Clone the repo
- Start the containers with [ddev](https://ddev.readthedocs.io/en/stable/) (will automatically install composer dependencies)
- You will need yarn to work with the web UI. You can get it [here](https://classic.yarnpkg.com/en/docs/install)

```bash
ddev start
```

- Install dependencies

```bash
yarn install
```

- Copy .env.example to .env

```bash
cp .env.example .env
```

- Generate app key

```bash
ddev exec php artisan key:generate
```

- Run database migration

```bash
ddev exec php artisan migrate:fresh
```

- Generate JWT secret

```bash
ddev exec php artisan jwt:secret
```

- Start development server
```bash
yarn run start
```

- Or run a build for production
```bash
yarn run build
```

- Visit http://localhost:3000
