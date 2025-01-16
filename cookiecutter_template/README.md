# example source plugin for CloudQuery

This plugin fetches data from `{{cookiecutter.plugin_name}}`.

## Building the Plugin as a Container

```bash
make run
```

## Running the Plugin as a Container

```bash
make run-docker
```

## Testing it

```shell
cloudquery sync --log-console --log-level debug ./TestConfig.yaml
```

## How to test the plugin

0. Follow [this documentation](../../CloudQuery_account.md) first if you don't have account at https://cloudquery.io and also install and configure CloudQuery CLI tool.
1. Generate token for service XXX at URL / login with `aws-login --account otk-mgmt-twilio sre` / request API key for service YYY at URL.
2. Change directory to the plugin, for example: `cd plugins/{{cookiecutter.plugin_name}}`.
3. Run `make build-docker` to build an image `{{cookiecutter.plugin_name}}:latest` (VPN connection required).
4. Run the plugin container: `make run-docker`.
5. In another terminal tab, export variables `XXX` and `YYY`, then run `cloudquery sync` with `make local-test`.
6. Analyze logs and SQLite DB file.

Example of a good fetch:

`cloudquery sync` logs:

```console
 % make local-test
cloudquery sync TestConfig.yaml
Loading spec(s) from TestConfig.yaml
Starting sync for: github-prs (grpc@localhost:7777) -> [sqlite (cloudquery/sqlite@v2.7.3)]
| Syncing resources... (40/-, 0 resources/hr) [1h9m8s] Sync completed successfully. Resources: 167192, Errors: 0, Warnings: 0, Time: 1h9m8s
| Syncing resources... (40/-, -49213652 resources/hr) [1h9m8s] echo
```

Plugin logs:

```text
{"address": "[::]:7777", "event": "Starting server", "level": "info", "timestamp": "2024-06-13T09:50:09Z"}
...
XXX
...
YYY
...
{"client_id": "githubprs", "table": "github_prs_metadata", "resources": 167192, "depth": 0, "event": "table resolver finished successfully", "level": "info", "timestamp": "2024-06-13T10:59:46Z"}
```
