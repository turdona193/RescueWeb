# --- Install packages we need ---
package 'python3'
package 'git'

# --- Add the data partition ---
#directory '/mnt/data_joliss'

# mount '/mnt/data_joliss' do
#   action [:mount, :enable]  # mount and add to fstab
#   device 'data_joliss'
#   device_type :label
#   options 'noatime,errors=remount-ro'
# end

# --- Set host name ---
# Note how this is plain Ruby code, so we can define variables to
# DRY up our code:
hostname = 'cis420'

file '/etc/hostname' do
  content "#{hostname}\n"
end

include_recipe "python::virtualenv"
include_recipe "python::pip"

service 'hostname' do
  action :restart
end

file '/etc/hosts' do
  content "127.0.0.1 localhost #{hostname}\n"
end


python_pip "pyramid" do
  action :install
end

python_virtualenv "/home/ubuntu/myapp" do
  interpreter "python3"
  owner "ubuntu"
  group "ubuntu"
  options "--system-site-packages"
  action :create
end

directory "/tmp/private_code/.ssh" do
  owner "ubuntu"
  recursive true
end

cookbook_file "/tmp/private_code/.ssh/id_deploy" do
  source "serverKey"
  owner "ubuntu"
  mode 00400
end

cookbook_file "/tmp/private_code/wrap-ssh4git.sh" do
  source "wrap-ssh4git.sh"
  owner "ubuntu"
  mode 00700
end

git "/home/ubuntu/myapp/teamMurrica" do
  user "ubuntu"
  group "ubuntu"
  destination "/home/ubuntu/myapp/teamMurrica"
  repository "git@cs.potsdam.edu:cis420/teamMurrica.git"
  revision "master"
  ssh_wrapper "/tmp/private_code/wrap-ssh4git.sh"

  action :checkout
end

bash "start app" do
  user "ubuntu"
  cwd "/home/ubuntu/myapp"
  code <<-EOF
source bin/activate
cd teamMurrica/rescueweb
python setup.py develop
sudo killall -9 pserve
../../bin/initialize_rescueweb_db development.ini
../../bin/pserve development.ini  
EOF
end

