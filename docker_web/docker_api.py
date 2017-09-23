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



def stop_rm_con(con_name):
    container=docker_cmd.containers(all=True)
    if len(container)==0:
        print "\033[31m container is empty!\033[0m"
    else:
        for id in container:
	    if con_name in id["Names"][0]:
		container_id=id["Id"]
        	docker_cmd.stop(container=container_id)
        	docker_cmd.remove_container(container=container_id)
        	print "\033[31mDelete container ID %s\033[0m" % container_id


def create_con(image,cmd,con_name,port):
    container_id=docker_cmd.create_container(image=image,command=cmd,ports=[port],volumes=['/alidata/www/tomcat/logs/'],
                                host_config=docker_cmd.create_host_config(port_bindings={port:8080},dns=['192.168.1.110','223.5.5.5'],),name=con_name,labels={'aliyun.logs.%sstdout' % con_name:'stdout','aliyun.logs.%scatalina' % con_name:'/alidata/www/tomcat/logs/catalina.out'},detach=True)
    docker_cmd.start(container=container_id["Id"])

if __name__=="__main__":
    url="tcp://192.168.1.10:2375"
    con_name = "lvbb"
    tagname = "lvbb:%s" % image_time
    dockerfile_path = "/hptx_docker/%s/" % con_name
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
    create_images(path_file=dockerfile_path,tagname=tagname)
    stop_rm_con(con_name=con_name)
    create_con(image="lvbb:"+image_time,cmd=cmd,con_name=con_name,port=8080)












