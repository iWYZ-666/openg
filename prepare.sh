pip install -r requirements.txt
python3 src/download_json.py
docker run -d \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j
python3 src/create_graph.py