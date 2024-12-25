** Steps required for setup:

1. Install python with PPA

1. Make sure the following is installed on your linux disto

```bash
sudo apt install libjpeg-dev python3.11-dev
sudo apt-get install libosmesa6
export PYOPENGL_PLATFORM=osmesa
```

1. Install requirements with:
 
```bash
pip install -r requirements.txt
```
