#!/bin/bash


# Ensure ISHAR_WEB environment variable is set.
if [ -z ${ISHAR_WEB+x} ]; then
    >&2 echo "No IsharMUD ishar-web variable!"
    exit 1
fi
echo "IsharMUD ishar-web: ${ISHAR_WEB}"

# Ensure the "ishar-web" repository folder is present.
export ISHAR_CONTENT="${ISHAR_WEB}/ishar-web"
if [ ! -d ${ISHAR_CONTENT} ]; then
    >&2 echo "Cannot find ishar-web (${ISHAR_CONTENT})!"
    exit 1
fi

# Pull "ishar-web" Git repository.
git -C ${ISHAR_CONTENT} pull

# Ensure the "ishar-web" Python3 virtual environment ("venv") exists.
export ISHAR_VENV="${ISHAR_WEB}/venv/bin"
if [ ! -d ${ISHAR_VENV} ]; then
    >&2 echo "Cannot find virtual environment (${ISHAR_VENV})!"
    exit 1
fi

# Activate "ishar-web" Python3 virtual environment, which should include Django.
source ${ISHAR_VENV}/activate

# Ensure latest pip3 and Python project requirements are installed.
${ISHAR_VENV}/pip3 install -U pip &&
${ISHAR_VENV}/pip3 install -r ${ISHAR_CONTENT}/requirements.txt

# Perform any Django database migrations.
${ISHAR_VENV}/python3 ${ISHAR_CONTENT}/manage.py migrate

# Delete all Django static content and re-collect it.
rm -rf ${ISHAR_WEB}/static &&
${ISHAR_VENV}/python3 ${ISHAR_CONTENT}/manage.py collectstatic --no-input

# Clear the Django cache.
find ${ISHAR_WEB}/cache/ -type f -name '*.djcache' -delete

# Restart daphne/Django.
XDG_RUNTIME_DIR=/run/user/$UID systemctl --user restart daphne.service

# Tail the end of the daphne log(s) and show systemd status.
sleep 3 && tail -n 100 ${ISHAR_WEB}/logs/*
XDG_RUNTIME_DIR=/run/user/$UID systemctl --user --no-pager status daphne

exit 0
