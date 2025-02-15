"""Documentation fragments for the database_list module"""

specdoc_examples = ['''
- name: List all of the databases for the current Linode Account
  linode.cloud.database_list: {}''', '''
- name: Resolve all MySQL databases for the current Linode Account
  linode.cloud.database_list:
    filters:
      - name: engine
        values: mysql''']

result_images_samples = ['''[
   {
      "allow_list": [
         "203.0.113.1/32",
         "192.0.1.0/24"
      ],
      "cluster_size": 3,
      "created": "2022-01-01T00:01:01",
      "encrypted": false,
      "engine": "mysql",
      "hosts": {
         "primary": "lin-123-456-mysql-mysql-primary.servers.linodedb.net",
         "secondary": "lin-123-456-mysql-primary-private.servers.linodedb.net"
      },
      "id": 123,
      "instance_uri": "/v4/databases/mysql/instances/123",
      "label": "example-db",
      "region": "us-east",
      "status": "active",
      "type": "g6-dedicated-2",
      "updated": "2022-01-01T00:01:01",
      "updates": {
         "day_of_week": 1,
         "duration": 3,
         "frequency": "weekly",
         "hour_of_day": 0,
         "week_of_month": null
      },
      "version": "8.0.26"
   }
]''']
