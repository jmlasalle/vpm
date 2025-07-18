# `vpm`

Creates config file if it doesn&#x27;t exists. Runs before every command

**Usage**:

```console
$ vpm [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `version`: Prints the application&#x27;s version number.
* `home`
* `room`
* `element`
* `task`
* `part`
* `db`

## `vpm version`

Prints the application&#x27;s version number.

**Usage**:

```console
$ vpm version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vpm home`

**Usage**:

```console
$ vpm home [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Adds a home to the local database
* `get`: Get home information
* `update`: Update home information
* `delete`: Delete home

### `vpm home add`

Adds a home to the local database

**Usage**:

```console
$ vpm home add [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--address TEXT`: [required]
* `--description TEXT`
* `--help`: Show this message and exit.

### `vpm home get`

Get home information

**Usage**:

```console
$ vpm home get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm home update`

Update home information

**Usage**:

```console
$ vpm home update [OPTIONS]
```

**Options**:

* `--name TEXT`
* `--address TEXT`
* `--help`: Show this message and exit.

### `vpm home delete`

Delete home

**Usage**:

```console
$ vpm home delete [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vpm room`

**Usage**:

```console
$ vpm room [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`
* `all`
* `get-by-name`
* `update`
* `delete`

### `vpm room add`

**Usage**:

```console
$ vpm room add [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--level INTEGER`: [default: 0]
* `--description TEXT`
* `--help`: Show this message and exit.

### `vpm room all`

**Usage**:

```console
$ vpm room all [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm room get-by-name`

**Usage**:

```console
$ vpm room get-by-name [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

### `vpm room update`

**Usage**:

```console
$ vpm room update [OPTIONS]
```

**Options**:

* `--name TEXT`
* `--help`: Show this message and exit.

### `vpm room delete`

**Usage**:

```console
$ vpm room delete [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

## `vpm element`

**Usage**:

```console
$ vpm element [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Adds a new element to the local database.
* `get`: Get element information
* `all`: Get all elements
* `update`: Update element information
* `delete`: Delete an element

### `vpm element add`

Adds a new element to the local database.

**Usage**:

```console
$ vpm element add [OPTIONS]
```

**Options**:

* `--room-name TEXT`: [required]
* `--name TEXT`: [required]
* `--description TEXT`
* `--brand TEXT`
* `--model TEXT`
* `--model-number TEXT`
* `--manual-url TEXT`
* `--manufacture-url TEXT`
* `--install-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`
* `--cost FLOAT`
* `--currency TEXT`: [default: USD]
* `--help`: Show this message and exit.

### `vpm element get`

Get element information

**Usage**:

```console
$ vpm element get [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

### `vpm element all`

Get all elements

**Usage**:

```console
$ vpm element all [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm element update`

Update element information

**Usage**:

```console
$ vpm element update [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--new-name TEXT`
* `--description TEXT`
* `--help`: Show this message and exit.

### `vpm element delete`

Delete an element

**Usage**:

```console
$ vpm element delete [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

## `vpm task`

**Usage**:

```console
$ vpm task [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Adds a new task to the local database.
* `get`: Get task information
* `update`: Update task information
* `delete`: Delete a task
* `complete`: Mark a task as complete

### `vpm task add`

Adds a new task to the local database.

**Usage**:

```console
$ vpm task add [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--type TEXT`: Type of task (MAINTENANCE, REPAIR, REPLACE, INSPECT)  [default: MAINTENANCE]
* `--description TEXT`
* `--due-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`
* `--interval INTEGER`: Interval for recurring task
* `--interval-unit TEXT`: Unit for interval (days, weeks, months, years)
* `--priority INTEGER`
* `--help`: Show this message and exit.

### `vpm task get`

Get task information

**Usage**:

```console
$ vpm task get [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

### `vpm task update`

Update task information

**Usage**:

```console
$ vpm task update [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--new-name TEXT`
* `--type TEXT`: Type of task (MAINTENANCE, REPAIR, REPLACE, INSPECT)
* `--description TEXT`
* `--due-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]`
* `--priority INTEGER`
* `--help`: Show this message and exit.

### `vpm task delete`

Delete a task

**Usage**:

```console
$ vpm task delete [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

### `vpm task complete`

Mark a task as complete

**Usage**:

```console
$ vpm task complete [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

## `vpm part`

**Usage**:

```console
$ vpm part [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Adds a new part to the local database.
* `get`: Get part information
* `update`: Update part information
* `delete`: Delete a part

### `vpm part add`

Adds a new part to the local database.

**Usage**:

```console
$ vpm part add [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--description TEXT`: [required]
* `--manufacturer TEXT`
* `--model-number TEXT`
* `--serial-number TEXT`
* `--help`: Show this message and exit.

### `vpm part get`

Get part information

**Usage**:

```console
$ vpm part get [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

### `vpm part update`

Update part information

**Usage**:

```console
$ vpm part update [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--new-name TEXT`
* `--description TEXT`
* `--manufacturer TEXT`
* `--model-number TEXT`
* `--serial-number TEXT`
* `--help`: Show this message and exit.

### `vpm part delete`

Delete a part

**Usage**:

```console
$ vpm part delete [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--help`: Show this message and exit.

## `vpm db`

**Usage**:

```console
$ vpm db [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Initializes the database and creates all...
* `info`: Prints the database engine configuration...
* `schemas`: Prints the schemas in the database.
* `tables`: Prints the tables in the database.
* `columns`: Prints the columns of a table.

### `vpm db create`

Initializes the database and creates all necessary tables.

**Usage**:

```console
$ vpm db create [OPTIONS]
```

**Options**:

* `--overwrite`
* `--help`: Show this message and exit.

### `vpm db info`

Prints the database engine configuration (including URL).

**Usage**:

```console
$ vpm db info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm db schemas`

Prints the schemas in the database.

**Usage**:

```console
$ vpm db schemas [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm db tables`

Prints the tables in the database.

**Usage**:

```console
$ vpm db tables [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `vpm db columns`

Prints the columns of a table.

**Usage**:

```console
$ vpm db columns [OPTIONS] TABLE
```

**Arguments**:

* `TABLE`: [required]

**Options**:

* `--help`: Show this message and exit.
