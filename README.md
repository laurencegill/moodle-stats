# moodle-stats
Python script for pulling some moodle statistics from the database

You'll need some permissions (and a password), for example:

```
GRANT SELECT ON `moodle`.`mdl_users` TO 'moodlechecker'@'hostname';
GRANT SELECT ON `moodle`.`mdl_files` TO 'moodlechecker'@'hostname';
GRANT SELECT ON `moodle`.`mdl_chat_users` TO 'moodlechecker'@'hostname';
```

Use for cacti or similar, may possibly adapt for threshold alerts in the future.
