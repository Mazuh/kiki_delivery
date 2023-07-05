# Kiki Delivery

Kiki's Delivery Service -- 魔女の宅急便

## Setting up

### With Docker

TODO.

### Alternative for local development

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

And then start a development server:

```sh
make dev
```

A few useful outputs:

- Root API is available at: http://127.0.0.1:8000
- Live docs at: http://127.0.0.1:8000/docs

## Architecture

TODO.

## License

This project was made by me, [Marcell "Mazuh" G. C. da Silva](https://github.com/mazuh),
as part of the graduate course in Software Architecture specialization
at [FIAP](https://www.fiap.com.br/) college.
And it's under [MIT License](./LICENSE).
