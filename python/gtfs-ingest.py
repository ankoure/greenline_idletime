#!/usr/bin/env python
from datetime import timedelta, datetime
import time
import os
from google.transit import gtfs_realtime_pb2 as gtfs
import requests
import requests_cache
import psycopg2
from psycopg2.extras import execute_values


def parse_vehicles(feed):
    Branches = ['Green-B','Green-C','Green-D','Green-E']

    for entity in list(feed.entity):
        if entity.vehicle.trip.HasField("route_id"):
            # Checks if vehicle entity is a greenline vehicle
            if entity.vehicle.trip.route_id in Branches:
                value = datetime.fromtimestamp(entity.vehicle.timestamp)
                timestamp = value.strftime("%d %B %Y %H:%M:%S")
                systemtime = datetime.now()
                delay = systemtime - value
                yield (
                    entity.id,
                    entity.vehicle.trip.route_id,
                    timestamp,
                    systemtime,
                    delay,
                    entity.vehicle.current_status,
                    entity.vehicle.current_stop_sequence,
                    entity.vehicle.stop_id,
                    entity.vehicle.trip.direction_id,
                    entity.vehicle.trip.start_time,
                    entity.vehicle.trip.start_date,
                    entity.vehicle.trip.trip_id,
                    entity.vehicle.trip.schedule_relationship,
                    "SRID=4326;POINT( %f %f )"
                    % (
                        entity.vehicle.position.longitude,
                        entity.vehicle.position.latitude
                    )
                )


# Required Environment Variable

CONNECTION = os.environ['MBTA_CONNECTION']

# Global config

URL = "https://cdn.mbta.com/realtime/VehiclePositions.pb"
POLLING_INTERVAL = 60  # seconds
requests_cache.install_cache(
    ".gtfs-cache", expire_after=timedelta(seconds=POLLING_INTERVAL)
)


if __name__ == "__main__":
    with psycopg2.connect(CONNECTION) as conn:
        while True:
            with conn.cursor() as cursor:
                response = requests.get(URL)
                feed = gtfs.FeedMessage()
                feed.ParseFromString(response.content)

                # performant way to batch inserts
                # see http://initd.org/psycopg/docs/extras.html#psycopg2.extras.execute_batch
                start = time.time()
                execute_values(
                    cursor,
                    "INSERT INTO greenline (entity_id,branch,vehicle_time,system_time,delay,current_status,current_stop_sequence,stop_id,direction_id,start_time,start_date,trip_id,schedule_relationship,geog)"
                    "VALUES %s",
                    parse_vehicles(feed),
                )
                conn.commit()
                end = time.time()
                nrows = len(feed.entity)
                print(f"Elapsed Time: {end - start})")
                time.sleep(POLLING_INTERVAL)
