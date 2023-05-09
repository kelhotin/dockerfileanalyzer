## Dockerfile static analyzer
### Requirements
* Python 3.9
* Docker client
  * Developed with ubuntu, no idea how this works with Windows

### To run
```
python analyzer.py <Path-to-Dockerfile>`  
```
### To test
inside `test` folder
```
python -m pytest
```