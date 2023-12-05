python test.py 100 --reuse &
python test.py 1000 --reuse &
python test.py 10000 --reuse &

wait
python result.py