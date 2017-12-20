=========================
Chalice App - Simple API
=========================
Chalice is a Python Serverless Microframework for AWS https://github.com/aws/chalice

Here are the endpoints:

* "/" Return a simple status message: "ok"
* "/recipe/{food}" Consume recipe puppy api and query recipes for food. Reference: http://www.recipepuppy.com/about/api/ For example: "/recipe/taco" will show recipes for tacos
* "/upload/" Accept a PNG upload, store it on S3, and publish it to an html page. TODO: Conversion of POST data to file does not produce an image.

Issues
======

In Chalice config.json,
the following needed to be specified otherwise Chalice would not deploy to aws:
"manage_iam_role":false,
"iam_role_arn": <role>
