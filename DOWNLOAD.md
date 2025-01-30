Dataset **Fruit Recognition** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzE5NDJfRnJ1aXQgUmVjb2duaXRpb24vZnJ1aXQtcmVjb2duaXRpb24tRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiaFVFWUk0alp2NjIrY0lHa0hKdy9DeSsxTmFNOVMvVTRMdmpQTzZIS2FnST0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Fruit Recognition', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://zenodo.org/record/1310165/files/Fruit%20-Database.rar?download=1).