#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import textwrap
import subprocess
import time

def main():

    # Startup glassfish
    glassfishRoot = os.environ.get('GLASSFISH_ROOT')
    os.chdir(glassfishRoot + '/bin')
    subprocess.call(["./asadmin", "start-domain"])

    resourceType = os.environ.get('CONNECTION_POOL_RESOURCE_TYPE')
    dataSourceClassName = os.environ.get('CONNECTION_POOL_DATASOURCE_CLASSNAME')
    userName = os.environ.get('DATABASE_USERNAME')
    password = os.environ.get('DATABASE_PASSWORD')
    hostName = os.environ.get('DATABASE_HOST_NAME')
    port = os.environ.get('DATABASE_PORT')
    schemaName = os.environ.get('DATABASE_SCHEMA_NAME')

    # JDBC connection setting is added only when all the information for connecting to the database is complete.
    if resourceType is not None and \
        dataSourceClassName is not None and \
        hostName is not None and \
        port is not None and \
        schemaName is not None and \
        userName is not None and \
        password is not None:
        __createJdbcConnectionPool(resourceType, dataSourceClassName, schemaName, hostName, port, password, userName)
        resourceName = os.environ.get('JDBC_RESOURCE_NAME')
        __createJdbcResource(resourceName)

        # Load connection pool configuration
        time.sleep(3)
        subprocess.call(["./asadmin", "stop-domain"])
        subprocess.call(["./asadmin", "start-domain"])

    # Tail the server log to make the process resident.
    serverLog = glassfishRoot + "/domains/domain1/logs/server.log"
    subprocess.call(["tail", "-F", serverLog])

def __createJdbcConnectionPool(resourceType, dataSourceClassName, databaseName, serverName, port, password, userName):
    command = """
            ./asadmin create-jdbc-connection-pool                                                                               \
            --restype {resourceType}                                                                                            \
            --datasourceclassname {dataSourceClassName}                                                                         \
            --property user={userName}:password={password}:databaseName={databaseName}:serverName={serverName}:port={port}      \
            connection-pool
        """.format(
            resourceType = resourceType,
            dataSourceClassName = dataSourceClassName,
            databaseName = databaseName,
            serverName = serverName,
            port = port,
            password = password,
            userName = userName
        )
    subprocess.call(command, shell=True)

def __createJdbcResource(resourceName):
    command = "./asadmin create-jdbc-resource --connectionpoolid connection-pool {resourceName}".format(
        resourceName = resourceName
    )
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    main()