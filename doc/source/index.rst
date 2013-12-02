.. mimic documentation master file, created by
   sphinx-quickstart on Mon Dec  2 11:12:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mimic's documentation!
=================================

Contents:

    Project mimic 是uos installer以及hostmanager的后端, 承担安装uos的业务逻辑。


Getting Started For Developer
-----------------------------
install foreman: http://theforeman.org/manuals/1.2/#3.InstallingForeman

git clone git@git.ustack.com:ustack/mimic.git 

安装依赖、配置环境::
   
    virtualenv .venv
    source .venv/bin/activate
    pip install -r mimic/test_requirements
    pip install -r mimic/requirements

单元测试::
    
    testr run

覆盖率测试::

    python setup.py testr --coverage 
    coverage report -m

Getting Started For User
------------------------

安装UOS: wget http://mirrors.ustack.com/uos/dailybuild/uOS-dayilbuild-2013-12-02.iso

安装完成以后得到一个endpoint比如说是http://192.168.10.11

代码环境::

    git clone git@git.ustack.com:ustack/mimic.git
    virtualenv .venv
    source .venv/bin/activate
    python setup.py install

配置环境 /etc/mimic/mimic.conf ::

   foreman_address = http://192.168.10.11:3000
   foreman_proxy_address = http://192.168.10.11:8443

Mimic_API

Structure
---------------

UOS installer的后端包括了几个部分：

- 注册
- 网段分配
- 网络检测
- 服务安装

Host Manager的后端包括了几个部分:

- 硬件发现
- 硬件自动注册
- 机器角色判断
- 参数规则判断

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
