# Libcdb

A simple library for searching and querying all libc related data on https://libc.ml

## Usage

Search all matched libc with '90' at the end of function system's address.

```python
import libcdb

for libc in libcdb.search_libc({'fun':'system','adr':'0x90'}):
    print(libc)

# Output:
# Libc version:libc6_2.23-0ubuntu7_amd64
# Libc version:libc6_2.19-0ubuntu6.11_amd64
# Libc version:libc6_2.21-0ubuntu5_amd64
# Libc version:libc6-amd64_2.15-0ubuntu10.11_i386
# Libc version:libc6_2.23-0ubuntu5_amd64
# Libc version:libc6_2.23-0ubuntu4_amd64
# Libc version:libc6_2.19-0ubuntu6.6_i386
# Libc version:libc6_2.19-0ubuntu6.9_amd64
# Libc version:libc6-amd64_2.15-0ubuntu10.12_i386
# Libc version:libc6-dbg_2.19-0ubuntu6.11_amd64
# Libc version:libc6-dbg_2.23-0ubuntu7_amd64
# Libc version:libc6-dbg_2.19-0ubuntu6.14_amd64
# Libc version:libc6-dbg_2.23-0ubuntu10_amd64
```

Query all data related to specific libc version

```python
import libcdb

libc = libcdb.query_libc('libc6-dbg_2.23-0ubuntu7_amd64')
libc.base = 0x1000000
print('main_arena at 0x{:08x}'.format(libc['main_arena']))

# Output:
# main_arena at 0x013c3b20
```

## How to install

I recommend to install by pip, which is simplest way.

```bash
pip install libcdb
```

Or you can just download the libcdb.py and add it to your project :).

## Caution

Only dbg version of libc (_eg. libc6-dbg_2.23-0ubuntu7_amd64_) contains full symbol (_eg. main_arena_).

## Documentation

```python
CLASSES
    LIBC

    class LIBC
     |  LIBC object
     |
     |  Provides dict-like access method.
     |
     |  Automatically load all libc data if key NOT found.
     |
     |  Methods defined here:
     |
     |  __getitem__(self, item)
     |
     |  __init__(self, data=None, id=None)
     |
     |  __repr__(self)
     |
     |  __setitem__(self, key, value)
     |
     |  fetchall(self)
     |
     |  parse(self, data)

FUNCTIONS
    query_libc(id)
        Query specific libc based on id

        example:
            query_libc('libc6_2.24-7ubuntu2_amd64')
        :param id:
        :return: A LIBC object

    query_libc_raw(id)
        Query raw json data for specific id
        :param id:
        :return: Raw libc json data

    search_libc(condition)
        Search libc database for specific condition
        condition address can be string or hex or int.

        example:
            search_libc({'fun':'system','adr':'0x90'})
            search_libc({'fun':'system','adr':0x90})
            search_libc(('system','0x90'))
            search_libc(('system',0x90))
        :param condition:
        :return: A LIBC object
```