#!/bin/bash

# create user
USERHOME=/home/user
USERNAME=user

echo "Starting with UID : ${USER_ID:=1001}, GID: ${GROUP_ID:=1001}"
groupadd ${USERNAME} -g ${GROUP_ID} && \
[ -d ${USERHOME} ] && chown ${USER_ID} ${USERHOME}
useradd -u ${USER_ID} -g ${GROUP_ID} -d ${USERHOME} -m -s /bin/bash -G sudo ${USERNAME}

echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
# sudo時にPATHを引き継ぐ
sed -i '/Defaults.*secure_path.*/d' /etc/sudoers && \
echo 'Defaults  env_keep += "PATH"' >> /etc/sudoers

if [ "$1" != "" ]; then
    exec /usr/sbin/gosu ${USERNAME} "$@"
else
    exec /usr/sbin/gosu ${USERNAME} bash
fi