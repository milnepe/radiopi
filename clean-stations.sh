#!/bin/sh -x

sed -E 's/\\u00a9|\\u009|\\u00b3|\\u00a1|\\u00a8|\\u00bc|\\u00a8|\\u00b|\\u00a6|\\u00a4|\\u00ae|\\u00e3|\\u0083|\\u00e3|\\u00828|\\u00e3|\\u0082|\\u00aa|\\u00e7|\\u00ac|\\u00ac1//g' "etc/radiopi/stations.orig.json" > "etc/radiopi/stations.json"
