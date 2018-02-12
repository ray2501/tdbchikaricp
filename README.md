tdbchikaricp
=====

It is unofficial Tcl DataBase Connectivity Driver for HikariCP library.

[Tcl Database Connectivity (TDBC)](http://www.tcl.tk/man/tcl8.6/TdbcCmd/tdbc.htm)
is a common interface for Tcl programs to access SQL databases.

[tclBlend](http://tcljava.sourceforge.net/docs/website/index.html) is a Tcl package
that provides access to Java classes from Tcl. tclBlend is implemented using 
[JNI](https://en.wikipedia.org/wiki/Java_Native_Interface).

[tclJBlend](http://wiki.tcl.tk/47668) is a fork of TclBlend, a Tcl extension that
uses JNI to communicate with a Java interpreter.

[HikariCP](http://brettwooldridge.github.io/HikariCP/) is a solid high-performance
JDBC connection pool.

The library consists of a single [Tcl Module](http://tcl.tk/man/tcl8.6/TclCmd/tm.htm#M9) file.
tdbc::hikaricp extension is using tclBlend package to call HikariCP/JDBC API.

The tdbc::hikaricp driver provides a database interface that conforms to Tcl DataBase Connectivity (TDBC)
and allows a Tcl script to connect to any SQL database presenting a HakariCP/JDBC interface.
Now it is a limited support implement.

Only test on openSUSE LEAP 42.3 (64bit) and Open JDK8.

This extension needs Tcl >= 8.6, TDBC and tclBlend (or tclJBlend) package.
Tcl 8.6.1-8.6.5 maybe need patch, please
check [tclBlend](http://wiki.tcl.tk/1313).


License
=====

MIT License


Installation
=====

The tdbc::hikaricp driver requires Tcl >= 8.6, TDBC and tclBlend package.

For Windows platform, if your Tcl lib folder is `C:\Tcl\lib`,
then copy hikaricp-0.1.tm this file to below location:

    C:\Tcl\lib\tcl8\8.6\tdbc

For openSUSE (64bit), copy hikaricp-0.1.tm this file to below location:

    /usr/lib64/tcl/tcl8/8.6/tdbc

Or you can use installer.tcl to install this package.
`installer.tcl` use `info library` to get path and install tm file.
If you want to uninstall after using installer.tcl to install,
try below command (on Linux platform):

    sudo ./installer.tcl -uninstall 1

If you try to uninstall on Windows platform,

    tclsh installer.tcl -uninstall 1


Commands
=====

tdbc::hikaricp::connection create db configFile ?datasource? ?-option value...?

Connection to a HakariCP database is established by invoking `tdbc::hikaricp::connection create`,
passing it the name to be used as a connection handle, followed by a property file path.

The tdbc::hikaricp::connection create object command supports the -isolation and -readonly options.

HikariCP driver for TDBC implements a statement object that represents a SQL statement in a database.
Instances of this object are created by executing the `prepare` or `preparecall` object
command on a database connection.

The `prepare` object command against the connection accepts arbitrary SQL code
to be executed against the database.

The `paramtype` object command allows the script to specify the type and
direction of parameter transmission of a variable in a statement.
Now HakariCP driver only specify the type work.

HakariCP driver paramtype accepts below type:  
bigint, binary, bit, char, date, decimal, double, float, integer,
longvarbinary, longvarchar, numeric, real, time, timestamp, smallint,
tinyint, varbinary, varchar, blob and clob.

The `execute` object command executes the statement.


Examples
=====

Before execute TDBC::HakariCP package, please setup CLASSPATH correctly.

You need add 3 packages in your CLASSPATH:
* Database JDBC driver file
* slf4j
* HikariCP

Below is an example (on Linux platform):

	export CLASSPATH=$CLASSPATH:/home/danilo/hsqldb/lib/hsqldb.jar
	export CLASSPATH=$CLASSPATH:/home/danilo/slf4j-api-1.7.25.jar
	export CLASSPATH=$CLASSPATH:/home/danilo/HikariCP-2.7.7.jar

If you want to disable slf4j warning, try to add slf4j-nop to your CLASSPATH:

	export CLASSPATH=$CLASSPATH:/home/danilo/slf4j-nop-1.7.25.jar

## Example: HSQLDB

Below is a config file (hsqldb.config):

    dataSourceClassName=org.hsqldb.jdbc.JDBCDataSource
    dataSource.user=SA
    dataSource.password=
    dataSource.databaseName=test.db

Below is an exmaple:

    package require tdbc::hikaricp

    set configFile   /home/danilo/hsqldb.config

    tdbc::hikaricp::connection create db $configFile

    set statement [db prepare {create table if not exists person (id integer not null, name varchar(40))}]
    $statement execute
    $statement close

    set statement [db prepare {insert into person values(:id, :name)}]
    # It is important -> need to setup type
    $statement paramtype id integer
    $statement paramtype name varchar    

    set myparams [dict create id 1 name Leo]
    $statement execute $myparams    

    set id 2
    set name Mary    
    $statement execute
    $statement close

    set statement [db prepare {SELECT * FROM person}]

    $statement foreach row {
        if {[catch {set id [dict get $row ID]}]} {
            puts "ID:"
        } else {
            puts "ID: $id"
        }
        
        if {[catch {set name [dict get $row NAME]}]} {
            puts "NAME:"
        } else {
            puts "NAME: $name"
        }        
    }

    $statement close

    set statement [db prepare {drop table person}]
    $statement execute
    $statement close

    db close

## Example: PostgreSQL

Below is a config file (postgresql.config):

    dataSourceClassName=org.postgresql.ds.PGSimpleDataSource
    connectionTimeout=30000
    dataSource.user=danilo
    dataSource.password=danilo
    dataSource.databaseName=danilo
    dataSource.portNumber=5432
    dataSource.serverName=localhost

Below is an exmaple:

    package require tdbc::hikaricp

    set configFile   /home/danilo/postgresql.config

    tdbc::hikaricp::connection create db $configFile

    set statement [db prepare {select VERSION()}]
    puts "Current PostgreSQL:"
    $statement foreach row {
        puts "[dict get $row version]"
    }

    $statement close

    db close

And another example, create a HikariDataSource and transfer it to our driver,

    package require java
    package require tdbc::hikaricp

    java::import com.zaxxer.hikari.HikariConfig
    java::import com.zaxxer.hikari.HikariDataSource

    set configFile   /home/danilo/tmp/postgresql.config
    set config [ java::new HikariConfig $configFile ]
    set DataSourceI [ java::new HikariDataSource $config ]
    tdbc::hikaricp::connection create db "" $DataSourceI

    set statement [db prepare {select VERSION()}]
    puts "Current PostgreSQL:"
    $statement foreach row {
        puts "[dict get $row version]"
    }

    $statement close

    db close
    $DataSourceI close

User can create a DataSource and transfer it to our driver,
so it is possible to create another DataSource object and use it
(if setup CLASSPATH correctly). Below is an example:

    package require java
    package require tdbc::hikaricp

    java::import org.postgresql.ds.PGSimpleDataSource

    set DataSourceI [ java::new PGSimpleDataSource ]
    $DataSourceI setUser            "danilo"
    $DataSourceI setPassword        "danilo"
    $DataSourceI setDatabaseName    "danilo"
    $DataSourceI setServerName      "localhost"

    tdbc::hikaricp::connection create db "" $DataSourceI

    set statement [db prepare {select VERSION()}]
    puts "Current PostgreSQL:"
    $statement foreach row {
        puts "[dict get $row version]"
    }

    $statement close

    db close


And another example, using [Alibaba Druid](https://github.com/alibaba/druid) DataSource
to test. You need add Druid package in your CLASSPATH:

    export CLASSPATH=$CLASSPATH:/home/danilo/druid-1.1.8.jar

Then you can create a Alibaba Druid DataSource and transfer it to our driver,

    package require java
    package require tdbc::hikaricp

    java::import com.alibaba.druid.pool.DruidDataSource

    set DataSourceI [ java::new DruidDataSource ]
    $DataSourceI setDriverClassName "org.postgresql.Driver"
    $DataSourceI setUsername        "danilo"
    $DataSourceI setPassword        "danilo"
    $DataSourceI setUrl             "jdbc:postgresql://localhost:5432/danilo"
    $DataSourceI setInitialSize     5
    $DataSourceI setMinIdle         1
    $DataSourceI setMaxActive       10

    tdbc::hikaricp::connection create db "" $DataSourceI

    set statement [db prepare {select VERSION()}]
    puts "Current PostgreSQL:"
    $statement foreach row {
        puts "[dict get $row version]"
    }

    $statement close

    db close
    $DataSourceI close

