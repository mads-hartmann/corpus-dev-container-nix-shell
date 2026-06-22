# corpus-dev-container-nix-shell

Minimal corpus fixture for evaluating devcontainer setup generation against a repository that already uses `nix-shell`.

The existing environment setup is defined in `shell.nix`, following the declarative shell shape from the official Nix tutorial.

## Development

Enter the environment:

```sh
nix-shell
```

Run the check task:

```sh
make check
```

Start the HTTP service:

```sh
make serve
```

The service listens on `0.0.0.0:8000` by default and exposes `GET /healthz`.
