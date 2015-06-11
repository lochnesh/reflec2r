reflec2r
==========

Written in Python 2.7.x, using [dwolla-python](https://github.com/Dwolla/dwolla-python) and [peewee](https://github.com/coleifer/peewee) for database operations.

## Quickstart

#### Grab your dependencies
```bash
git clone http://stash.dwolla.net/scm/dlab/reflec2r.git
cd reflec2r
pip install dwolla peewee
```

#### Create your database
```MySQL
CREATE DATABASE IF NOT EXISTS reflector;

USE reflector;

CREATE TABLE `reflector` (
`id`  int(11) UNSIGNED NOT NULL AUTO_INCREMENT ,
`tx_id`  int(11) NULL DEFAULT NULL ,
`refund_id`  int(11) NULL DEFAULT NULL ,
`amount`  varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL ,
`date`  datetime NULL DEFAULT NULL ,
PRIMARY KEY (`id`));

CREATE TABLE `reflector_settings` (
`key`  varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL ,
`value`  varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL 
);
```

#### Set your environment variables

| Key            | Description                             |
|----------------|-----------------------------------------|
| DWOLLA_KEY     | Dwolla API Key                          |
| DWOLLA_SECRET  | Dwolla API Secret                       |
| DWOLLA_TOKEN   | Reflector account token with Send scope |
| DWOLLA_PIN     | Reflector account PIN                   |
| DWOLLA_SANDBOX | Sandbox mode?                           |
| REFL_DBNAME    | MySQL database name                     |
| REFL_DBHOST    | MySQL server hostname/IP                |
| REFL_DBPW      | Database password                       |
| REFL_DBUN      | Database username                       |

#### Crontab
Adjust time accordingly, this would run every 15 minutes.

```bash
su - my_best_practices_non_privileged_user
crontab -e
(vi)
*/15 * * * * python /home/my_best_practices_non_privileged_user/reflec2r.py
(:wq)
```

## Overview

reflec2r is simple, it just:
* Checks to see if another instance is running.
* Grabs all `money_received` transactions from the last ISO-8601 timestamp forward and refunds them.
* Unlocks 'mutex'.

## Changelog

2.0.2
* Better history checking
* Removed timestamp dependency

2.0.1
* Catch all exceptions
* Better logging

2.0.0
* Initial release

## License

The MIT License (MIT)

Copyright (c) 2015 David Stancu, Dwolla Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
