#!/bin/bash
cd /project/infinitebrain/inbox
for f in *_spec.json
do
	echo "Processing model for file - $f"
	python /project/infinitebrain/addmodel.py $f >&1
done
for f in *_mech.json
do
	echo "Processing mechanism for file - $f"
	python /project/infinitebrain/addmodel.py $f >&1
done



