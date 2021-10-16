#!/bin/bash

# INSTALL DOCKER
yum install -y docker
service docker start

# START ARGUS
mkdir /usr/local/argus
cat >/usr/local/argus/start_argus.sh <<EOF
#!/bin/bash
TARGET=\$1
if [ "\$(docker ps -aq -f name=\$TARGET)" ]; then
  echo "Removing existing container for \${TARGET}"
    docker rm -f \$TARGET
fi
docker run --name \$TARGET -v \$TARGET:/usr/local/argus/data --restart=on-failure -d -t argus:latest python main.py --user \${TARGET}
EOF
cat >/usr/local/argus/update_argus.sh <<EOF
#!/bin/bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
docker pull 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
docker tag 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest argus:latest
EOF
cat >/usr/local/argus/update_and_start.sh <<EOF
#!/bin/bash
source /usr/local/argus/update_argus.sh
source /usr/local/argus/start_argus.sh oli
source /usr/local/argus/start_argus.sh pa
source /usr/local/argus/start_argus.sh ash
EOF
source /usr/local/argus/update_and_start.sh
