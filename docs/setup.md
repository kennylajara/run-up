# How to setup RunUp

Once you have [installed RunUp](getting-started.md#installation), you just need to complete two simple tasks: Create a config file and initialize RunUp in the directory.

## Configuration

To configure RunUp you need to create a [YAML](https://en.wikipedia.org/wiki/YAML) file named `runup.yaml` or `runup.yml`, this will be our configuration file. There your will define the way your backups will be created.

### Definitions

#### Version

`string (required)` You must always define a version. At the moment the value of the version need to be `1` or `1.0`. This won't change the behavior of the program since this definition has been introduced for future backward compatibility.

*Example:*

```yaml
version: '1'
```

#### Project

`array (required)` Each value of this array is another array where the is the name of a project or service to be backed up and the value is project parameter.

**Project's parameters**

| Name      | Type        | Description                                                                             |
| --------- | ----------- | --------------------------------------------------------------------------------------- |
| `include` | `List[str]` | `(required)` List of path to directories and files to include in the backup.            |
| `exclude` | `List[str]` | `(optional)` List of path to directories and files to exlude from the already included. |

> **Note:** Absolute paths are not officially supported. It is recommended to use relative paths from location of the `runup.yaml` file.

### Example

Now let's see an example of a `runup.yml` file created configred to backup 2 projects. One name `app` and another named `website`.

For the `app` project we are going to backup all the directory `app` and its content. For the project `website` we are going to backup the directories `cronjobs` and `web` but ignoring the subdirectory `web/src/vendor` and its content.

```yaml
version: '1'

project:
  app:
    include:
      - './app'
  website:
    include: 
      - './cronjobs'
      - './web'
    exclude:
      - './web/src/vendor'
```

## Initialization

Once you have created the config file, you always need to initalize RunUp by executing:

```
runup init
```
