# Restoring backups with RunUp

Restoring your backups is pretty straight foward. It is only one command with a couple of options that you will need depending on what exactly you want to do.

## Full restoration of the lastest backup

In order to restore all the projects to the latest version backed up, you will need to execute one single command:

```
runup restore
```

## Restoring the lastest backup of a specific project

When you to restore one specific project, not all, you just need to specify the name of the project you want to restore.

_Example:_

```
runup restore projectname
```

## Restoring an older backup

When you don't want to restore the latest backup but an older one, you can do specifying the number of the job that created that backup with the `--job` option.

_Example:_

To restore all the projects their status at the moment of the backup number 3, you can do it with the command:

```
runup restore --job 3
```

In the other hand, if you want to restore only a specific project, you can do it with the command:

```
runup restore --job 3 projectname
```

## Cleaning the directory at restoration time

By default, a backup restoration will only replace the modified files. That means, any file created after the backup to be restored will still be present after the backup restoration. To change this behavior yu can add the flag `--clear-location`.

_Example:_

```
runup restore --clear-location projectname
```
