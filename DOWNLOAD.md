Dataset **Fruit Recognition** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/W/J/L8/XbT0RLhdFsRFHnp7m7JkFj75A6dJP168aoDkAHtuie7GAolIxhMYyoVsWILzdWduZ7XT1LFiTDrQnFOArEbDtJ2ES7AETJXX24JTtSweLVs8eXCJXzaaD8U23L3B.tar)

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