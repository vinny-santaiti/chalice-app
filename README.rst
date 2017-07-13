=========================
Chalice App - Simple API
=========================
.. Chalice is a Python Serverless Microframework for AWS

Here are the endpoints:
1.
"/"
Return a simple status message: "ok"

2.
"/recipe/{food}"
Consume recipe puppy api and query recipes for food

.. http://www.recipepuppy.com/about/api/

For example:
"/recipe/taco" will show recipes for tacos

3.
"/upload/"
accept a PNG upload, store it on S3, and publish it to an html page.

Issues

In chalice config.json,
the following needed to be specified otherwise Chalice would not deploy to aws:
"manage_iam_role":false,
"iam_role_arn": <role>

Demo

https://o4hmmtm9x7.execute-api.us-east-2.amazonaws.com/dev/
