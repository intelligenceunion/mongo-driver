About
=================

**iu_mongo** is a simple mongo driver based on [pymongo](https://docs.mongodb.com/ecosystem/drivers/python/) (the official mongodb driver for python language) and provide convinient features such like **Document Definition** and **Document Manipulation** just like [mongoengine](http://mongoengine.org/), and the codes are based on mongoengine(but are not dependent on mongoengine). The only dependence of **iu_mongo** is pymongo.

Supported pymongo version
================
pymongo with version 3.7+ is supported

Supported python version
=======
python 3+ is supported

Installation
=====
just install iu_mongo as a VCS pip package installation in editable mode

    pip install -e git+git://github.com/intelligenceunion/mongo-driver.git

Document Definition
=============
**Document Definition** is very like to mongoengine. Still, little difference is between them.

```python
    from iu_mongo.document import Document, EmbeddedDocument
    from iu_mongo.fields import *

    class TestEDoc(EmbeddedDocument):
        test_int = IntField()


    class TestDoc(Document):
        meta = {
            'db_name': 'test'
        }
        test_int = IntField()
        test_str = StringField()
        test_pk = IntField(required=True)
        test_list = ListField(IntField())
        test_edoc = EmbeddedDocumentField('TestEDoc')
        test_dict = DictField()
        test_list_edoct = EmbeddedDocumentListField('TestEDoc')
```
Note that thare are two main difference between iu_mongo and mongoengine when defining a document

1. `db_field` is never needed, iu_mongo will use the **field name** as the field name when saving documents into mongodb.
2. `primary_key` is not supported, please issue an unique index build if you need a primary key

Also, please specify `meta['db_name']` to a db name in which database iu_mongo will store documents for mongodb

Document Manipulation
====
iu_mongo provide many collection-level operations as well as document-level operations. Supported operations are

- find
- find_iter
- find_one
- count
- distinct
- reload
- update
- find_and_modify
- remove
- save
- delete
- update_one
- set, unset, inc, push, pull, add_to_set
  
Also, iu_mongo support bulk-like operations, for example
```python
    with TestDoc.bulk() as bulk_context:
        for i in range(10):
            TestDoc.bulk_update(bulk_context, {
                'test_pk': {'$lt': 10 * (i + 1), '$gt': 10 * i}
            }, {
                '$set': {
                    'test_int': 1000
                }
            }, multi=False)
```

supported bulk operations are
- bulk_save
- bulk_update
- bulk_remove
- bulk_update_one
- bulk_set
- bulk_inc
- bulk_push
- bulk_pull
- bulk_add_to_set

Contribute guidelines
=====
1. Make sure you have [pipenv](https://pipenv.readthedocs.io/en/latest/) and python3 environment
2. Clone or fork this repo then run `pipenv install` in the repo directory to setup a python virtual environment with all dev dependencies installed.
3. Write your codes to add new features to iu_mongo
4. Before commit your codes, please write unit test to make sure iu_mongo will perform well based on your change, run `pipenv run test_all` to issue an entire testing and make sure all test cases are PASSED. You can also run `pipenv run test_single MODULE/CLASS/CLASS METHOD/MODULE PATH` to just issue a test in your test module or class, this is useful when you just want your new-write test cases are tested.
5. After everything is done (write codes, test codes), push your commits and issue a pull request if needed be.