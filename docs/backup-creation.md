# Creating Backups with RunUp

Once RunUp is properly [installed](getting-started.md#installation) and [configured](setup.md#configuration), creating a backup can be one of the easiest things you will ever do in your life as a programmer.

## Backup all the projects

To create a backup of all the projects in the `runup.yaml` file, you only need to run the followin command:

```
runup backup
```

## Backup one specific project

If you have multiple projects on your config file but you only wnat to create a backup of one of them, you only need to add the name of the project as an argument. Example:

```
runup backup myproject
```
