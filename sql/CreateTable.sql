-- public.greenline definition

-- Drop table

DROP TABLE public.greenline;

CREATE TABLE public.greenline (
	autopk serial4 NOT NULL,
	entity_id varchar(25) NULL,
	branch varchar(25) NULL,
	vehicle_time timestamptz NULL,
	system_time timestamptz NULL,
	delay time NULL,
	current_status varchar(100) NULL,
	current_stop_sequence int4 NULL,
	stop_id varchar(25) NULL,
	direction_id int4 NULL,
	start_time varchar(10) NULL,
	start_date varchar(10) NULL,
	trip_id varchar(64) NULL,
	schedule_relationship varchar(64) NULL,
	geog public.geography(point, 4326) NULL,
	CONSTRAINT greenline_pk PRIMARY KEY (autopk)
);
CREATE INDEX greenline_entity_id_idx ON public.greenline USING btree (entity_id);
CREATE INDEX greenline_geog_idx ON public.greenline USING GIST (geog);
CREATE INDEX greenline_vehicle_time_idx ON public.greenline USING btree (vehicle_time);
CREATE INDEX greenline_system_time_idx ON public.greenline USING btree (system_time);