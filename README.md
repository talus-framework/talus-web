To troubleshoot master connectivity.
```
rs0:PRIMARY> use talus
switched to db talus
rs0:PRIMARY> db.master.find()
{ "_id" : ObjectId("58fe2e7384c2692ad7f7d2b9"), "hostname" : "talus", "ip" : "10.0.0.8", "vms" : [ ], "queues" : {  } }
rs0:PRIMARY> quit()
```

To troubleshoot slave connectivity.
```
mongo
rs0:PRIMARY> use talus
switched to db talus
rs0:PRIMARY> db.slave.find()
{ "_id" : ObjectId("58fe2fba84c2692ad7f7d2bb"), "hostname" : "slave-linux", "uuid" : "ed36482c-fa70-44c0-bdcb-6461bf7b13e0", "ip" : "10.0.0.16", "max_vms" : 2, "running_vms" : 0, "total_jobs_run" : 0, "vms" : [ ], "timestamps" : { "created" : ISODate("2017-04-24T17:02:50.352Z"), "modified" : 1493053420.399946 } }
rs0:PRIMARY> quit()
```


Logs:
```
tail -f /var/log/talus/apache2/access.log 
journalctl -u docker.talus-web.service
```
