# labview_rethinkdb
RethinkDB LabVIEW Client Driver

## What is RethinkDB?
[RethinkDB](https://www.rethinkdb.com/) is an open-source no-sql database for the realtime web.

## Getting Started
1. Install LabVIEW 2017+
2. Download and unzip the RethinkDB 2.3.6+ executable (e.g. C:\projects\rethinkdb-2.3.6\rethinkdb.exe)
3. Start the local RethinkDB Server using the command line (cmd.exe)

```
cd C:\projects\rethinkdb-2.3.8
rethinkdb.exe --http-port 5001
```

4. Ensure the RethinkDB server is running, in a web browser navigate to 

```
http://localhost:5001
```

5. Open the LabVIEW project `rethinkdb.lvproj`
6. Run the `\examples\rethinkdb_example_simple.vi`
   1. host = `localhost`
   2. port = `28015`
   3. version = `10`  # version 1.0 (v1_0)
7. Verify the LabVIEW RethinkDB Client connected successfully

```json
{"max_protocol_version":0,
"min_protocol_version":0,
"server_version":"2.3.6-windows",
"success":true}
```
## Basic Usage
1. Query the database list:

```
rethinkdb_query.vi
  Query: 'r.db_list()'
```


## Documentation
TBD
