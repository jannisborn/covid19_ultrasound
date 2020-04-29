# POCOVIDScreen

## Teaser 
Code for the web interface of POCOVIDScreen (see [https://pocovidscreen.org/](https://pocovidscreen.org/)).

![alt text](https://github.com/jannisborn/covid19_pocus_ultrasound/blob/master/pocovidnet/plots/pocovidscreen.png "Web interface")

## Installation

- Clone the repo
- Start the containers with ddev (will automatically install composer dependencies)
- Install NPM dependencies.

```bash
ddev start
```

```bash
cd pocovidscreen 
npm install
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

- Start npm watcher to start coding
```bash
npm run watch
```

- Or run build for production
```bash
npm run prod
```

- Visit https://covidscreen.ddev.site/
