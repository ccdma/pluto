#!/bin/bash

USERNAME=user
USERHOME=/home/${USERNAME}

function createsu () {
    groupadd ${USERNAME} -g ${GROUP_ID} && \
    [ -d ${USERHOME} ] && chown ${USER_ID} ${USERHOME}
    useradd -u ${USER_ID} -g ${GROUP_ID} -d ${USERHOME} -m -s /bin/bash -G sudo ${USERNAME}

    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    # sudo時にPATHを引き継ぐ
    sed -i '/Defaults.*secure_path.*/d' /etc/sudoers && \
    echo 'Defaults  env_keep += "PATH"' >> /etc/sudoers
}

id -u ${USERNAME} &>/dev/null || createsu

exec /usr/sbin/gosu ${USERNAME} "$@"
