import boto3
import zipfile
import sys
import os
from ctypes import cdll

# ** Start of ML Runtime **
# Don't edit :)
native_libs = {
    "sklearn-scipy-numpy":
    ["libquadmath.so.0",
     "libgfortran.so.3",
     "libatlas.so.3",
     "libptcblas.so.3",
     "libptf77blas.so.3",
     "libf77blas.so.3",
     "libcblas.so.3",
     "liblapack.so.3"]
}

def load(lib):
    print "loading " + lib
    cdll.LoadLibrary(lib)

def load_native_libs(pack):
    deps_path = "/tmp/deps/" + pack.replace("-", "_")
    for lib in native_libs.get(pack, []):
        load(deps_path + "/lib/" + lib)

def load_pack(pack):
    pack_file = "/tmp/" + pack + ".zip"
    if os.path.isfile(pack_file):
        load_native_libs(pack)
        return

    s3 = boto3.resource('s3')
    s3.Bucket("ml-engineer").download_file(pack + ".zip", pack_file)

    zip_ref = zipfile.ZipFile(pack_file, 'r')
    deps_path = "/tmp/deps/" + pack.replace("-", "_")
    zip_ref.extractall(deps_path)
    zip_ref.close()
    sys.path.append(deps_path)

    load_native_libs(pack)

load_pack("sklearn-scipy-numpy")
load_pack("pandas-numpy-pack")
# ** End of ML Runtime **

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from sklearn.externals import joblib

def train_classifier(x, y):
    clf = RandomForestClassifier(n_jobs=2, random_state=0)
    clf.fit(x, y)
    return clf

def store_model_to_s3(model, bucket, key):
    """Stores a model into S3 bucket 'ml-engineer' under the given key"""
    joblib.dump(model, "/tmp/model.pkl", compress=1)
    s3 = boto3.client('s3')
    s3.upload_file("/tmp/model.pkl", bucket, key)
    os.remove("/tmp/model.pkl")

def lambda_handler(event, context):
    """Entry point of training Lambda event execution"""

    np.random.seed(0)
    headers = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
    train_data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",names=headers)
    encoder = LabelEncoder()
    train_data['sex_dummy'] = encoder.fit_transform(train_data['sex'])
    train_data['income_dummy'] = encoder.fit_transform(train_data['income'])
    x = train_data[['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week', 'sex_dummy']]
    y = train_data['income_dummy']
    model = train_classifier(x, y)

    store_model_to_s3(model, os.environ['STACK_NAME'], "model.pkl")

    return 'Model trained'
