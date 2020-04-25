### Trained models

This folder contains the 5 traine `POCOVID-Net` models as presented in the
paper.

#### Load the pretrained model
If you have the `pocovidnet` package installed (see
[pocovidnet/README.md](../README.md) for the instructions), you can use the
pretrained model by:

```python
from pocovidnet.evaluate_covid19 import Evaluator

model = Evaluator(ensemble=True)
```
*NOTE*: If you set `ensemble=True` you are using a model ensemble consisting of
all 5 models trained during cross validation.

#### Use the model
Perform a forward pass simply by:

```python
predicions = model(image)
```
*NOTE*: All images are automatically rescaled to `224 x 224` pixels, hence
quadratic images lead to better performances as the aspect ratio is maintained.
