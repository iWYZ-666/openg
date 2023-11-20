docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j
 python3 manage.py runserver 0.0.0.0:8000
