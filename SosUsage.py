from enum import Enum

import os, re

from path import Path


from PromStat import PromStat, AGGR
from MongoDataStore import MongoDataStore


#hyperdrive_http_bytes_reclaimable_free_space.json:                    "__name__": "hyperdrive_http_bytes_reclaimable_free_space",
#hyperdrive_relocation_byte_reclaimed_total.json:                    "__name__": "hyperdrive_relocation_byte_reclaimed_total",
#hyperdrive_http_bytes_net.json
#hyperdrive_http_key_net.json
#hyperdrive_index_capacity.json
# hyperdrive_index_free.json
#hyperdrive_index_nbkeys.json

class SosUsage:

    sosmetrics = None
    datastore = []

    def __init__(self, sosarchive):
        self.sosmetrics = sosarchive +'/sos_commands/metalk8s/metrics/'
        if Path(sosarchive +'/sos_commands/artesca').is_dir():
            files = os.listdir(sosarchive +'/sos_commands/artesca')
            for file in files:
                if (re.search("(.*)eval_db.getCollection___infost", file)):
                    self.datastore.append(sosarchive +'/sos_commands/artesca/' + str(file))
        else:
            print("No mongodb output found")

    def extractUsage(self):
        available = PromStat(self.sosmetrics+'/kubelet_volume_stats_available_bytes.json')
        capacity = PromStat(self.sosmetrics+'/kubelet_volume_stats_capacity_bytes.json')
        xcore_objects_net = PromStat(self.sosmetrics+'/hyperdrive_http_object_net.json')
        xcore_bytes_net = PromStat(self.sosmetrics+'/hyperdrive_http_bytes_net.json')
        xcore_reclaimable = PromStat(self.sosmetrics+'/hyperdrive_http_bytes_reclaimable_free_space.json')

        mongodb_capa = capacity.extractFilteredMetric("persistentvolumeclaim", 'datadir-data-db-mongodb-sharded-shard[0-9]-data-[0-9]', AGGR.MAX, AGGR.MAX)
        mongodb_used = mongodb_capa - available.extractFilteredMetric("persistentvolumeclaim", 'datadir-data-db-mongodb-sharded-shard[0-9]-data-[0-9]', AGGR.MAX, AGGR.MAX)

        xcore_index_capa = capacity.extractFilteredMetric("persistentvolumeclaim", 'artesca-storage-service-(.*)-index', AGGR.MAX, AGGR.MAX)
        xcore_index_used = xcore_index_capa - available.extractFilteredMetric("persistentvolumeclaim", 'artesca-storage-service-(.*)-index', AGGR.MAX, AGGR.MAX)

        xcore_data_capa = capacity.extractFilteredMetric("persistentvolumeclaim", 'artesca-storage-service-(.*)-data(.*)', AGGR.MAX, AGGR.SUM)
        xcore_data_used = xcore_data_capa - available.extractFilteredMetric("persistentvolumeclaim", 'artesca-storage-service-(.*)-data(.*)', AGGR.MAX, AGGR.SUM)


        xcore_objects = xcore_objects_net.extractMetric(AGGR.MAX, AGGR.SUM)
        xcore_protected = xcore_bytes_net.extractMetric(AGGR.MAX, AGGR.SUM)
        xcore_reclaimable = xcore_reclaimable.extractMetric(AGGR.MAX, AGGR.MAX)

        mongo_data_store = MongoDataStore(self.datastore)

        print("=======================  USAGE  =======================")
        print("mongodb used = " + '{:.1f}'.format(mongodb_used/1024/1024/1024) + " GiB")
        print("mongodb capa = " + '{:.1f}'.format(mongodb_capa/1024/1024/1024) + " GiB")
        print("mongodb usage = " + '{:.1f}%'.format(mongodb_used/mongodb_capa*100))

        print("xcore index used = " + '{:.1f}'.format(xcore_index_used/1024/1024/1024) + " GiB")
        print("xcore index capa = " + '{:.1f}'.format(xcore_index_capa/1024/1024/1024) + " GiB")
        print("xcore index usage = " + '{:.1f}%'.format(xcore_index_used/xcore_index_capa*100))

        print("xcore data used = " + '{:.1f}'.format(xcore_data_used/1024/1024/1024/1024) + " TiB")
        print("xcore data capa = " + '{:.1f}'.format(xcore_data_capa/1024/1024/1024/1024) + " TiB")
        print("xcore data usage = " + '{:.1f}%'.format(xcore_data_used/xcore_data_capa*100))

        print("xcore objects  = " + '{:.0f}'.format(xcore_objects))
        print("xcore protected = " + '{:.1f}'.format(xcore_protected/1024/1024/1024/1024) + " TiB")
        print("xcore reclaimable = " + '{:.1f}'.format(xcore_reclaimable/1024/1024/1024/1024) + " TiB")

        print("countitem objects  = " + '{:.0f}'.format(mongo_data_store.objects))
        print("countitem used current = " + '{:.1f}'.format(mongo_data_store.current_usage/1024/1024/1024/1024) + " TiB")
        print("countitem used previous = " + '{:.1f}'.format(mongo_data_store.previous_usage/1024/1024) + " MiB")
        print("countitem date = " + mongo_data_store.measuredOn)

        print("orphans = " + '{:.1f}'.format((xcore_protected - mongo_data_store.current_usage - mongo_data_store.previous_usage)/1024/1024/1024/1024) + "TiB")
        print("overhead = " + '{:.3f}'.format((xcore_data_used - xcore_reclaimable)/xcore_protected))

        print("xcore avg obj size = "+ '{:.1f}'.format(xcore_protected/xcore_objects/1024) + " KiB")
        print("countitem avg obj size = "+ '{:.1f}'.format((mongo_data_store.current_usage+mongo_data_store.previous_usage)/mongo_data_store.objects/1024) + " KiB")
