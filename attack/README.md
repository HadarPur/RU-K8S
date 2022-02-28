# Installation

## 1) GCP Attcker Machine config
    ### a) Allow full access for gcp api for the machine ( you know that tick you need to set when the machine is off...)
    ### b) Make sure `gcloud` is configured, on gcp machines it should come built-in.
    ### c) On local machine install gcloud and run gcloud auth login - login using you gcp account

## 2) install prerequsitis (ubuntu)

#### Clone git

```
sudo apt-get install git-all
```

```
git clone https://github.com/HadarPur/RU-K8S-FinalProject.git
```

#### Run initialize.sh script

```
./initialize.sh
```

#### Login to gcloud

```
gcloud auth login
```

```
gcloud container clusters get-credentials microsvc-us --zone=us-central1-a
```

#### Make sure we got the api toke by running:

```
cat ~/.kube/config
```

You should see some certificate or a Bearer token You should see a context similar to this
```
 context:
    cluster: gke_independent-bay-250811_us-central1-a_microsvc-us
    user: gke_independent-bay-250811_us-central1-a_microsvc-us
  name: gke_independent-bay-250811_us-central1-a_microsvc-us
current-context: gke_independent-bay-250811_us-central1-a_microsvc-us
```

## 3) now you should be able to run the script
```
python3 yoyo_attaker_flow.py
```

