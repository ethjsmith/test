#!/bin/bash

$0
cd /srv/salt/managed_files/monster-dev/
git pull
salt _X_ state.apply
