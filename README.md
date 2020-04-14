# pm_data_types
Data types common to the components of Peri Meleon
These types are designed for encoding and decoding with jsonpickle.
jsonpickle handles nested objects.
To make things easier for jsonpickle, enumeration properties
and dates are encoded before being stored inside the objects.
(Actually this is to make things easier for the guy who has to
write Java code that produces unpicklable JSON--jsonpickle can
handle enums and dates just fine, but the syntax gets involved.)

## Install
git clone git@github.com:fkuhl/pm_data_types

cd pm_data_types

python3 -m pip install -r requirements.txt

## Run test program
python3 ./try-data.py
