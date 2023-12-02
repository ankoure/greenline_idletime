# Green Line Idle Time Analysis

# Requirements
- PostgreSQL
- PostGIS
- Python
- Node (optional) for PM2
- AWS Lightsail instance/EC2/Other VPS
- Geoserver (optional) to share via WFS/WMS

# Project Goals
* Ingest data into PostgreSQL w/PostGIS using gtfs-realtime python bindings
*  Determine where on the rail network, each greenline train is
*  Classify the train's position based on the following:
    *  Train in Service
    *  On Siding
    *  Train in Yard or Out of Service
* Create PostGIS Trajectories for each TripID by service day (if nessecary)
* Analyze the data to answer the following questions
    * Which intersections create the most delay for each line?
    * Which stations does each line stop at for the longest time?
    * Where else on the line do trains sit, while in service?
    * What is the average time a Green Line train is stopped while in service?
        * Where on the line do Trains sit the most?   
    * Using the PostGIS Trajectories, can we detect when bunching occurs?
        * Can the conditions that led to bunching be determined?
        * How often does "going express" to X Station remediate bunching?
       

# Quickstart
