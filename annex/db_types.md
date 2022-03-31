## MariaDB data types

### Data types

| Type | Description | Storage |
| :--- | :---------- | :------ |
| varchar(M) | Variable-length string. M respresents the maximum number of characters to display. | len + 1 bytes if <= 255 bytes,<br>otherwise, len + 2 bytes| 
| timestamp | Converted Unix timestamp in the format YYYY-MM-DD hh:mm:ss.<br/>Range: from 1970-01-01 00:00:01 to 2038-01-19 03:14:07. | 4 bytes |
| int(M) | Normal-size integer. M respresents the maximum number of digits to display.<br/>Range: from 0 to (2 \*\* 32) - 1 for UNSIGNED, from -(2 \*\* 31) to (2 \*\* 31) - 1 for SIGNED. | 4 bytes |
| json | Text value containing the JSON file. May contain up to (2 \*\* 32) - 1 characters. | len + 4 bytes |
| datetime | Date and time in the format YYYY-MM-DD hh:mm:ss.<br/>Range: from 1000-01-01 00:00:00 to 9999-12-31 23:59:59. | 8 bytes |
| bigint(M) | Large integer. M respresents the maximum number of digits to display.<br/>Range: from 0 to (2 \*\* 64) - 1 for UNSIGNED, from -(2 \*\* 63) to (2 \*\* 63) - 1 for SIGNED. | 8 bytes |
| bit(M) | Bit-field value. M represents the number of bits per value.<br/>Values are automatically zero-padded. Values are returned as binary. | (M + 7) / 8 bytes |
| blob | Binary large object. May contain up to 65,535 bytes. | len + 2 bytes |

**len** - actual length in bytes.

### Date and time notation

YYYY - year, four digits;
MM - month, two digits;
DD - day, two digits;
hh - hour, two digits;
mm - minute, two digits;
ss - second, two digits.
