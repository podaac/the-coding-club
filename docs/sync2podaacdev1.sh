#!/bin/bash

make html
rsync -azvv build/html podaac-dev1:/data/export/ftppub/outgoing/2022_UWG_Meeting/


