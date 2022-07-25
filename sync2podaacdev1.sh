#!/bin/bash

cd docs
make html
cd ..
 
rsync -azvv docs/build/html podaac-dev1:/data/export/ftppub/outgoing/2022_UWG_Meeting/


