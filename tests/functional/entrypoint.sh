#!/bin/bash
#!/bin/bash

python3 pip install -r ./requirements.txt
python3 ./wait_for_services.py
pytest 