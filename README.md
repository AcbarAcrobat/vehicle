# entity_server

## Run

```sh
$ pytest # all
$ pytest tests/facility # certain entity
```

## Parallel

```sh
$ pytest -n=12 # cpu count
```

## Report
Install [Allure](https://github.com/allure-framework/allure2/releases)

At the end of test run:
```sh
$ cd entity_server
$ allure serve allure_dir
```
