echo "apt-get update" 
echo "apt-get update"
sudo apt-get update
echo "apt-get install -y curl"
sudo apt-get install -y curl
echo "sudo apt-get install -y default-jre openjdk-11-jre-headless openjdk-8-jre-headless"
sudo apt-get install -y default-jre openjdk-11-jre-headless openjdk-8-jre-headless
echo "curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash" 
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash
echo "sudo apt install nodejs" 
sudo apt install nodejs
echo "sudo apt-get"
sudo apt-get update
echo "Install gcloud"
sudo apt-get install apt-transport-https ca-certificates gnupg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.listcurl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
gcloud init      
echo "sudo apt-get"
sudo apt-get update
echo "Install k8s"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
sudo apt-get install -y kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
echo "curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash"
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash
echo "sudo apt install nodejs"
sudo apt install nodejs
echo "sudo apt-get"
sudo apt-get update
echo "sudo apt-get install -y apt-transport-https"
sudo apt-get install -y apt-transport-https
echo "curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
echo "sudo apt-get"
sudo apt-get update
echo "sudo apt-get install -y kubectl"
sudo apt-get install -y kubectl
echo "sudo apt-get install -y python3-pip"
sudo apt-get install -y python3-pip
echo "sudo npm install -g loadtest"
sudo npm install -g loadtest
echo "gcloud auth login"
gcloud auth login 
gcloud auth login
echo "gcloud container clusters get-credentials microsvc-us --zone=us-central1-a"
gcloud container clusters get-credentials microsvc-us --zone=us-central1-a
echo "cat ~/.kube/config"
cat ~/.kube/config
echo "pip install -r requirements.txt"
pip install -r requirements.txt
