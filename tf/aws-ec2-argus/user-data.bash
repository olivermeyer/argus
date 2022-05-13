#!/bin/bash

# INSTALL DOCKER
yum install -y docker
service docker start

# INSTALL ARGUS
mkdir /usr/local/argus
cat >/usr/local/argus/update_argus.sh <<EOF
#!/bin/bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 595687261518.dkr.ecr.eu-west-1.amazonaws.com
docker pull 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest
docker tag 595687261518.dkr.ecr.eu-west-1.amazonaws.com/argus:latest argus:latest
EOF
source /usr/local/argus/update_argus.sh
