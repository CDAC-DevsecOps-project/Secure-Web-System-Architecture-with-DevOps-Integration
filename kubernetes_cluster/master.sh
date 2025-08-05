# Setup for Control Plane (Master) servers

hostname
POD_CIDR="192.168.0.0/16"

# Pull required images
sudo kubeadm config images pull

# get the private IP of the master node    
MASTER_PRIVATE_IP=$(hostname -I | awk '{print $1}')
sudo kubeadm init   --apiserver-advertise-address="$MASTER_PRIVATE_IP"   --apiserver-cert-extra-sans="$MASTER_PRIVATE_IP"   --pod-network-cidr="$POD_CIDR"   --ignore-preflight-errors=Swap


# Configure kubeconfig
mkdir -p "$HOME"/.kube
sudo cp -i /etc/kubernetes/admin.conf "$HOME"/.kube/config
sudo chown "$(id -u)":"$(id -g)" "$HOME"/.kube/config

# Install Calico Network Plugin Network 
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Kubernetes cluster join command on worker nodes
sudo kubeadm join 192.168.80.170:6443 \
  --token kdlqe2.zax68knueqdcwoy5 \
  --discovery-token-ca-cert-hash sha256:ac94453bf1514ffe736e59ee73c050d23c46d90961fd54032fa0fd8ea54bfc8e

# After installation of cluster, on master node
kubectl get nodes
watch -n 1 kubectl get nodes