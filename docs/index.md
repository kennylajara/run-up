# RunUp - The Definitive Backup Solution

RunUp is a backup solution that implements a new backup strategy: Fragmented Backups. This solution solves all the drawback of the traditional backup strategies.

## Framented Backup

Traditionally, there are two ways of creating backups: Full backups and partial (incremental or differential) backups. Full backups duplicates data and are very slow to create, while partial backups reduce data duplication and are created faster but are slower to restore because you need to restore several partial backups.

We have devised the fragmented backups, a new backup strategy that creates partial backups but restores full backups, getting the best of both worlds.

### Save disk space

We don't duplicate unchanged files in your backup storage even if is duplicated in your repository or renamed at some point in the future.

### Create faster backups

RunUp only copy the new or changed files. This allow us to create the backups faster, saving you time and memory usage.

### Restore your backup faster

While restoring the data, we handle it as a full backup so we don't have the drawback of the tools implementing partial backup strategies.