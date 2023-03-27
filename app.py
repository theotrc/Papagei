#! /usr/bin/env python
from App import app,db 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8000)