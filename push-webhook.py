import re

from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/<repository>', methods=['POST'])
def default(repository):
    # ignore pushes other than to master
    if request.json[u'ref'] == u'refs/heads/master':

        # gather all the added and modified files
        touched = list()
        for commit in request.json[u'commits']:
            touched.extend(commit[u'added'])
            touched.extend(commit[u'modified'])

        # todo replace with real regex
        regex = re.compile("migrations")
        migrations = [x for x in touched if regex.search(x)]

        # send an email or something
        app.logger.info("migrations: %s", migrations)
    else:
        app.logger.info("push ignored")

    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')