from os import path
from urllib.parse import urlparse

import yaml
from flask import Flask, json, request
from kubernetes import client, config

app = Flask(__name__)


@app.route('/deployment', methods=['GET'])
def deployment_list():
    config.load_kube_config()

    from kubernetes import client
    apis_api = client.AppsV1Api()

    names = []
    for deployment in apis_api.list_namespaced_deployment(namespace="default").items:
        names.append(deployment.metadata.name)

    return json.dumps(names)


@app.route('/deployment', methods=['POST'])
def deployment_create():
    config.load_kube_config()

    dep = yaml.safe_load(request.get_data(False, True))
    k8s_apps_v1 = client.AppsV1Api()
    
    resp = k8s_apps_v1.create_namespaced_deployment(
        body=dep, 
        namespace="default")

    return "Deployment created. status='%s'" % resp.metadata.name


if __name__ == "__main__":
    app.run(debug=True)

