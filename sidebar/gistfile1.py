import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from cStringIO import StringIO
from io import BytesIO
import base64

from flask import Flask
app = Flask(__name__)

html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''

@app.route("/")
def hello():
    df = pd.DataFrame(
        {'y':np.random.randn(10), 'z':np.random.randn(10)},
        index=pd.period_range('1-2000',periods=10),
    )
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df.plot(ax=ax)

    # io = StringIO()
    io = BytesIO()
    fig.savefig(io, format='png')
    data = base64.encodestring(io.getvalue())

    return html.format(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
