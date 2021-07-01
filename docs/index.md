# RunUp - The Definitive Backup Solution

RunUp is a backup solution that implements a new backup strategy: fragmented backups. This solution solves all the drawbacks of traditional strategies.

## Fragmented backup

There are three typical backup strategies: Full backups, incremental backups and differential backups:

* Full backups duplicate unmodified data and are very slow to create, but are easier and faster to restore. 
* Differential backups still create full backups (say weekly) and create partial backups _containing only the new and modified files since the last full backup_ (say daily). This may reduce data duplication somewhat and makes partial backups faster than the full backup, but it makes restore slower because you need to restore the last full backup and the last differential backup.
* Incremental backups work in the same way as differential backups but partial backups _only contain the files changed since the last full or partial backup_. This reduces data duplication even further and makes partial backups faster, but makes data restoration even slower, as you will have to restore the last full backup and all partial backups created after the full backup, in order.

With the above information in mind, I have come up with fragmented backups, a new backup strategy that only creates a full backup the first time, then all backups will be incremental backups. But the unchanged files are associated with the previously stored files, so during the backup restore, it is possible to "merge the fragments" and make the restore as fast as if it were a full backup.

## Key features

### Saves disk space

Files are never duplicated in the backup storage, even if they are duplicated in the repository or renamed without changing the content.

### Create faster backups

Each backup contains only one copy of new or changed files. This allows us to create backups faster, saving time and memory usage.

### Quick restoration of backups

When restoring data, we handle it as a full backup, so we don't have the inconvenience of tools that implement traditional partial backup strategies.
