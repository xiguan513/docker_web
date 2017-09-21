#!/usr/bin/env python
#-*- coding:utf-8 -*-

import docker
import time
import os


image_time=time.strftime('%Y%m%d%H%M%S')

def create_images(path_file,tagname):
    response=[line for line in docker_cmd.build(path=path_file,tag=tagname,rm=True,nocache=True)]
    for line in response:
        print line,

def stop_rm_con():
    container=docker_cmd.containers(all=True)
    if len(container)==0:
        print "\033[31m container is empty!\033[0m"
    else:
        container_id=container[0]["Id"]
        docker_cmd.stop(container=container_id)
        docker_cmd.remove_container(container=container_id)
        print "\033[31mDelete container ID %s\033[0m" % container_id


def create_con(image,cmd):
    container_id=docker_cmd.create_container(image=image,command=cmd,ports=[8080],volumes=['/alidata/www/tomcat/logs/'],
                                host_config=docker_cmd.create_host_config(port_bindings={8080:8080},dns=['192.168.1.110','223.5.5.5'],),name="lvbb",labels={'aliyun.logs.lvbbstdout':'stdout','aliyun.logs.lvbbcatalina':'/alidata/www/tomcat/logs/catalina.out'},detach=True)
    docker_cmd.start(container=container_id["Id"])


if __name__=="__main__":
    url="tcp://192.168.1.10:2375"
    tagname = "lvbb:%s" % image_time
    dockerfile_path = "/hptx_docker/lvbb/"
    war_dir=dockerfile_path+"war"+"/"
    cmd = '/opt/tomcat.sh'
    war_list={"admin":"/root/.jenkins/workspace/docker_lvbb/admin-web/target/admin-web-1.0-SNAPSHOT.war",
              "pay":"/root/.jenkins/workspace/docker_lvbb/payment-web/target/payment-web-1.0-SNAPSHOT.war"}

    if os.path.isdir(war_dir):
                war_bak=dockerfile_path+"war"+str(image_time)
		os.renames(war_dir,war_bak)
		os.mkdir(war_dir)
    else:
		os.mkdir(war_dir)

    for war in war_list.keys():
        war_file=war_list[war]
        if os.path.exists(war_file):
            os.system("cp %s %s" % (war_file,war_dir+"/"))

    docker_cmd = docker.Client(base_url=url)
    create_images(dockerfile_path, tagname)
    stop_rm_con()
    create_con("lvbb:"+image_time,cmd)
