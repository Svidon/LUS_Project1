# LUS_Project1

First project for Language Understanding System course about *Concept tagging*.

The dataset used is about movies and it can be found at LINK.

Here some basic information is explained. For more details look at `report.pdf`

---

## Data Analysis

In the folder `data_analysis` there is some little data analysis regarding the distribution of the tags present in the dataset.

## How to use

You have to have installed python3, opengrm and openfst.

There are two different models a more advanced one and a basic one. To run any of the models just enter the folder and type `make` or `make help`. This command will display all the instructions for running the model in a correct way. With wrong commands the model will give errors. The basic ones are:
* `make help` to display the help message
* `make train order=<num> method=<method>` to train the model. **num** has to be a number and it indicates the order of the **n-grams** used to build the language model. **method** is the smoothing method for the language model (type help to see a list of possible methods)
* `make test` it applies the model to the testing set
* `make clean` it deletes all the generated files of both the training and testing part

## Results

When `make test` is run, it will generate two meaningful files. The first is `result.txt` and it will contain every sentence of the test set with the resulting tag. The second is `evaluation.txt` and it provides meaningful statistics about the accuracy of the model on the test set: this is generated thanks to the `conlleval.pl` file in the `extra` folder.

The `extra` folder also contains the results of the model with the optimal parameters found and its evaluation. The optimal parameters are specified in the evaluation name (e.g. `evaluation_2_absolute.txt` contains the evaluation of the basic model with `order=2` and `method=aboslute`).

Finally the `model_evaluation` contains all the evaluations of the model with all the parameters that were tested.

## Status

ATM the basic model is built and evaluated. The advanced core is working and improvements are on the way.
