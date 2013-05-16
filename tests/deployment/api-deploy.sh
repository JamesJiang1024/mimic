#!/bin/bash

PWD=$(cd $(dirname $0) && pwd)
TOPDIR=$(dirname $PWD)
TOPDIR=$(dirname $TOPDIR)

mkdir -pv /etc/faucet
mkdir -pv /var/log/faucet

cp $TOPDIR/etc/faucet/api-paste.ini.sample /etc/faucet/api-paste.ini
cp $TOPDIR/etc/faucet/faucet.conf.sample /etc/faucet/faucet.conf

#### create database and tables.
##MYSQL_PASSWORD=""
##DATABASE_NAME="faucet"
##MYSQL="mysql -uroot -p${PASSWORD}"
##$MYSQL -e "DROP DATABASE IF EXISTS $DATABASE_NAME;"
##$MYSQL -e "CREATE DATABASE $DATABASE_NAME CHARACTER SET utf8;"
##$MYSQL $DATABASE_NAME < $PWD/schema.sql
##
#### add load balance into service catalog
##source faucetrc
##sed -i -e '/loadbalance/d' /etc/keystone/default_catalog.templates
##
##(cat <<EOF
##
##catalog.RegionOne.loadbalance.publicURL = http://localhost:5556/v2.0
##catalog.RegionOne.loadbalance.adminURL = http://localhost:5556/v2.0
##catalog.RegionOne.loadbalance.internalURL = http://localhost:5556/v2.0
##catalog.RegionOne.loadbalance.name = Load Balance Service
##EOF
##) >> /etc/keystone/default_catalog.templates
##
#### create keystone user
### Grab a numbered field from python prettytable output
### Fields are numbered starting with 1
### Reverse syntax is supported: -1 is the last field, -2 is second to last, etc.
### get_field field-number
##function get_field() {
##    while read data; do
##        if [ "$1" -lt 0 ]; then
##            field="(\$(NF$1))"
##        else
##            field="\$$(($1 + 1))"
##        fi
##        echo "$data" | awk -F'[ \t]*\\|[ \t]*' "{print $field}"
##    done
##}
##
##TENANT_ID=$(keystone tenant-list | grep " service " | get_field 1)
##USER_ID=$(keystone user-list | grep " faucet " | get_field 1)
##
##if [ "$USER_ID" != "" ]
##then
##    keystone user-delete $USER_ID
##fi
##
##keystone user-create --tenant_id $TENANT_ID --name faucet --pass nova --email faucet@example.com
##
##USER_ID=$(keystone user-list | grep " faucet " | get_field 1)
##ROLE_ID=$(keystone role-list | grep " admin " | get_field 1)
##
##keystone user-role-add --user_id $USER_ID --role_id $ROLE_ID --tenant_id $TENANT_ID
