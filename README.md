# Recon Scripts

Collection of bash and python scripts used for reconnaisance automation.

## `./burp/`

### `b2h.py` - Burp To Http
Converts Burp Suite *.xml files into *.http files containing requests/responses.

**Usage**
```shell
$ ./b2h.py <input_file> [<output_directory>]
```


## `./nmap/`

### `nmp.py` - NMap Parser
Parses Nmap xml report and outputs data in the following format:
```
<url> <port> <protocol> <status> <service>
```

**Usage**
```shell
$ ./nmp.py <xml_file>
```