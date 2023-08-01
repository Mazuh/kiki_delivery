# Kiki Delivery

Kiki's Delivery Service -- 魔女の宅急便

## Setting up

### With Docker containers

Having at least Docker 24, run (containers with new volumes just to make sure):

```sh
docker compose down --volumes
docker compose up
```

And access:
http://localhost:8000/docs/

That's enough for a local demo.

### In host machine for local development

Make sure you have installed:

- Python 3.11
- PostgreSQL 14

If you're in a Linux or Mac environment, just run for initial setup:

```sh
make build
```

Also, install these VS Code extensions to keep the code well linted, formated
and even with some static type checking:

- Python (Microsoft)
- Pylance (Microsoft)
- Black (Microsoft)

You might need to reopen the VS Code or the terminal to load these new stuff.

New terminals VS should be already loaded with the `.venv`, it'll
prefix all terminal prompts. But in case that doesn't
happen you can manually load it with:

```sh
source .venv/bin/activate
```

Now install the dependencies of this virtual env:

```sh
make install
```

Run database migrations (hint: `createdb kiki_delivery`):

```sh
make migrate
```

And then start a development server:

```sh
make dev
```

A few useful outputs:

- Root API is available at: http://127.0.0.1:8000
- Live docs at: http://127.0.0.1:8000/docs

## Architecture

It's inspired by a mix of concepts from DDD, Clean and Hexagonal architecturing.

Currently, there's no authentication nor authorization.

Aggregate root domains are:
- Customer ("cliente").
- Order ("pedido").
- Product ("product").

The layers are:
- Domain, having all the business rule agnostic to frameworks and storage,
  all other layers depend of this layer but this layer doesn't depend of anything
  else but itself.
- Infrastructure, they implement what the domain logic defined as abstract
  interfaces to persist the changes.
- Application, as RESTful API controllers, they by default inject the standard
  infrastructure but it's very agnostic to it, mostly focus on picking the domain
  entities and making proper calls to it.

Each domain sublayer has a driven ports module for defining things like
the repositories APIs, the aggregated entities in another module and a few
contextual value objects in one last module containing important data
validation.

The infrastructure sublayers contain an Alembic module for managing database
changes, ORM modules for handling with SQL databases and repositories to
implement the concrete versio of domain interfaces.

And the application tries to organize itself in a RESTful design for
more predictable and mostly idempotent state, so it can be very reusable
and simple. Because of that, it might not be obvious, but the use cases can
be achieved through:

- Customer management by both user themselves at individual level and
  system-wide level: all customers endpoints, it's a full CRUD.
- Products management: supposed to be read by users and having writing
  all operations for restaurant managers.
- Searching products by category: GET products endpoint.
- Adding chart: a specific endpoint for POST order items.
- Checkout: individual POST and GET of orders but also an extra endpoint
  to change the orders status to RECEIVED only if there are items added first.
- Orders listing: almost full CRUD operations for the restaurant, and an
  individual GET by id for customers query.

The migration scripts include seed data for all of this described above.

## License

This project was made by me, [Marcell "Mazuh" G. C. da Silva](https://github.com/mazuh),
as part of the graduate course in Software Architecture specialization
at [FIAP](https://www.fiap.com.br/) college.
And it's under [MIT License](./LICENSE).
