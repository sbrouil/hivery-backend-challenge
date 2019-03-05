import os
import yaml

config = {}

with open('%s/config.yml' % os.path.dirname(os.path.realpath(__file__)), 'r') as configyml:
    config = yaml.load(configyml)

def get(namespace=None):
    if namespace is None:
        return config
    else:
        return config[namespace]