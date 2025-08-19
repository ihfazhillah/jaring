# Issue 17: Improve configuration file handling

- The script should look for a `jaring.yaml` file in the current working directory by default.
- The `-c` or `--config` command-line argument should override the default configuration file.
- This allows running `jaring.py` from other directories and having it automatically pick up the local `jaring.yaml` file.